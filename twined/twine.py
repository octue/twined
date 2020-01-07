import json as jsonlib
import logging
import pkg_resources
from . import exceptions
from jsonschema import validate as jsonschema_validate, ValidationError


logger = logging.getLogger(__name__)


class Twine:

    def __init__(self, **kwargs):
        """ Instantiate a twine class, providing a file name or a utf-8 encoded string containing valid json.
        The twine is itself validated to be correct against the twine schema.

        Note: Instantiating the twine does not validate that any inputs to an application are correct - it merely
        checks that the twine itself is correct.

        """
        self._load_twine(**kwargs)

    def _load_twine(self, file=None, json=None):
        """ Load twine from a *.json file or a json string and validate its contents
        """

        # Default twine with nothing in it
        if (file is None) and (json is None):
            self._raw = {}
            logger.warning('No twine file specified. Loading empty twine.')
            return

        # Decode the json string and deserialize to objects
        try:
            # From the file...
            if file is not None:
                if json is not None:
                    raise exceptions.InvalidInput('You cannot specify both file and json inputs')

                try:
                    with open(file) as f:
                        self._raw = jsonlib.load(f)
                        logger.debug('Loaded twine from file %s', file)
                except FileNotFoundError as e:
                    raise exceptions.MissingTwine(e)

            # Directly from the string...
            else:
                self._raw = jsonlib.loads(json)
                logger.debug('Loaded twine from input json string')

            self._validate_twine()

        except jsonlib.decoder.JSONDecodeError as e:
            raise exceptions.InvalidTwine(e)

    def _validate_twine(self):
        """ Validate that the loaded twine contains all required parts and that each part is valid.

         A twine *contains* schema, but we also need to verify that it matches a certain schema itself.

        """
        twine_schema = jsonlib.loads(pkg_resources.resource_string('twined', 'schema/twine_schema.json'))

        try:
            jsonschema_validate(instance=self._raw, schema=twine_schema)
            logger.debug('Validated raw twine against schema')

        except ValidationError as e:
            raise exceptions.InvalidTwine(e.message)

    def validate(
        self,
        configuration=None,
        manifest=None,
        credentials=None,
        monitors=None,
        logs=None,
    ):
        pass
