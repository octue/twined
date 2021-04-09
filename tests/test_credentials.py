import os
import unittest
from unittest import mock

from twined import Twine, exceptions
from .base import VALID_SCHEMA_TWINE, BaseTestCase


class TestCredentialsTwine(BaseTestCase):
    """Tests related to the twine itself - ensuring that valid and invalid `credentials` entries in a twine file work
    as expected.
    """

    def test_fails_on_no_name(self):
        """Ensures InvalidTwine exceptions are raised when instantiating twines with a missing `name` field in a
        credential.
        """
        invalid_credentials_no_name_twine = """
            {
                "credentials": [
                    {
                        "purpose": "credentials without a name should be invalid"
                    }
                ]
            }
        """

        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=invalid_credentials_no_name_twine)

    def test_fails_on_lowercase_name(self):
        """Ensures InvalidTwine exceptions are raised when instantiating twines with lowercase letters in the `name`
        field.
        """
        invalid_credentials_lowercase_name_twine = """
            {
                "credentials": [
                    {
                        "name": "my_secrets_should_be_uppercase",
                        "purpose": "Token for accessing a 3rd party API service"
                    }
                ]
            }
        """

        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=invalid_credentials_lowercase_name_twine)

    def test_fails_on_dict(self):
        """Ensures InvalidTwine exceptions are raised when instantiating twines with invalid `credentials` entries
        (given as a dict, not an array).
        """
        invalid_credentials_dict_not_array_twine = """
            {
                "credentials": {
                    "name": "MY_API_SECRET_KEY",
                    "purpose": "Token for accessing a 3rd party API service"
                }
            }
        """

        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=invalid_credentials_dict_not_array_twine)

    def test_fails_on_name_whitespace(self):
        invalid_credentials_space_in_name_twine = """
            {
                "credentials": [
                    {
                        "name": "MY NAME SHOULD NOT HAVE WHITESPACE",
                        "purpose": "Token for accessing a 3rd party API service"
                    }
                ]
            }
        """

        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=invalid_credentials_space_in_name_twine)


class TestCredentialsValidation(BaseTestCase):
    """Tests related to whether validation of children occurs successfully (given a valid twine)"""

    VALID_CREDENTIALS_TWINE = """
        {
            "credentials": [
                {
                    "name": "SECRET_THE_FIRST",
                    "purpose": "Token for accessing a 3rd party API service",
                    "location": "local"
                },
                {
                    "name": "SECRET_THE_SECOND",
                    "purpose": "Token for accessing a 3rd party API service",
                    "location": "local"
                },
                {
                    "name": "SECRET_THE_THIRD",
                    "purpose": "Usually a big secret but sometimes has a convenient non-secret default, like a sandbox or local database",
                    "default": "postgres://pguser:pgpassword@localhost:5432/pgdb",
                    "location": "local"
                }
            ]
        }
    """

    def test_no_credentials(self):
        """Test that a twine with no credentials will validate straightforwardly"""
        twine = Twine(source=VALID_SCHEMA_TWINE)
        twine.validate_credentials()

    def test_missing_credentials(self):
        """Test that a twine with credentials will not validate where they are missing from the environment"""
        twine = Twine(source=self.VALID_CREDENTIALS_TWINE)
        with self.assertRaises(exceptions.CredentialNotFound):
            twine.validate_credentials()

    def test_default_credentials(self):
        """Test that a twine with credentials will validate where ones with defaults are missing from the environment"""
        twine = Twine(source=self.VALID_CREDENTIALS_TWINE)

        with mock.patch.dict(os.environ, {"SECRET_THE_FIRST": "a value", "SECRET_THE_SECOND": "another value"}):
            validated_credentials = twine.validate_credentials()
            self.assertEqual(validated_credentials, {"SECRET_THE_FIRST", "SECRET_THE_SECOND", "SECRET_THE_THIRD"})
            self.assertEqual(os.environ["SECRET_THE_THIRD"], "postgres://pguser:pgpassword@localhost:5432/pgdb")

    def test_non_default_credentials(self):
        """ Test that the environment will override a default value for a credential."""
        twine = Twine(source=self.VALID_CREDENTIALS_TWINE)
        with mock.patch.dict(
            os.environ,
            {"SECRET_THE_FIRST": "a value", "SECRET_THE_SECOND": "another value", "SECRET_THE_THIRD": "nondefault"},
        ):
            twine.validate_credentials()
            self.assertEqual(os.environ["SECRET_THE_THIRD"], "nondefault")

    def test_credentials_with_google_secrets(self):
        """Test that both local and Google secrets are valid as credentials."""
        valid_credentials_twine_with_google_secret = """
            {
                "credentials": [
                    {
                        "name": "LOCAL_SECRET",
                        "location": "local"
                    },
                    {
                        "name": "GOOGLE_SECRET",
                        "location": "google",
                        "project_name": "blah",
                        "version": "latest"
                    }
                ]
            }
        """

        twine = Twine(source=valid_credentials_twine_with_google_secret)
        with mock.patch.dict(os.environ, {"LOCAL_SECRET": "a value", "GOOGLE_SECRET": "My precious!"}):
            credentials = twine.validate_credentials()
            self.assertTrue("LOCAL_SECRET" in credentials)
            self.assertTrue("GOOGLE_SECRET" in credentials)


if __name__ == "__main__":
    unittest.main()
