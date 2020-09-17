import unittest

from twined import Twine, exceptions
from .base import BaseTestCase


class TestManifestStrands(BaseTestCase):
    """ Testing operation of the Twine class for validation of data using strands which require manifests
     """

    def test_missing_manifest_files(self):
        """ Ensures that if you try to read values from missing files, the right exceptions get raised
        """
        twine_file = self.path + "twines/valid_manifest_twine.json"
        twine = Twine(source=twine_file)
        file = self.path + "not_a_file.json"
        with self.assertRaises(exceptions.InputManifestFileNotFound):
            twine.validate_input_manifest(source=file)

        with self.assertRaises(exceptions.OutputManifestFileNotFound):
            twine.validate_output_manifest(source=file)

    def test_valid_manifest_files(self):
        """ Ensures that a manifest file will validate
        """
        twine_file = self.path + "twines/valid_manifest_twine.json"
        twine = Twine(source=twine_file)
        file = self.path + "manifests/inputs/input_valid.json"
        twine.validate_input_manifest(source=file)
        file = self.path + "manifests/outputs/output_valid.json"
        twine.validate_output_manifest(source=file)

    # def test_empty_values(self):
    #     """ Ensures that appropriate errors are generated for invalid values
    #     """
    #     twine_file = self.path + "twines/valid_schema_twine.json"
    #     twine = Twine(file=twine_file)
    #     values_file = self.path + "configurations/empty.json"
    #     with self.assertRaises(exceptions.InvalidValuesJson):
    #         twine.validate_configuration(file=values_file)
    #
    # def test_incorrect_values(self):
    #     """ Ensures that appropriate errors are generated for invalid values
    #     """
    #     twine_file = self.path + "twines/valid_schema_twine.json"
    #     twine = Twine(file=twine_file)
    #     values_file = self.path + "configurations/incorrect.json"
    #     with self.assertRaises(exceptions.InvalidValuesContents):
    #         twine.validate_configuration(file=values_file)
    #
    # def test_missing_not_required_values(self):
    #     """ Ensures that appropriate errors are generated for missing values
    #     """
    #     twine_file = self.path + "twines/valid_schema_twine.json"
    #     twine = Twine(file=twine_file)
    #     values_file = self.path + "outputs/missing_not_required.json"
    #     twine.validate_output_values(file=values_file)
    #
    # def test_missing_required_values(self):
    #     """ Ensures that appropriate errors are generated for missing values
    #     """
    #     twine_file = self.path + "twines/valid_schema_twine.json"
    #     twine = Twine(file=twine_file)
    #     values_file = self.path + "inputs/missing_required.json"
    #     with self.assertRaises(exceptions.InvalidValuesContents):
    #         twine.validate_input_values(file=values_file)
    #
    # def test_valid_values_files(self):
    #     """ Ensures that values can be read and validated correctly from files on disk
    #     """
    #     twine_file = self.path + "twines/valid_schema_twine.json"
    #     twine = Twine(file=twine_file)
    #     twine.validate_configuration(file=self.path + "configurations/valid.json")
    #     twine.validate_input_values(file=self.path + "inputs/valid.json")
    #     twine.validate_output_values(file=self.path + "outputs/valid.json")
    #
    # def test_valid_values_json(self):
    #     """ Ensures that values can be read and validated correctly from a json string
    #     """
    #     twine_file = self.path + "twines/valid_schema_twine.json"
    #     twine = Twine(file=twine_file)
    #     values_file = self.path + "configurations/valid.json"
    #     with open(values_file, "r", encoding="utf-8") as f:
    #         json_string = f.read()
    #     twine.validate_configuration(json=json_string)
    #
    # def test_valid_with_extra_values(self):
    #     """ Ensures that extra values get ignored
    #     """
    #     twine_file = self.path + "twines/valid_schema_twine.json"
    #     twine = Twine(file=twine_file)
    #     values_file = self.path + "configurations/valid_with_extra.json"
    #     twine.validate_configuration(file=values_file)


if __name__ == "__main__":
    unittest.main()
