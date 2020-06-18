import json as jsonlib
import logging
import pkg_resources
from . import exceptions
from jsonschema import validate as jsonschema_validate, ValidationError


logger = logging.getLogger(__name__)


SCHEMA_STRANDS = (
    'input_values',
    'configuration',
    'output_values',
)

MANIFEST_STRANDS = (
    'input_manifest',
    'output_manifest',
)

CREDENTIAL_STRANDS = ('credentials',)

CHILDREN_STRANDS = ('children',)

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

    def _load_twine(self, file=None, json=None):
        """ Load twine from a *.json file or a json string and validates twine contents
        """

        if (file is None) and (json is None):
            # If loading an unspecified twine, return an empty one rather than raising error (like in _load_data())
            self._raw = {}
            logger.warning('No twine file specified. Loading empty twine.')
        else:
            self._raw = self._load_json('twine', file=file, json=json)

        self._validate_against_schema('twine', self._raw)
        self._validate_twine_version()

    def _load_json(self, kind, file=None, json=None):
        """ Loads data from either a *.json file or a json string
        """

        if (file is None) and (json is None):
            raise exceptions.TwineTypeException(f'Cannot load {kind} - no file name or json string specified')

        # Decode the json string and deserialize to objects
        try:
            # From the file...
            if file is not None:
                if json is not None:
                    raise exceptions.TwineTypeException('You cannot specify both file and json inputs')

                try:
                    with open(file) as f:
                        data = jsonlib.load(f)
                        logger.debug('Loaded %s from file %s', kind, file)
                except FileNotFoundError as e:
                    raise exceptions.file_not_found_map[kind](e)

            # Directly from the string...
            else:
                data = jsonlib.loads(json)
                logger.debug('Loaded %s from input json string', kind)

        except jsonlib.decoder.JSONDecodeError as e:
            raise exceptions.invalid_json_map[kind](e)

        return data

    def _validate_against_schema(self, strand, data):
        """ Validates data against a schema, raises exceptions of type Invalid<strand>Json if not compliant.

        Can be used to validate:
            - values data for compliance with schema (for schema based strands) or
            - the twine file contents itself against the present version twine spec
        """
        if strand == "twine":
            # A twine *contains* schema, but we also need to verify that it matches a certain schema itself
            # The twine schema is distributed with this packaged to ensure version consistency...
            schema = jsonlib.loads(pkg_resources.resource_string('twined', 'schema/twine_schema.json'))
        else:
            if strand not in SCHEMA_STRANDS:
                raise exceptions.TwineTypeException(f'Unknown strand {strand}. Try one of {SCHEMA_STRANDS}.')
            schema_key = strand + '_schema'
            schema = self._raw[schema_key]

        try:
            jsonschema_validate(instance=data, schema=schema)
            logger.debug('Validated %s against schema', strand)

        except ValidationError as e:
            raise exceptions.invalid_contents_map[strand](e.message)

    def _validate_twine_version(self):
        """ Validates that the installed version is consistent with an optional version specification in the twine file
        """
        installed_twined_version = pkg_resources.get_distribution("twined").version
        twine_file_twined_version = self._raw.get('twined_version', None)
        logger.debug(
            'Twine versions... %s installed, %s specified in twine', installed_twined_version, twine_file_twined_version
        )
        if (twine_file_twined_version is not None) and (installed_twined_version != twine_file_twined_version):
            raise exceptions.TwineVersionConflict(
                f'Twined library version conflict. Twine file requires {twine_file_twined_version} but you have {installed_twined_version} installed'
            )

    def validate_configuration(self, **kwargs):
        """ Validates that the configuration values, passed as either a file or a json string, are correct
        """
        config = self._load_json('configuration', **kwargs)
        self._validate_against_schema('configuration', config)
        return config

    def validate_input_values(self, **kwargs):
        """ Validates that the input values, passed as either a file or a json string, are correct
        """
        data = self._load_json('input_values', **kwargs)
        self._validate_against_schema('input_values', data)
        return data

    def validate_output_values(self, **kwargs):
        """ Validates that the output values, passed as either a file or a json string, are correct
        """
        data = self._load_json('output_values', **kwargs)
        self._validate_against_schema('output_values', data)
        return data

    # def validate(
    #     self,
    #     configuration=None,
    #     manifest=None,
    #     credentials=None,
    #     monitors=None,
    #     logs=None,
    # ):
    #     """ Validates that inputs to an application are correct
    #     """
    #     pass
