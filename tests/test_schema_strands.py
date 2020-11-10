import os
import unittest

from twined import Twine, exceptions
from .base import VALID_SCHEMA_TWINE, BaseTestCase


class TestSchemaStrands(BaseTestCase):
    """ Testing operation of the Twine class for validation of data using strands which contain schema
     """

    def test_invalid_strand(self):
        """ Ensures that an incorrect strand name would lead to the correct exception
        Note: This tests an internal method. The current API doesn't allow this error to emerge but tthis check allows
        us to extend to a generic method
        """
        twine_file = VALID_SCHEMA_TWINE
        twine = Twine(source=twine_file)
        values_file = os.path.join(self.path, "values", "configurations", "configuration_valid.json")
        data = twine._load_json("configuration", source=values_file)
        with self.assertRaises(exceptions.UnknownStrand):
            twine._validate_against_schema("not_a_strand_name", data)

    def test_missing_values_files(self):
        """ Ensures that if you try to read values from missing files, the right exceptions get raised
        """
        twine_file = VALID_SCHEMA_TWINE
        twine = Twine(source=twine_file)
        values_file = os.path.join(self.path, "not_a_file.json")
        with self.assertRaises(exceptions.ConfigurationValuesFileNotFound):
            twine.validate_configuration_values(source=values_file)

        with self.assertRaises(exceptions.InputValuesFileNotFound):
            twine.validate_input_values(source=values_file)

        with self.assertRaises(exceptions.OutputValuesFileNotFound):
            twine.validate_output_values(source=values_file)

    def test_no_values(self):
        """ Ensures that giving no data source raises an invalidJson error
        """
        twine_file = VALID_SCHEMA_TWINE
        with self.assertRaises(exceptions.InvalidValuesJson):
            Twine(source=twine_file).validate_configuration_values(source=None)

    def test_empty_values(self):
        """ Ensures that appropriate errors are generated for invalid values
        """
        twine_file = VALID_SCHEMA_TWINE
        twine = Twine(source=twine_file)
        values_file = os.path.join(self.path, "values", "configurations", "configuration_empty.json")
        with self.assertRaises(exceptions.InvalidValuesJson):
            twine.validate_configuration_values(source=values_file)

    def test_strand_not_found(self):
        """ Ensures that if a twine doesn't have a strand, you can't validate against it
        """
        valid_no_output_schema_twine = """
           {
                "configuration_values_schema": {
                    "$schema": "http://json-schema.org/2019-09/schema#",
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
        """ Ensures that appropriate errors are generated for invalid values
        """
        twine_file = VALID_SCHEMA_TWINE
        values_file = os.path.join(self.path, "values", "configurations", "configuration_incorrect.json")
        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine(source=twine_file).validate_configuration_values(source=values_file)

    def test_missing_not_required_values(self):
        """ Ensures that appropriate errors are generated for missing values
        """
        twine_file = VALID_SCHEMA_TWINE
        values_file = os.path.join(self.path, "values", "outputs", "output_missing_not_required.json")
        Twine(source=twine_file).validate_output_values(source=values_file)

    def test_missing_required_values(self):
        """ Ensures that appropriate errors are generated for missing values
        """
        twine_file = VALID_SCHEMA_TWINE
        values_file = os.path.join(self.path, "values", "inputs", "input_missing_required.json")
        with self.assertRaises(exceptions.InvalidValuesContents):
            Twine(source=twine_file).validate_input_values(source=values_file)

    def test_valid_values_files(self):
        """ Ensures that values can be read and validated correctly from files on disk
        """
        twine_file = VALID_SCHEMA_TWINE
        twine = Twine(source=twine_file)
        twine.validate_configuration_values(
            source=os.path.join(self.path, "values", "configurations", "configuration_valid.json")
        )
        twine.validate_input_values(source=os.path.join(self.path, "values", "inputs", "input_valid.json"))
        twine.validate_output_values(source=os.path.join(self.path, "values", "outputs", "output_valid.json"))

    def test_valid_values_json(self):
        """ Ensures that values can be read and validated correctly from a json string
        """
        twine_file = VALID_SCHEMA_TWINE
        values_file = os.path.join(self.path, "values", "configurations", "configuration_valid.json")
        with open(values_file, "r", encoding="utf-8") as f:
            json_string = f.read()
        Twine(source=twine_file).validate_configuration_values(source=json_string)

    def test_valid_with_extra_values(self):
        """ Ensures that extra values get ignored
        """
        twine_file = VALID_SCHEMA_TWINE
        values_file = os.path.join(self.path, "values", "configurations", "configuration_valid_with_extra.json")
        Twine(source=twine_file).validate_configuration_values(source=values_file)


if __name__ == "__main__":
    unittest.main()
