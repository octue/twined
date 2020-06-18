import unittest
from twined import Twine, exceptions
from .base import BaseTestCase


class TestTwine(BaseTestCase):
    """ Testing operation of the Twine class
     """

    def test_init_twine_with_filename(self):
        """ Ensures that the twine class can be instantiated with a file
        """
        twine_file = self.path + 'apps/simple_app/twine.json'
        Twine(file=twine_file)

    def test_init_twine_with_json(self):
        """ Ensures that a twine can be instantiated with a json string
        """
        with open(self.path + 'apps/simple_app/twine.json', 'r', encoding='utf-8') as f:
            json_string = f.read()
        Twine(json=json_string)

    def test_init_twine_with_incorrect_file_string(self):
        """ Ensures that error is raised instantiating with a non-filename
        """
        with self.assertRaises(exceptions.MissingTwine):
            Twine(file='{"mistakenly_passed": "json instead of filename"}')

    def test_init_twine_with_both_inputs(self):
        """ Ensures that error is raised when attempting to instantiate with both file and json inputs
        """
        with self.assertRaises(exceptions.InvalidInput):
            Twine(
                file=self.path + 'apps/simple_app/twine.json',
                json='{"input_values": "something"}'
            )

    def test_missing_twine_file(self):
        """ Ensures that an absent file raises a MissingTwine exception
        """
        twine_file = 'file_is_missing.json'
        with self.assertRaises(exceptions.MissingTwine):
            Twine(file=twine_file)

    def test_no_twine(self):
        """ Tests that the canonical-but-useless case of no twine provided validates whilst issuing a warning
        """
        with self.assertLogs(level='WARNING') as log:
            Twine()
            self.assertEqual(len(log.output), 1)
            self.assertEqual(len(log.records), 1)
            self.assertIn('No twine file specified', log.output[0])

    def test_empty_twine(self):
        """ Ensures that an empty twine file can be loaded
        """
        twine_file = self.path + 'apps/empty_app/twine.json'
        with self.assertLogs(level='DEBUG') as log:
            Twine(file=twine_file)
            self.assertEqual(len(log.output), 2)
            self.assertEqual(len(log.records), 2)
            self.assertIn('Loaded', log.output[0])
            self.assertIn('Validated', log.output[1])

    def test_example_twine(self):
        """ Ensures that the example (full) twine can be loaded and validated
        """
        twine_file = self.path + 'apps/example_app/twine.json'
        Twine(file=twine_file)

    def test_simple_twine(self):
        """ Ensures that the simple app schema can be loaded and used to parse some basic config and values data
        """
        twine_file = self.path + 'apps/simple_app/twine.json'
        Twine(file=twine_file)

    def test_broken_json_twine(self):
        """ Ensures that an invalid json file raises an InvalidTwine exception
        """
        twine_file = self.path + 'twines/invalid_json_twine.json'
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(file=twine_file)


if __name__ == '__main__':
    unittest.main()
