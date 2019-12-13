import unittest
from twined import Twine


class TestSchema(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_twine_with_filename(self):
        """ Ensures that the simple app schema can be loaded and used to parse some basic config and values data
        """
        twine_file = 'data/simple_app/twine.json'
        twine = Twine(twine_file)

    def test_empty_twine(self):
        """ Ensures that an empty twine can be loaded
        """
        twine_file = 'data/empty_app/twine.json'
        twine = Twine(twine_file)

    def test_example_twine(self):
        """ Ensures that the example (full) twine can be loaded
        """
        twine_file = 'data/example_app/twine.json'
        twine = Twine(twine_file)

    def test_twine_simple_configuration(self):
        """ Ensures that the simple app schema can be loaded and used to parse some basic config and values data
        """

        twine_file = 'data/simple_app/twine.json'
        twine = Twine(twine_file)

        input_config_file = 'data/simple_app/input/config.json'
        input_manifest_file = 'data/simple_app/input/manifest.json'

if __name__ == '__main__':
    unittest.main()
