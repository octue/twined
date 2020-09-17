import json as jsonlib
import logging
import os
import pkg_resources

from jsonschema import ValidationError
from jsonschema import validate as jsonschema_validate

from dotenv import load_dotenv
from .utils import load_json
from . import exceptions

logger = logging.getLogger(__name__)


SCHEMA_STRANDS = (
    "input_values",
    "configuration_values",
    "output_values",
)

MANIFEST_STRANDS = (
    "configuration_manifest",
    "input_manifest",
    "output_manifest",
)

CREDENTIAL_STRANDS = ("credentials",)

CHILDREN_STRANDS = ("children",)

ALL_STRANDS = (
    *SCHEMA_STRANDS,
    *MANIFEST_STRANDS,
    *CREDENTIAL_STRANDS,
    *CHILDREN_STRANDS,
)


class Twine:
    def __init__(self, **kwargs):
        """ Instantiate a twine class, providing a file name or a utf-8 encoded string containing valid json.
        The twine is itself validated to be correct against the twine schema.

        Note: Instantiating the twine does not validate that any inputs to an application are correct - it merely
        checks that the twine itself is correct.

        """
        self._load_twine(**kwargs)

    def _load_twine(self, source=None):
        """ Load twine from a *.json filename, file-like or a json string and validates twine contents
        """

        if source is None:
            # If loading an unspecified twine, return an empty one rather than raising error (like in _load_data())
            self._raw = {}
            logger.warning("No twine source specified. Loading empty twine.")
        else:
            self._raw = self._load_json("twine", source, allowed_kinds=('file-like', 'filename', 'string'))

        self._validate_against_schema("twine", self._raw)
        self._validate_twine_version()

    def _load_json(self, kind, source, **kwargs):
        """ Loads data from either a *.json file, an open file pointer or a json string. Directly returns any other data
        """

        if source is None:
            raise exceptions.TwineTypeException(f"Cannot load {kind} - no data source specified")

        # Decode the json string and deserialize to objects
        try:
            data = load_json(source, **kwargs)
        except FileNotFoundError as e:
            raise exceptions.file_not_found_map[kind](e)

        except jsonlib.decoder.JSONDecodeError as e:
            raise exceptions.invalid_json_map[kind](e)

        return data

    def _validate_against_schema(self, strand, data):
        """ Validates data against a schema, raises exceptions of type Invalid<strand>Json if not compliant.

        Can be used to validate:
            - the twine file contents itself against the present version twine spec
            - children data against the required schema for the present version twine spec
            - values data for compliance with schema written in the twine (for strands like input_values_schema)
        """
        if strand == "twine":
            # The data is a twine. A twine *contains* schema, but we also need to verify that it matches a certain
            # schema itself. The twine schema is distributed with this packaged to ensure version consistency...
            schema = jsonlib.loads(pkg_resources.resource_string("twined", "schema/twine_schema.json"))

        elif strand in CHILDREN_STRANDS:
            # The data is a list of children. The "children" strand of the twine describes matching criteria for
            # the children, not the schema of the "children" data, which is distributed with this package to ensure
            # version consistency...
            schema = jsonlib.loads(pkg_resources.resource_string("twined", "schema/children_schema.json"))

        elif strand in MANIFEST_STRANDS:
            # The data is a manifest of files. The "*_manifest" strands of the twine describe matching criteria used to
            # filter files appropriate for consumption by the digital twin, not the schema of the manifest data, which
            # is distributed with thie package to ensure version consistency...
            schema = jsonlib.loads(pkg_resources.resource_string("twined", "schema/manifest_schema.json"))

        else:
            if strand not in SCHEMA_STRANDS:
                raise exceptions.TwineTypeException(f"Unknown strand {strand}. Try one of {ALL_STRANDS}.")
            schema_key = strand + "_schema"
            schema = self._raw[schema_key]

        try:
            jsonschema_validate(instance=data, schema=schema)
            logger.debug("Validated %s against schema", strand)

        except ValidationError as e:
            raise exceptions.invalid_contents_map[strand](str(e))

    def _validate_twine_version(self):
        """ Validates that the installed version is consistent with an optional version specification in the twine file
        """
        installed_twined_version = pkg_resources.get_distribution("twined").version
        twine_file_twined_version = self._raw.get("twined_version", None)
        logger.debug(
            "Twine versions... %s installed, %s specified in twine", installed_twined_version, twine_file_twined_version
        )
        if (twine_file_twined_version is not None) and (installed_twined_version != twine_file_twined_version):
            raise exceptions.TwineVersionConflict(
                f"Twined library version conflict. Twine file requires {twine_file_twined_version} but you have {installed_twined_version} installed"
            )

    def _validate_values(self, kind, source, values_class=None, **kwargs):
        """ Common values validator method
        """
        data = self._load_json(kind, source, **kwargs)
        self._validate_against_schema(kind, data)
        if values_class:
            # TODO create a values object from the data
            pass
        return data

    def _validate_manifest(self, kind, source, manifest_class=None, **kwargs):
        """ Common manifest validator method
        """
        data = self._load_json(kind, source, **kwargs)
        self._validate_against_schema(kind, data)
        if manifest_class:
            # TODO create a manifest object and verify that all the required keys etc are there
            pass
        return data

    def validate_children(self, **kwargs):
        """ Validates that the children values, passed as either a file or a json string, are correct
        """
        # TODO cache this loaded data keyed on a hashed version of kwargs
        children = self._load_json("children", **kwargs)
        self._validate_against_schema("children", children)

        strand = self._raw.get("children", [])

        # Loop the children and accumulate values so we have an O(1) check
        children_keys = {}
        for child in children:
            children_keys[child["key"]] = children_keys.get(child["key"], 0) + 1

        # Check there is at least one child for each item described in the strand
        # TODO add max, min num specs to the strand schema and check here
        for item in strand:
            strand_key = item["key"]
            if children_keys.get(strand_key, 0) <= 0:
                raise exceptions.InvalidValuesContents(f"No children found matching the key {strand_key}")

        # Loop the strand and add unique keys to dict so we have an O(1) check
        strand_keys = {}
        for item in strand:
            strand_keys[item["key"]] = True

        # Check that each child has a key which is described in the strand
        for child in children:
            child_key = child["key"]
            if not strand_keys.get(child_key, False):
                raise exceptions.InvalidValuesContents(
                    f"Child with key '{child_key}' found but no such key exists in the 'children' strand of the twine."
                )

        # TODO Additional validation that the children match what is set as required in the Twine
        return children

    def validate_credentials(self, dotenv_path=None):
        """ Validates that all credentials required by the twine are present

        Credentials may either be set as environment variables or defined in a '.env' file. If not present in the
        environment, validate_credentials will check for variables in a .env file (if present) and populate the
        environment with them. If not present in either the environment or the .env file, default values are used
        (if defined) or an error is thrown.

        Typically a .env file resides at the root of your application (the working directory) although a specific path
        may be set using the `dotenv_path` argument.

        .env files should never be committed to git or any other version control system.

        A .env file can look like this:
        ```
        # a comment that will be ignored.
        YOUR_SECRET_VALUE=itsasecret
        MEANING_OF_LIFE=42
        MULTILINE_VAR="hello\nworld"
        ```
        Or like this (also useful for bash users):
        ```
        export YOUR_SECRET_VALUE=itsasecret
        export MEANING_OF_LIFE=42
        export MULTILINE_VAR="hello\nworld"
        ```
        """

        # Load any variables from the .env file into the environment
        dotenv_path = dotenv_path or os.path.join(".", ".env")
        load_dotenv(dotenv_path)

        # Loop through the required credentials to check for presence of each
        credentials = {}
        for credential in self._raw.get("credentials", []):
            name = credential["name"]
            default = credential.get("default", None)
            credentials[name] = os.environ.get(name, default)
            if credentials[name] is None:
                raise exceptions.CredentialNotFound(f"Credential '{name}' missing from environment or .env file")

        return credentials

    def validate_configuration_values(self, source, **kwargs):
        """ Validates that the configuration values, passed as either a file or a json string, are correct
        """
        return self._validate_values("configuration_values", source, **kwargs)

    def validate_input_values(self, source, **kwargs):
        """ Validates that the input values, passed as either a file or a json string, are correct
        """
        return self._validate_values("input_values", source, **kwargs)

    def validate_output_values(self, source, **kwargs):
        """ Validates that the output values, passed as either a file or a json string, are correct
        """
        return self._validate_values("output_values", source, **kwargs)

    def validate_configuration_manifest(self, source, **kwargs):
        """ Validates the input manifest, passed as either a file or a json string
        """
        return self._validate_manifest("configuration_manifest", source, **kwargs)

    def validate_input_manifest(self, source, **kwargs):
        """ Validates the input manifest, passed as either a file or a json string
        """
        return self._validate_manifest("input_manifest", source, **kwargs)

    def validate_output_manifest(self, source, **kwargs):
        """ Validates the output manifest, passed as either a file or a json string
        """
        return self._validate_manifest("output_manifest", source, **kwargs)
