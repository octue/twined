import unittest

from twined import Twine, exceptions
from .base import BaseTestCase


class TestSchemaStrands(BaseTestCase):
    """ Testing operation of the Twine class for validation of data using strands which contain schema
     """

    def test_invalid_strand(self):
        """ Ensures that an incorrect strand name would lead to the correct exception
        Note: This tests an internal method. The current API doesn't allow this error to emerge but tthis check allows
        us to extend to a generic method
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        values_file = self.path + "values/configurations/configuration_valid.json"
        data = twine._load_json("configuration", source=values_file)
        with self.assertRaises(exceptions.TwineTypeException):
            twine._validate_against_schema("not_a_strand_name", data)

    def test_missing_values_files(self):
        """ Ensures that if you try to read values from missing files, the right exceptions get raised
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        values_file = self.path + "not_a_file.json"
        with self.assertRaises(exceptions.ConfigurationValuesFileNotFound):
            twine.validate_configuration_values(source=values_file)

        with self.assertRaises(exceptions.InputValuesFileNotFound):
            twine.validate_input_values(source=values_file)

        with self.assertRaises(exceptions.OutputValuesFileNotFound):
            twine.validate_output_values(source=values_file)

    def test_empty_values(self):
        """ Ensures that appropriate errors are generated for invalid values
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        values_file = self.path + "values/configurations/configuration_empty.json"
        with self.assertRaises(exceptions.InvalidValuesJson):
            twine.validate_configuration_values(source=values_file)

    def test_incorrect_values(self):
        """ Ensures that appropriate errors are generated for invalid values
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        values_file = self.path + "values/configurations/configuration_incorrect.json"
        with self.assertRaises(exceptions.InvalidValuesContents):
            twine.validate_configuration_values(source=values_file)

    def test_missing_not_required_values(self):
        """ Ensures that appropriate errors are generated for missing values
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        values_file = self.path + "values/outputs/output_missing_not_required.json"
        twine.validate_output_values(source=values_file)

    def test_missing_required_values(self):
        """ Ensures that appropriate errors are generated for missing values
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        values_file = self.path + "values/inputs/input_missing_required.json"
        with self.assertRaises(exceptions.InvalidValuesContents):
            twine.validate_input_values(source=values_file)

    def test_valid_values_files(self):
        """ Ensures that values can be read and validated correctly from files on disk
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        twine.validate_configuration_values(source=self.path + "values/configurations/configuration_valid.json")
        twine.validate_input_values(source=self.path + "values/inputs/input_valid.json")
        twine.validate_output_values(source=self.path + "values/outputs/output_valid.json")

    def test_valid_values_json(self):
        """ Ensures that values can be read and validated correctly from a json string
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        values_file = self.path + "values/configurations/configuration_valid.json"
        with open(values_file, "r", encoding="utf-8") as f:
            json_string = f.read()
        twine.validate_configuration_values(source=json_string)

    def test_valid_with_extra_values(self):
        """ Ensures that extra values get ignored
        """
        twine_file = self.path + "twines/valid_schema_twine.json"
        twine = Twine(source=twine_file)
        values_file = self.path + "values/configurations/configuration_valid_with_extra.json"
        twine.validate_configuration_values(source=values_file)


if __name__ == "__main__":
    unittest.main()
