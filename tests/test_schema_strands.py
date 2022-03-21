import os
import unittest
from tempfile import TemporaryDirectory

from twined import Twine, exceptions
from .base import VALID_SCHEMA_TWINE, BaseTestCase


class TestSchemaStrands(BaseTestCase):
    """Testing operation of the Twine class for validation of data using strands which contain schema"""

    VALID_CONFIGURATION_VALUE = """{"n_iterations": 1}"""

    def test_invalid_strand(self):
        """Ensures that an incorrect strand name would lead to the correct exception
        Note: This tests an internal method. The current API doesn't allow this error to emerge but tthis check allows
        us to extend to a generic method
        """
        twine = Twine(source=VALID_SCHEMA_TWINE)
        data = twine._load_json("configuration", source=self.VALID_CONFIGURATION_VALUE)
        with self.assertRaises(exceptions.UnknownStrand):
            twine._validate_against_schema("not_a_strand_name", data)

    def test_missing_values_files(self):
        """Ensures that if you try to read values from missing files, the right exceptions get raised"""
        twine = Twine(source=VALID_SCHEMA_TWINE)
        values_file = os.path.join(self.path, "not_a_file.json")

        with self.assertRaises(exceptions.ConfigurationValuesFileNotFound):
            twine.validate_configuration_values(source=values_file)

        with self.assertRaises(exceptions.InputValuesFileNotFound):
            twine.validate_input_values(source=values_file)

        with self.assertRaises(exceptions.OutputValuesFileNotFound):
            twine.validate_output_values(source=values_file)

    def test_no_values(self):
        """Ensures that giving no data source raises an invalidJson error"""
        with self.assertRaises(exceptions.InvalidValuesJson):
            Twine(source=VALID_SCHEMA_TWINE).validate_configuration_values(source=None)

    def test_empty_values(self):
        """Ensures that appropriate errors are generated for invalid values"""
        with self.assertRaises(exceptions.InvalidValuesJson):
            Twine(source=VALID_SCHEMA_TWINE).validate_configuration_values(source="")

    def test_strand_not_found(self):
        """Ensures that if a twine doesn't have a strand, you can't validate against it"""
        valid_no_output_schema_twine = """
           {
                "configuration_values_schema": {
                    "$schema": "https://json-schema.org/draft/2019-09/schema",
                    "title": "The example configuration form",
                    "description": "The configuration strand of an example twine",
                    "type": "object",
                    "properties": {
                        "n_iterations": {
                            "description": "An example of an integer configuration variable, called 'n_iterations'.",
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 10,
                            "default": 5
                        }
                    }
                }
            }
        """

        with self.assertRaises(exceptions.StrandNotFound):
            Twine(source=valid_no_output_schema_twine).validate_output_values(source="{}")

    def test_incorrect_values(self):
        """Ensures that appropriate errors are generated for invalid values"""
        incorrect_configuration_value = """{"n_iterations": "should not be a string, this field requires an integer"}"""
        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine(source=VALID_SCHEMA_TWINE).validate_configuration_values(source=incorrect_configuration_value)

    def test_missing_not_required_values(self):
        """Ensures that appropriate errors are generated for missing values"""
        Twine(source=VALID_SCHEMA_TWINE).validate_output_values(source="{}")

    def test_missing_required_values(self):
        """Ensures that appropriate errors are generated for missing values"""
        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine(source=VALID_SCHEMA_TWINE).validate_input_values(source="{}")

    def test_valid_values_files(self):
        """Ensures that values can be read and validated correctly from files on disk"""
        twine = Twine(source=VALID_SCHEMA_TWINE)

        with TemporaryDirectory() as tmp_dir:
            valid_configuration_file = self._write_json_string_to_file(self.VALID_CONFIGURATION_VALUE, tmp_dir)
            twine.validate_configuration_values(source=valid_configuration_file)
            twine.validate_input_values(source="""{"height": 40}""")
            twine.validate_output_values(source="""{"width": 36}""")

    def test_valid_values_json(self):
        """Ensures that values can be read and validated correctly from a json string"""
        Twine(source=VALID_SCHEMA_TWINE).validate_configuration_values(source=self.VALID_CONFIGURATION_VALUE)

    def test_valid_with_extra_values(self):
        """Ensures that extra values get ignored"""
        configuration_valid_with_extra_field = """
            {
                "n_iterations": 1,
                "another_field": "may or may not be quietly ignored"
            }
        """

        Twine(source=VALID_SCHEMA_TWINE).validate_configuration_values(source=configuration_valid_with_extra_field)


if __name__ == "__main__":
    unittest.main()
