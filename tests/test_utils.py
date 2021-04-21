import json
import unittest
from tempfile import TemporaryDirectory
from unittest import mock
import numpy as np

from twined import exceptions
from twined.utils import TwinedEncoder, load_json
from .base import VALID_SCHEMA_TWINE, BaseTestCase


class TestUtils(BaseTestCase):
    """Testing operation of the Twine class"""

    def test_load_json_with_file_like(self):
        """Ensures that json can be loaded from a file-like object"""
        with TemporaryDirectory() as tmp_dir:
            with open(self._write_json_string_to_file(VALID_SCHEMA_TWINE, tmp_dir), "r") as file_like:
                data = load_json(file_like)
                for key in data.keys():
                    self.assertIn(key, ("configuration_values_schema", "input_values_schema", "output_values_schema"))

    def test_load_json_with_object(self):
        """Ensures if load_json is called on an already loaded object, it'll pass-through successfully"""
        already_loaded_data = {"a": 1, "b": 2}
        data = load_json(already_loaded_data)
        for key in data.keys():
            self.assertIn(key, ("a", "b"))

    def test_load_json_with_disallowed_kind(self):
        """Ensures that when attempting to load json with a kind which is diallowed, the correct exception is raised"""
        custom_allowed_kinds = ("file-like", "filename", "object")  # Removed  "string"
        with self.assertRaises(exceptions.InvalidSourceKindException):
            load_json("{}", allowed_kinds=custom_allowed_kinds)

    def test_encoder_without_numpy(self):
        """Ensures that the json encoder can work without numpy being installed"""
        some_json = {"a": np.array([0, 1])}
        with mock.patch("twined.utils.encoders._numpy_spec", new=None):
            with self.assertRaises(TypeError) as e:
                json.dumps(some_json, cls=TwinedEncoder)

        # Very annoying behaviour change between python 3.6 and 3.8
        py38 = "Object of type 'ndarray' is not JSON serializable" in e.exception.args[0]
        py36 = "Object of type ndarray is not JSON serializable" in e.exception.args[0]
        self.assertTrue(py36 or py38)

    def test_encoder_with_numpy(self):
        """Ensures that the json encoder can work with numpy installed"""
        some_json = {"a": np.array([0, 1])}
        json.dumps(some_json, cls=TwinedEncoder)


if __name__ == "__main__":
    unittest.main()
