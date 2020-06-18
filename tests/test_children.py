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


# class TestChildrenValidation(unittest.TestCase):
#     """ Tests related to whether validation of children occurs successfully (given a valid twine)
#     """
#
#     def test_no_children(self):
#         """ Test that a twine with no children will validate on an empty children input
#         """
#         raise exceptions.NotImplementedYet()
#
#     def test_missing_children(self):
#         """ Test that a twine with children will not validate on an empty children input
#         """
#         raise exceptions.NotImplementedYet()
#
#     def test_extra_children(self):
#         """ Test that a twine with no children will not validate a non-empty children input
#         """
#         raise exceptions.NotImplementedYet()
#
#     def test_matched_children(self):
#         """ Test that a twine with children required will validate when the children input matches
#         """
#         raise exceptions.NotImplementedYet()


if __name__ == "__main__":
    unittest.main()
