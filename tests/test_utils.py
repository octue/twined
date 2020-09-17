import json
import unittest
from unittest import mock
import numpy as np

from twined.utils import TwinedEncoder
from .base import BaseTestCase


class TestUtils(BaseTestCase):
    """ Testing operation of the Twine class
     """

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
