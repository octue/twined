import os

from twined import Twine, exceptions
from .base import BaseTestCase


class TestManifestStrands(BaseTestCase):
    """Testing operation of the Twine class for validation of data using strands which require manifests"""

    VALID_MANIFEST_STRAND = """
        {
            "configuration_manifest": {
                "datasets": {
                    "configuration_files_data": {
                        "purpose": "A dataset containing files used in configuration"
                    }
                }
            },
            "input_manifest": {
                "datasets": {
                    "met_mast_data": {
                        "purpose": "A dataset containing meteorological mast data"
                    },
                    "scada_data": {
                        "purpose": "A dataset containing scada data"
                    }
                }
            },
            "output_manifest": {
                "datasets": {
                    "output_files_data": {
                        "purpose": "A dataset containing output results"
                    }
                }
            }
        }
    """

    def test_missing_manifest_files(self):
        """Ensures that if you try to read values from missing files, the right exceptions get raised"""
        twine = Twine(source=self.VALID_MANIFEST_STRAND)
        file = os.path.join(self.path, "not_a_file.json")

        with self.assertRaises(exceptions.ConfigurationManifestFileNotFound):
            twine.validate_configuration_manifest(source=file)

        with self.assertRaises(exceptions.InputManifestFileNotFound):
            twine.validate_input_manifest(source=file)

        with self.assertRaises(exceptions.OutputManifestFileNotFound):
            twine.validate_output_manifest(source=file)

    def test_error_raised_if_datasets_are_missing_from_manifest(self):
        """Test that an error is raised if a dataset is missing from a manifest."""
        twine = """
            {
                "input_manifest": {
                    "datasets": {
                        "cat": {
                            "purpose": "blah"
                        },
                        "dog": {
                            "purpose": "blah"
                        }
                    }
                }
            }
        """

        input_manifest = {
            "id": "30d2c75c-a7b9-4f16-8627-9c8d5cc04bf4",
            "datasets": {"my-dataset": "gs://my-bucket/my_dataset", "dog": "gs://dog-house/dog"},
        }

        twine = Twine(source=twine)

        with self.assertRaises(exceptions.InvalidManifestContents) as context:
            twine.validate_input_manifest(source=input_manifest)

        self.assertEqual(
            context.exception.message,
            "A dataset named 'cat' is expected in the input_manifest but is missing.",
        )

    def test_missing_optional_datasets_do_not_raise_error(self):
        """Test that optional datasets specified in the twine missing from the manifest don't raise an error."""
        twine = """
            {
                "input_manifest": {
                    "datasets": {
                        "cat": {
                            "purpose": "blah",
                            "optional": true
                        },
                        "dog": {
                            "purpose": "blah"
                        }
                    }
                }
            }
        """

        input_manifest = {
            "id": "30d2c75c-a7b9-4f16-8627-9c8d5cc04bf4",
            "datasets": {"dog": "gs://dog-house/dog"},
        }

        Twine(source=twine).validate_input_manifest(source=input_manifest)

    def test_valid_manifest_files(self):
        """Ensures that a manifest file will validate."""
        valid_configuration_manifest = """
            {
                "id": "3ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": {
                    "configuration_files_data": {
                        "id": "34ad7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "configuration_files_data",
                        "tags": {},
                        "labels": ["the", "config", "labels"],
                        "files": [
                            {
                                "path": "configuration/datasets/7ead7669/file_1.csv",
                                "tags": {},
                                "labels": [],
                                "timestamp": 0,
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86"
                            },
                            {
                                "path": "configuration/datasets/7ead7669/file_2.csv",
                                "tags": {},
                                "labels": [],
                                "timestamp": 0,
                                "id": "bbff07bc-7c19-4ed5-be6d-a6546eae8e45"
                            }
                        ]
                    }
                }
            }
        """

        valid_input_manifest = """
            {
                "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": {
                    "met_mast_data": {
                        "id": "7ead7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "met_mast_data",
                        "tags": {},
                        "labels": ["met", "mast", "wind"],
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_1.csv",
                                "tags": {},
                                "labels": [],
                                "timestamp": 0,
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86"
                            },
                            {
                                "path": "input/datasets/7ead7669/file_2.csv",
                                "tags": {},
                                "labels": [],
                                "timestamp": 0,
                                "id": "bbff07bc-7c19-4ed5-be6d-a6546eae8e45"
                            }
                        ]
                    },
                    "scada_data": "gs://my-bucket/scada-data"
                }
            }
        """

        valid_output_manifest = """
            {
                "id": "2ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": {
                    "output_files_data": {
                        "id": "1ead7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "output_files_data",
                        "tags": {},
                        "labels": ["the", "output", "labels"],
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_1.csv",
                                "tags": {},
                                "labels": [],
                                "timestamp": 0,
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86"
                            },
                            {
                                "path": "input/datasets/7ead7669/file_2.csv",
                                "tags": {},
                                "labels": [],
                                "timestamp": 0,
                                "id": "bbff07bc-7c19-4ed5-be6d-a6546eae8e45"
                            }
                        ]
                    }
                }
            }
        """

        twine = Twine(source=self.VALID_MANIFEST_STRAND)
        twine.validate_configuration_manifest(source=valid_configuration_manifest)
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

    def test_error_raised_if_multiple_datasets_have_same_name(self):
        """Test that an error is raised if the input manifest has more than one dataset with the same name."""
        twine = """
            {
                "input_manifest": {
                    "datasets": {
                        "met_mast_data": {
                            "purpose": "A dataset containing meteorological mast data"
                        }
                    }
                }
            }
        """

        input_manifest = """
            {
                "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": {
                    "met_mast_data": {
                        "id": "7ead7669-8162-4f64-8cd5-4abe92509e19",
                        "name": "met_mast_data",
                        "tags": {},
                        "labels": [],
                        "files": []
                    },
                    "met_mast_data": {
                        "id": "7ead7669-8162-4f64-8cd5-4abe92509e18",
                        "name": "met_mast_data",
                        "tags": {},
                        "labels": [],
                        "files": []
                    }
                }
            }
        """

        twine = Twine(source=twine)

        with self.assertRaises(KeyError):
            twine.validate_input_manifest(source=input_manifest)
