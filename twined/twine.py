import json
import logging
import pkg_resources
from .exceptions import InvalidTwine
from jsonschema import validate, ValidationError


logger = logging.getLogger(__name__)


class Twine:

    def __init__(self, file=None):
        self._load_twine(file)

    def _load_twine(self, file=None):
        """ Load twine from a *.json file and validate its contents
        """

        # Default twine with nothing in it
        if file is None:
            self._raw = {}
            logger.debug('No twine file specified. Loading empty twine.')
            return

        # Read the json string from the file and deserialize to objects
        if not file.endswith('.json'):
            raise InvalidTwine('Specified twine filename should end in ".json". Given: %s', file)
        with open(file) as f:
            self._raw = json.load(f)
            logger.debug('Loaded twine from file %s', file)

        self._validate_twine()

    def _validate_twine(self):
        """ Validate that the loaded twine contains all required parts and that each part is valid.

         A twine *contains* schema, but we also need to verify that it matches a certain schema itself.

        """
        twine_schema = json.loads(pkg_resources.resource_string('twined', 'schema/twine_schema.json'))

        try:
            validate(instance=self._raw, schema=twine_schema)
            logger.debug('Success: validated raw twine against schema')
        except ValidationError as e:
            raise InvalidTwine(e.message)

    def validate(
        self,
        configuration=None,
        manifest=None,
        credentials=None,
        monitors=None,
        logs=None,
    ):
        pass
