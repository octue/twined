import os
import unittest

from twined import Twine, exceptions
from .base import BaseTestCase


class TestTwine(BaseTestCase):
    """ Testing operation of the Twine class
     """

    def test_init_twine_with_filename(self):
        """ Ensures that the twine class can be instantiated with a file
        """
        twine_file = os.path.join(self.path, "apps/simple_app/twine.json")
        Twine(source=twine_file)

    def test_init_twine_with_json(self):
        """ Ensures that a twine can be instantiated with a json string
        """
        with open(os.path.join(self.path, "apps/simple_app/twine.json"), "r", encoding="utf-8") as f:
            json_string = f.read()
        Twine(source=json_string)

    def test_no_twine(self):
        """ Tests that the canonical-but-useless case of no twine provided validates empty
        """
        Twine()

    def test_incorrect_version_twine(self):
        """ Ensures exception is thrown on mismatch between installed and specified versions of twined
        """
        twine_file = os.path.join(self.path, "twines/incorrect_version_twine.json")
        with self.assertRaises(exceptions.TwineVersionConflict):
            Twine(source=twine_file)

    def test_empty_twine(self):
        """ Ensures that an empty twine file can be loaded
        """
        with self.assertLogs(level="DEBUG") as log:
            Twine(source="{}")
            self.assertEqual(len(log.output), 3)
            self.assertEqual(len(log.records), 3)
            self.assertIn("Detected source", log.output[0])
            self.assertIn("Validated", log.output[1])

    def test_example_twine(self):
        """ Ensures that the example (full) twine can be loaded and validated
        """
        twine_file = os.path.join(self.path, "apps/example_app/twine.json")
        Twine(source=twine_file)

    def test_simple_twine(self):
        """ Ensures that the simple app schema can be loaded and used to parse some basic config and values data
        """
        twine_file = os.path.join(self.path, "apps/simple_app/twine.json")
        Twine(source=twine_file)

    def test_broken_json_twine(self):
        """ Ensures that an invalid json file raises an InvalidTwine exception
        """
        twine_file = os.path.join(self.path, "twines/invalid_json_twine.json")
        with self.assertRaises(exceptions.InvalidTwineJson):
            Twine(source=twine_file)


if __name__ == "__main__":
    unittest.main()
