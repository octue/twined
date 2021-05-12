import json as jsonlib
import logging
import os
import pkg_resources
from dotenv import load_dotenv
from jsonschema import ValidationError, validate as jsonschema_validate

from twined import exceptions
from twined.utils import ConvertStringRepresentedBooleanToBooleanType, load_json, trim_suffix


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

MONITOR_STRANDS = ("monitors",)

ALL_STRANDS = (
    *SCHEMA_STRANDS,
    *MANIFEST_STRANDS,
    *CREDENTIAL_STRANDS,
    *CHILDREN_STRANDS,
    *MONITOR_STRANDS,
)

TAG_TYPE_MAP = {
    "string": str,
    "float": float,
    "int": int,
    "boolean": ConvertStringRepresentedBooleanToBooleanType(),
}


class Twine:
    """Twine class manages validation of inputs and outputs to/from a data service, based on spec in a 'twine' file.

    Instantiate a Twine by providing a file name or a utf-8 encoded string containing valid json.
    The twine is itself validated to be correct on instantiation of Twine().

    Note: Instantiating the twine does not validate that any inputs to an application are correct - it merely
    checks that the twine itself is correct.

    """

    def __init__(self, **kwargs):
        """Constructor for the twine class"""
        for name, strand in self._load_twine(**kwargs).items():
            setattr(self, name, strand)

        self._available_strands = tuple(trim_suffix(name, "_schema") for name in vars(self))

    def _load_twine(self, source=None):
        """Load twine from a *.json filename, file-like or a json string and validates twine contents"""

        if source is None:
            # If loading an unspecified twine, return an empty one rather than raising error (like in _load_data())
            raw = {}
            logger.warning("No twine source specified. Loading empty twine.")
        else:
            raw = self._load_json("twine", source, allowed_kinds=("file-like", "filename", "string", "object"))

        self._validate_against_schema("twine", raw)
        self._validate_twine_version(twine_file_twined_version=raw.get("twined_version", None))
        return raw

    def _load_json(self, kind, source, **kwargs):
        """Loads data from either a *.json file, an open file pointer or a json string. Directly returns any other data"""

        if source is None:
            raise exceptions.invalid_json_map[kind](f"Cannot load {kind} - no data source specified.")

        # Decode the json string and deserialize to objects.
        try:
            data = load_json(source, **kwargs)
        except FileNotFoundError as e:
            raise exceptions.file_not_found_map[kind](e)

        except jsonlib.decoder.JSONDecodeError as e:
            raise exceptions.invalid_json_map[kind](e)

        return data

    def _validate_against_schema(self, strand, data):
        """Validates data against a schema, raises exceptions of type Invalid<strand>Json if not compliant.

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
            # is distributed with this package to ensure version consistency...
            schema = jsonlib.loads(pkg_resources.resource_string("twined", "schema/manifest_schema.json"))

        else:
            if strand not in SCHEMA_STRANDS:
                raise exceptions.UnknownStrand(f"Unknown strand {strand}. Try one of {ALL_STRANDS}.")
            schema_key = strand + "_schema"
            try:
                schema = getattr(self, schema_key)
            except AttributeError:
                raise exceptions.StrandNotFound(f"Cannot validate - no {schema_key} strand in the twine")

        try:
            jsonschema_validate(instance=data, schema=schema)
            logger.debug("Validated %s against schema", strand)

        except ValidationError as e:
            raise exceptions.invalid_contents_map[strand](str(e))

    def _validate_twine_version(self, twine_file_twined_version):
        """Validates that the installed version is consistent with an optional version specification in the twine file"""
        installed_twined_version = pkg_resources.get_distribution("twined").version
        logger.debug(
            "Twine versions... %s installed, %s specified in twine", installed_twined_version, twine_file_twined_version
        )
        if (twine_file_twined_version is not None) and (installed_twined_version != twine_file_twined_version):
            raise exceptions.TwineVersionConflict(
                f"Twined library version conflict. Twine file requires {twine_file_twined_version} but you have {installed_twined_version} installed"
            )

    def _validate_values(self, kind, source, cls=None, **kwargs):
        """Common values validator method"""
        data = self._load_json(kind, source, **kwargs)
        self._validate_against_schema(kind, data)
        if cls:
            return cls(**data)
        return data

    def _validate_manifest(self, kind, source, cls=None, **kwargs):
        """Common manifest validator method"""
        data = self._load_json(kind, source, **kwargs)

        # TODO elegant way of cleaning up this nasty serialisation hack to manage conversion of outbound manifests to primitive
        inbound = True
        if hasattr(data, "serialise"):
            inbound = False
            data = data.serialise()

        self._validate_against_schema(kind, data)
        converted_tags = self._validate_required_dataset_tags(kind, data)

        if cls and inbound:
            # TODO verify that all the required keys etc are there
            manifest = cls(**data)

            for dataset in manifest.datasets:
                for file in dataset.files:
                    for tag_name, tag_value in converted_tags[file.id].items():
                        setattr(file, tag_name, tag_value)

            return manifest

        return data

    def _validate_required_dataset_tags(self, manifest_type, serialised_manifest):
        """Ensure the required tags for each dataset are present on each of its files, cast them to their required
        types, and return them in a dictionary of file IDs mapped to dictionaries of `tag-name:tag-value` pairs. The
        required tags are removed from each file's `tags` key/attribute to avoid duplication, but keyword-only tags are
        left in place.

        :param str manifest_type: the kind of manifest e.g. "input_manifest"
        :param dict serialised_manifest:
        :return dict:
        """
        converted_tags = {}
        dataset_schemas = getattr(self, manifest_type)

        for dataset, dataset_schema in zip(serialised_manifest["datasets"], dataset_schemas):
            required_tags = {
                required_tag["name"]: required_tag for required_tag in dataset_schema.get("required_tags", {})
            }

            if not required_tags:
                return None

            for file in dataset["files"]:
                converted_tags[file["id"]] = {}

                # Check if any required tags are missing.
                datafile_outer_tags = {tag.split(":")[0] for tag in file["tags"]}
                missing_tags = required_tags.keys() - datafile_outer_tags

                if missing_tags:
                    raise exceptions.InvalidValuesContents(
                        f"{list(missing_tags)!r} are required tags for datafile {file['id']!r} but are missing - "
                        f"please provide values for them."
                    )

                # Remove tags from datafile.tags if they are required and valid - they will later be added as attributes
                # to the corresponding Datafile instance. Non-key-value tags and non-required key-value tags are left in
                # datafile.tags
                tags_to_remove = []

                # Validate tags and cast them to their required types.
                for tag in file["tags"]:
                    present_subtags = tag.split(":")

                    # Tags that are just keywords/labels are only used externally and are never required.
                    if len(present_subtags) == 1:
                        continue

                    if len(present_subtags) > 2:
                        raise ValueError(f"Tags cannot contain more than one colon; received {tag!r}.")

                    outer_tag, inner_tag = present_subtags
                    required_tag_info = required_tags.get(outer_tag)

                    # If the tag isn't required, nothing needs to be done to it and it can be left in file["tags"].
                    if not required_tag_info:
                        continue

                    required_type = TAG_TYPE_MAP[required_tag_info["kind"]]

                    try:
                        converted_tags[file["id"]][outer_tag] = required_type(inner_tag)
                    except (TypeError, ValueError):
                        raise TypeError(f"Tag {tag!r} for datafile {file['id']!r} should be of type {required_type!r}.")

                    tags_to_remove.append(tag)

                for tag in tags_to_remove:
                    file["tags"].remove(tag)

        return converted_tags

    @property
    def available_strands(self):
        """Tuple of strand names that are found in this twine"""
        return self._available_strands

    def validate_children(self, source, **kwargs):
        """Validates that the children values, passed as either a file or a json string, are correct"""
        # TODO cache this loaded data keyed on a hashed version of kwargs
        children = self._load_json("children", source, **kwargs)
        self._validate_against_schema("children", children)

        strand = getattr(self, "children", [])

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

    def validate_credentials(self, *args, dotenv_path=None, **kwargs):
        """Validate that all credentials required by the twine are present.

        Credentials must be set as environment variables, or defined in a '.env' file. If stored remotely in a secrets
        manager (e.g. Google Cloud Secrets), they must be loaded into the environment before validating the credentials
        strand.

        If not present in the environment, validate_credentials will check for variables in a .env file (if present)
        and populate the environment with them. Typically a .env file resides at the root of your application (the
        working directory) although a specific path may be set using the `dotenv_path` argument.

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
        if not hasattr(self, "credentials"):
            return set()

        # Load any variables from the .env file into the environment.
        dotenv_path = dotenv_path or os.path.join(".", ".env")
        load_dotenv(dotenv_path)

        for credential in self.credentials:
            if credential["name"] not in os.environ:
                raise exceptions.CredentialNotFound(
                    f"Credential {credential['name']!r} missing from environment or .env file."
                )

        return self.credentials

    def validate_configuration_values(self, source, **kwargs):
        """Validates that the configuration values, passed as either a file or a json string, are correct"""
        return self._validate_values("configuration_values", source, **kwargs)

    def validate_input_values(self, source, **kwargs):
        """Validates that the input values, passed as either a file or a json string, are correct"""
        return self._validate_values("input_values", source, **kwargs)

    def validate_output_values(self, source, **kwargs):
        """Validates that the output values, passed as either a file or a json string, are correct"""
        return self._validate_values("output_values", source, **kwargs)

    def validate_configuration_manifest(self, source, **kwargs):
        """Validates the input manifest, passed as either a file or a json string"""
        return self._validate_manifest("configuration_manifest", source, **kwargs)

    def validate_input_manifest(self, source, **kwargs):
        """Validates the input manifest, passed as either a file or a json string"""
        return self._validate_manifest("input_manifest", source, **kwargs)

    def validate_output_manifest(self, source, **kwargs):
        """Validates the output manifest, passed as either a file or a json string"""
        return self._validate_manifest("output_manifest", source, **kwargs)

    @staticmethod
    def _get_cls(name, cls):
        """Getter that will return cls[name] if cls is a dict or cls otherwise"""
        return cls.get(name, None) if isinstance(cls, dict) else cls

    def validate(self, allow_missing=False, allow_extra=False, cls=None, **kwargs):
        """Validate strands from sources provided as keyword arguments

        Usage:
        ```
            self.twine.validate(
                input_values=input_values,
                input_manifest=input_manifest,
                credentials=credentials,
                children=children,
                cls=CLASS_MAP,
                allow_missing=False,
                allow_extra=False,
            )
        ```

        :parameter allow_missing: If strand is present in the twine, but the source is equal to None, allow validation
        to continue.
        :type allow_missing: bool

        :parameter allow_extra: If strand is present in the sources, but not in the twine, allow validation to continue
        (only strands in the twine will be validated and converted, others will be returned as-is)
        :type allow_extra: bool

        :parameter cls: optional dict of classes keyed on strand name (alternatively, one single class which will be
        applied to strands) which will be instantiated with the validated source data.
        :type cls: dict or any

        :return: dict of validated and initialised sources
        :rtype: dict
        """

        # pop any strand name:data pairs out of kwargs and into their own dict
        source_kwargs = tuple(name for name in kwargs.keys() if name in ALL_STRANDS)
        sources = dict((name, kwargs.pop(name)) for name in source_kwargs)
        for strand_name, strand_data in sources.items():

            if not allow_extra:
                if (strand_data is not None) and (strand_name not in self.available_strands):
                    raise exceptions.StrandNotFound(
                        f"Source data is provided for '{strand_name}' but no such strand is defined in the twine"
                    )

            if not allow_missing:
                if (strand_name in self.available_strands) and (strand_data is None):
                    raise exceptions.TwineValueException(
                        f"The '{strand_name}' strand is defined in the twine, but no data is provided in sources"
                    )

            if strand_data is not None:
                # TODO Consider reintroducing a skip based on whether cls is already instantiated. For now, leave it the
                #  responsibility of the caller to determine what has already been validated and what hasn't.
                #     # Use the twine to validate and instantiate as the desired class
                #     if not isinstance(value, type(cls)):
                #         self.logger.debug(
                #             "Instantiating %s as %s and validating against twine", name, cls.__name__ if cls else "default_class"
                #         )
                #         return self.twine.validate(name, source=value, cls=cls)
                method = getattr(self, f"validate_{strand_name}")
                klass = self._get_cls(strand_name, cls)
                sources[strand_name] = method(strand_data, cls=klass, **kwargs)
            else:
                sources[strand_name] = None

        return sources

    def validate_strand(self, name, source, **kwargs):
        """Validates a single strand by name"""
        return self.validate({name: source}, **kwargs)[name]

    def prepare(self, *args, cls=None, **kwargs):
        """Prepares instance for strand data using a class map"""
        prepared = {}
        for arg in args:
            if arg not in ALL_STRANDS:
                raise exceptions.UnknownStrand(f"Unknown strand '{arg}'")

            elif arg not in self.available_strands:
                prepared[arg] = None

            else:
                klass = self._get_cls(arg, cls)
                prepared[arg] = klass(**kwargs) if klass else dict(**kwargs)
                if hasattr(prepared[arg], "prepare"):
                    prepared[arg] = prepared[arg].prepare(getattr(self, arg))

        return prepared
