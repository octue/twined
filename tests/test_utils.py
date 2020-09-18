import json
import unittest
from unittest import mock
import numpy as np

from twined import exceptions
from twined.utils import TwinedEncoder, load_json
from .base import BaseTestCase


class TestUtils(BaseTestCase):
    """ Testing operation of the Twine class
     """

    def test_load_json_with_file_like(self):
        """ Ensures that json can be loaded from a file-like object
        """
        file_name = self.path + "apps/simple_app/twine.json"
        with open(file_name, "r") as file_like:
            load_json(file_like)

    def test_load_json_with_disallowed_kind(self):
        """ Ensures that when attempting to load json with a kind which is diallowed, the correct exception is raised
        """
        custom_allowed_kinds = ("file-like", "filename", "object")  # Removed  "string"
        with self.assertRaises(exceptions.InvalidSourceKindException):
            load_json("{}", allowed_kinds=custom_allowed_kinds)

    def test_encoder_without_numpy(self):
        """ Ensures that the json encoder can work without numpy being installed
        """
        some_json = {"a": np.array([0, 1])}
        with mock.patch("twined.utils.encoders._numpy_spec", new=None):
            with self.assertRaises(TypeError) as e:
                json.dumps(some_json, cls=TwinedEncoder)

        self.assertEqual("Object of type 'ndarray' is not JSON serializable", e.exception.args[0])

    def test_encoder_with_numpy(self):
        """ Ensures that the json encoder can work with numpy installed
        """
        some_json = {"a": np.array([0, 1])}
        json.dumps(some_json, cls=TwinedEncoder)


if __name__ == "__main__":
    unittest.main()
