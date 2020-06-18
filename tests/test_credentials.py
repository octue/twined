import unittest

from twined import Twine, exceptions

from .base import BaseTestCase


class TestCredentialsTwine(BaseTestCase):
    """ Tests related to the twine itself - ensuring that valid and invalid
     `credentials` entries in a twine file work as expected
     """

    def test_fails_on_no_name(self):
        """ Ensures InvalidTwine exceptions are raised when instantiating twines
        with a missing `name` field in a credential
        """
        twine_file = self.path + "twines/invalid_credentials_no_name_twine.json"
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(file=twine_file)

    def test_fails_on_lowercase_name(self):
        """ Ensures InvalidTwine exceptions are raised when instantiating twines
        with lowercase letters in the `name` field
        """
        twine_file = self.path + "twines/invalid_credentials_lowercase_name_twine.json"
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(file=twine_file)

    def test_fails_on_dict(self):
        """ Ensures InvalidTwine exceptions are raised when instantiating twines
        with invalid `credentials` entries (given as a dict, not an array)
        """
        twine_file = self.path + "twines/invalid_credentials_dict_not_array_twine.json"
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(file=twine_file)

    def test_fails_on_name_whitespace(self):
        twine_file = self.path + "twines/invalid_credentials_space_in_name_twine.json"
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(file=twine_file)


# class TestCredentialsValidation(unittest.TestCase):
#     """ Tests related to whether validation of children occurs successfully (given a valid twine)
#     """
#
#     def test_no_credentials(self):
#         """ Test that a twine with no credentials will validate straightforwardly
#         """
#         raise exceptions.NotImplementedYet()
#
#     def test_missing_credentials(self):
#         """ Test that a twine with credentials will not validate where they are missing from the environment
#         """
#         raise exceptions.NotImplementedYet()
#
#     def test_matched_credentials(self):
#         """ Test that a twine with credentials required will validate when the credentials are available in the
#         environment
#         """
#         raise exceptions.NotImplementedYet()


if __name__ == "__main__":
    unittest.main()
