import os
import unittest
from unittest import mock

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
        twine_file = os.path.join(self.path, "twines", "invalid_credentials_no_name_twine.json")
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=twine_file)

    def test_fails_on_lowercase_name(self):
        """ Ensures InvalidTwine exceptions are raised when instantiating twines
        with lowercase letters in the `name` field
        """
        twine_file = os.path.join(self.path, "twines", "invalid_credentials_lowercase_name_twine.json")
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=twine_file)

    def test_fails_on_dict(self):
        """ Ensures InvalidTwine exceptions are raised when instantiating twines
        with invalid `credentials` entries (given as a dict, not an array)
        """
        twine_file = os.path.join(self.path, "twines", "invalid_credentials_dict_not_array_twine.json")
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=twine_file)

    def test_fails_on_name_whitespace(self):
        twine_file = os.path.join(self.path, "twines", "invalid_credentials_space_in_name_twine.json")
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=twine_file)


class TestCredentialsValidation(BaseTestCase):
    """ Tests related to whether validation of children occurs successfully (given a valid twine)
    """

    def test_no_credentials(self):
        """ Test that a twine with no credentials will validate straightforwardly
        """
        twine = Twine(source=os.path.join(self.path, "twines", "valid_schema_twine.json"))
        twine.validate_credentials()

    def test_missing_credentials(self):
        """ Test that a twine with credentials will not validate where they are missing from the environment
        """
        twine = Twine(source=os.path.join(self.path, "twines", "valid_credentials_twine.json"))
        with self.assertRaises(exceptions.CredentialNotFound):
            twine.validate_credentials()

    def test_default_credentials(self):
        """ Test that a twine with credentials will validate where ones with defaults are missing from the environment
        """
        twine = Twine(source=os.path.join(self.path, "twines", "valid_credentials_twine.json"))
        with mock.patch.dict(os.environ, {"SECRET_THE_FIRST": "a value", "SECRET_THE_SECOND": "another value"}):
            credentials = twine.validate_credentials()

        self.assertIn("SECRET_THE_FIRST", credentials.keys())
        self.assertIn("SECRET_THE_SECOND", credentials.keys())
        self.assertIn("SECRET_THE_THIRD", credentials.keys())
        self.assertEqual(credentials["SECRET_THE_THIRD"], "postgres://pguser:pgpassword@localhost:5432/pgdb")

    def test_nondefault_credentials(self):
        """ Test that the environment will override a default value for a credential
        """
        twine = Twine(source=os.path.join(self.path, "twines", "valid_credentials_twine.json"))
        with mock.patch.dict(
            os.environ,
            {"SECRET_THE_FIRST": "a value", "SECRET_THE_SECOND": "another value", "SECRET_THE_THIRD": "nondefault"},
        ):
            credentials = twine.validate_credentials()

        self.assertEqual(credentials["SECRET_THE_THIRD"], "nondefault")


if __name__ == "__main__":
    unittest.main()
