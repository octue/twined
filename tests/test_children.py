import unittest

from twined import Twine, exceptions
from .base import BaseTestCase


class TestChildrenTwine(BaseTestCase):
    """ Tests related to the twine itself - ensuring that valid and invalid
     `children` entries in a twine file work as expected
     """

    def test_invalid_children_dict_not_array(self):
        """ Ensures InvalidTwine exceptions are raised when instantiating twines where `children` entry is incorrectly
        specified as a dict, not an array
        """
        twine_file = self.path + "twines/invalid_children_dict_not_array_twine.json"
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(file=twine_file)

    def test_invalid_children_no_key(self):
        """ Ensures InvalidTwine exceptions are raised when instantiating twines where a child
        is specified without the required `key` field
        """
        twine_file = self.path + "twines/invalid_children_no_key_twine.json"
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(file=twine_file)

    def test_valid_children(self):
        """ Ensures that a twine can be instantiated with correctly specified children
        """
        twine_file = self.path + "twines/valid_children_twine.json"
        twine = Twine(file=twine_file)
        self.assertEqual(len(twine._raw["children"]), 1)

    def test_empty_children(self):
        """ Ensures that a twine file will validate with an empty list object as children
        """
        twine_file = self.path + "twines/valid_empty_children_twine.json"
        twine = Twine(file=twine_file)
        self.assertEqual(len(twine._raw["children"]), 0)


class TestChildrenValidation(BaseTestCase):
    """ Tests related to whether validation of children occurs successfully (given a valid twine)
    """

    def test_no_children(self):
        """ Test that a twine with no children will validate on an empty children input
        """
        twine = Twine()  # Creates empty twine
        twine.validate_children(json="[]")

    def test_missing_children(self):
        """ Test that a twine with children will not validate on an empty children input
        """
        twine = Twine(file=self.path + "twines/valid_children_twine.json")
        with self.assertRaises(exceptions.InvalidValuesContents):
            twine.validate_children(json="[]")

    def test_extra_children(self):
        """ Test that a twine with no children will not validate a non-empty children input
        """
        twine = Twine()  # Creates empty twine
        with self.assertRaises(exceptions.InvalidValuesContents):
            twine.validate_children(file=self.path + "children/valid.json")

    def test_extra_key(self):
        """ Test that children with extra data will not raise validation error
        """
        twine = Twine()  # Creates empty twine
        with self.assertRaises(exceptions.InvalidValuesContents):
            twine.validate_children(file=self.path + "children/extra_key.json")

    def test_extra_property(self):
        """ Test that children with extra data will not raise validation error
        # TODO review this behaviour - possibly should raise an error but allow for a user specified extra_data property
        """
        twine = Twine(file=self.path + "twines/valid_children_twine.json")
        twine.validate_children(file=self.path + "children/extra_property.json")

    def test_invalid_env_name(self):
        """ Test that a child uri env name not in ALL_CAPS_SNAKE_CASE doesn't validate
        """
        twine = Twine()  # Creates empty twine
        with self.assertRaises(exceptions.InvalidValuesContents):
            twine.validate_children(file=self.path + "children/invalid_env_name.json")

    def test_invalid_json(self):
        """ Tests that a children entry with invalid json will raise an error
        """
        twine = Twine(file=self.path + "twines/valid_children_twine.json")
        with self.assertRaises(exceptions.InvalidValuesJson):
            twine.validate_children(json="[")

    def test_valid(self):
        """ Test that a valid twine will validate valid children
        Valiantly and Validly validating validity since 1983.
        To those reading this, know that YOU'RE valid.
        """
        twine = Twine(file=self.path + "twines/valid_children_twine.json")
        twine.validate_children(file=self.path + "children/valid.json")


if __name__ == "__main__":
    unittest.main()
