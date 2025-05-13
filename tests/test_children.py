import unittest

from twined import Twine, exceptions

from .base import BaseTestCase


class TestChildrenTwine(BaseTestCase):
    """Tests ensuring that valid and invalid `children` entries in a twine file work as expected."""

    def test_invalid_children_dict_not_array(self):
        """Ensure that `InvalidTwine` exceptions are raised when instantiating twines where `children` entry is
        incorrectly specified as a dict, not an array.
        """
        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source="""{"children": {}}""")

    def test_invalid_children_no_key(self):
        """Ensure that `InvalidTwine` exceptions are raised when instantiating twines where a child is specified without
        the required `key` field.
        """
        source = """
            {
                "children": [{"purpose": "The purpose.", "notes": "Here are some notes."}]
            }
        """

        with self.assertRaises(exceptions.InvalidTwine):
            Twine(source=source)

    def test_valid_children(self):
        """Ensures that a twine with one child can be instantiated correctly."""
        source = """
            {
                "children": [{"key": "gis", "purpose": "The purpose.", "notes": "Some notes."}]
            }
        """
        self.assertEqual(len(Twine(source=source).children), 1)

    def test_empty_children(self):
        """Ensures that a twine file will validate with an empty list object as children"""
        twine = Twine(source="""{"children": []}""")
        self.assertEqual(len(twine.children), 0)


class TestChildrenValidation(BaseTestCase):
    """Tests related to whether validation of children occurs successfully (given a valid twine)"""

    VALID_TWINE_WITH_CHILDREN = """
        {
            "children": [{"key": "gis", "purpose": "The purpose", "notes": "Some notes."}]
        }
    """

    VALID_CHILD_VALUE = """
        [
            {
                "key": "gis",
                "id": "some-id",
                "backend": {
                    "name": "GCPPubSubBackend",
                    "project_id": "my-project"
                }
            }
        ]
    """

    def test_no_children(self):
        """Test that a twine with no children will validate on an empty children input"""
        Twine().validate_children(source=[])

    def test_missing_children(self):
        """Test that a twine with children will not validate on an empty children input."""
        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine(source=self.VALID_TWINE_WITH_CHILDREN).validate_children(source=[])

    def test_extra_children(self):
        """Test that a twine with no children will not validate a non-empty children input."""
        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine().validate_children(source=self.VALID_CHILD_VALUE)

    def test_backend_cannot_be_empty(self):
        """Test that the backend field of a child cannot be empty."""
        single_child_missing_backend = """[{"key": "gis", "id": "some-id", "backend": {}}]"""

        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine().validate_children(source=single_child_missing_backend)

    def test_extra_key_validation_on_empty_twine(self):
        """Test that children with extra data will not raise a validation error on an empty twine."""
        children_values_with_extra_data = """
            [
                {"key": "gis", "id": "id", "uri_env_name": "VAR_NAME", "an_extra_key": "not a problem if present"},
                {"key": "some_weird_other_child", "id": "some-other-id", "uri_env_name": "SOME_ENV_VAR_NAME"}
            ]
        """

        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine().validate_children(source=children_values_with_extra_data)

    def test_extra_key_validation_on_valid_twine(self):
        """Test that children with extra data will not raise a validation error on a non-empty valid twine.
        # TODO review this behaviour - possibly should raise an error but allow for a user specified extra_data property
        """
        single_child_with_extra_data = """
            [
                {
                    "key": "gis",
                    "id": "some-id",
                    "backend": {
                        "name": "GCPPubSubBackend",
                        "project_id": "my-project"
                    },
                    "some_extra_property": "should not be a problem if present"
                }
            ]
        """

        twine = Twine(source=self.VALID_TWINE_WITH_CHILDREN)
        twine.validate_children(source=single_child_with_extra_data)

    def test_invalid_env_name(self):
        """Test that a child uri env name not in ALL_CAPS_SNAKE_CASE doesn't validate"""
        child_with_invalid_environment_variable_name = """
            [
                {
                    "key": "gis",
                    "id": "some-id",
                    "uri_env_name": "an environment variable not in CAPS_CASE is invalid per the credentials spec"
                }
            ]
        """

        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine().validate_children(source=child_with_invalid_environment_variable_name)

    def test_invalid_json(self):
        """Tests that a children entry with invalid json will raise an error"""
        with self.assertRaises(exceptions.InvalidValuesJson):
            Twine(source=self.VALID_TWINE_WITH_CHILDREN).validate_children(source="[")

    def test_valid(self):
        """Test that a valid twine will validate valid children
        Valiantly and Validly validating validity since 1983.
        To those reading this, know that YOU'RE valid.
        """
        twine = Twine(source=self.VALID_TWINE_WITH_CHILDREN)
        twine.validate_children(source=self.VALID_CHILD_VALUE)


if __name__ == "__main__":
    unittest.main()
