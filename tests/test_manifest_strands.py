import os
import unittest

from twined import Twine, exceptions
from .base import BaseTestCase


class TestManifestStrands(BaseTestCase):
    """ Testing operation of the Twine class for validation of data using strands which require manifests
    """

    VALID_MANIFEST_STRAND = """
        {
            "configuration_manifest": [
                {
                    "key": "configuration_files_data",
                    "purpose": "A dataset containing files used in configuration",
                    "filters": "tags:(the AND config AND tags) files:(extension:csv AND sequence:>=0)"
                }
            ],
            "input_manifest": [
                {
                    "key": "met_mast_data",
                    "purpose": "A dataset containing meteorological mast data",
                    "filters": "tags:(met* AND mast AND location) files:(extension:csv AND sequence:>=0) location:10"
                },
                {
                    "key": "scada_data",
                    "purpose": "A dataset containing scada data",
                    "filters": "tags:(met* AND mast) files:(extension:csv AND sequence:>=0) location:10"
                }
            ],
            "output_manifest": [
                {
                    "key": "output_files_data",
                    "purpose": "A dataset containing output results",
                    "filters": "tags:(the AND output AND tags) files:(extension:csv AND sequence:>=0)"
                }
            ]
        }
    """

    def test_missing_manifest_files(self):
        """ Ensures that if you try to read values from missing files, the right exceptions get raised
        """
        twine = Twine(source=self.VALID_MANIFEST_STRAND)
        file = os.path.join(self.path, "not_a_file.json")

        with self.assertRaises(exceptions.ConfigurationManifestFileNotFound):
            twine.validate_configuration_manifest(source=file)

        with self.assertRaises(exceptions.InputManifestFileNotFound):
            twine.validate_input_manifest(source=file)

        with self.assertRaises(exceptions.OutputManifestFileNotFound):
            twine.validate_output_manifest(source=file)

    def test_valid_manifest_files(self):
        """ Ensures that a manifest file will validate
        """
        valid_configuration_manifest = """
            {
                "id": "3ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": [
                    {
                        "id": "34ad7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "my configuration dataset",
                        "tags": "the, config, tags",
                        "files": [
                            {
                                "path": "configuration/datasets/7ead7669/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": "",
                                "posix_timestamp": 0,
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                                "last_modified": "2019-02-28T22:40:30.533005Z",
                                "name": "file_1.csv",
                                "size_bytes": 59684813,
                                "sha-512/256": "somesha"
                            },
                            {
                                "path": "configuration/datasets/7ead7669/file_2.csv",
                                "cluster": 0,
                                "sequence": 1,
                                "extension": "csv",
                                "tags": "",
                                "posix_timestamp": 0,
                                "id": "bbff07bc-7c19-4ed5-be6d-a6546eae8e45",
                                "last_modified": "2019-02-28T22:40:40.633001Z",
                                "name": "file_2.csv",
                                "size_bytes": 59684813,
                                "sha-512/256": "someothersha"
                            }
                        ]
                    }
                ]
            }
        """

        valid_input_manifest = """
            {
                "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": [
                    {
                        "id": "7ead7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "my meteorological dataset",
                        "tags": "met, mast, wind",
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": "",
                                "posix_timestamp": 0,
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                                "last_modified": "2019-02-28T22:40:30.533005Z",
                                "name": "file_1.csv",
                                "size_bytes": 59684813,
                                "sha-512/256": "somesha"
                            },
                            {
                                "path": "input/datasets/7ead7669/file_2.csv",
                                "cluster": 0,
                                "sequence": 1,
                                "extension": "csv",
                                "tags": "",
                                "posix_timestamp": 0,
                                "id": "bbff07bc-7c19-4ed5-be6d-a6546eae8e45",
                                "last_modified": "2019-02-28T22:40:40.633001Z",
                                "name": "file_2.csv",
                                "size_bytes": 59684813,
                                "sha-512/256": "someothersha"
                            }
                        ]
                    }
                ]
            }
        """

        valid_output_manifest = """
            {
                "id": "2ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": [
                    {
                        "id": "1ead7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "my output dataset",
                        "tags": "the, output, tags",
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": "",
                                "posix_timestamp": 0,
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                                "last_modified": "2019-02-28T22:40:30.533005Z",
                                "name": "file_1.csv",
                                "size_bytes": 59684813,
                                "sha-512/256": "somesha"
                            },
                            {
                                "path": "input/datasets/7ead7669/file_2.csv",
                                "cluster": 0,
                                "sequence": 1,
                                "extension": "csv",
                                "tags": "",
                                "posix_timestamp": 0,
                                "id": "bbff07bc-7c19-4ed5-be6d-a6546eae8e45",
                                "last_modified": "2019-02-28T22:40:40.633001Z",
                                "name": "file_2.csv",
                                "size_bytes": 59684813,
                                "sha-512/256": "someothersha"
                            }
                        ]
                    }
                ]
            }
        """

        twine = Twine(source=self.VALID_MANIFEST_STRAND)
        twine.validate_input_manifest(source=valid_configuration_manifest)
        twine.validate_input_manifest(source=valid_input_manifest)
        twine.validate_output_manifest(source=valid_output_manifest)

    # def test_empty_values(self):
    #     """ Ensures that appropriate errors are generated for invalid values
    #     """
    #     twine_file = VALID_SCHEMA_TWINE
    #     twine = Twine(file=twine_file)
    #     values_file = os.path.join(self.path, "configurations", "empty.json")
    #     with self.assertRaises(exceptions.InvalidValuesJson):
    #         twine.validate_configuration(file=values_file)
    #
    # def test_incorrect_values(self):
    #     """ Ensures that appropriate errors are generated for invalid values
    #     """
    #     twine_file = VALID_SCHEMA_TWINE
    #     twine = Twine(file=twine_file)
    #     values_file = os.path.join(self.path, "configurations", "incorrect.json")
    #     with self.assertRaises(exceptions.InvalidValuesContents):
    #         twine.validate_configuration(file=values_file)
    #
    # def test_missing_not_required_values(self):
    #     """ Ensures that appropriate errors are generated for missing values
    #     """
    #     twine_file = VALID_SCHEMA_TWINE
    #     twine = Twine(file=twine_file)
    #     values_file = os.path.join(self.path, "outputs", "missing_not_required.json")
    #     twine.validate_output_values(file=values_file)
    #
    # def test_missing_required_values(self):
    #     """ Ensures that appropriate errors are generated for missing values
    #     """
    #     twine_file = VALID_SCHEMA_TWINE
    #     twine = Twine(file=twine_file)
    #     values_file = os.path.join(self.path, "inputs", "missing_required.json")
    #     with self.assertRaises(exceptions.InvalidValuesContents):
    #         twine.validate_input_values(file=values_file)
    #
    # def test_valid_values_files(self):
    #     """ Ensures that values can be read and validated correctly from files on disk
    #     """
    #     twine_file = VALID_SCHEMA_TWINE
    #     twine = Twine(file=twine_file)
    #     twine.validate_configuration(file=os.path.join(self.path, "configurations", "valid.json"))
    #     twine.validate_input_values(file=os.path.join(self.path, "inputs", "valid.json"))
    #     twine.validate_output_values(file=os.path.join(self.path, "outputs", "valid.json"))
    #
    # def test_valid_values_json(self):
    #     """ Ensures that values can be read and validated correctly from a json string
    #     """
    #     twine_file = VALID_SCHEMA_TWINE
    #     twine = Twine(file=twine_file)
    #     values_file = os.path.join(self.path, "configurations", "valid.json")
    #     with open(values_file, "r", encoding="utf-8") as f:
    #         json_string = f.read()
    #     twine.validate_configuration(json=json_string)
    #
    # def test_valid_with_extra_values(self):
    #     """ Ensures that extra values get ignored
    #     """
    #     twine_file = VALID_SCHEMA_TWINE
    #     twine = Twine(file=twine_file)
    #     values_file = os.path.join(self.path, "configurations", "valid_with_extra.json")
    #     twine.validate_configuration(file=values_file)


if __name__ == "__main__":
    unittest.main()
