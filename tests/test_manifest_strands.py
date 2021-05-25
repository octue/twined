import os
import unittest

from twined import Twine, exceptions
from .base import BaseTestCase


class TestManifestStrands(BaseTestCase):
    """Testing operation of the Twine class for validation of data using strands which require manifests"""

    VALID_MANIFEST_STRAND = """
        {
            "configuration_manifest": {
                "datasets": [
                    {
                        "key": "configuration_files_data",
                        "purpose": "A dataset containing files used in configuration"
                    }
                ]
            },
            "input_manifest": {
                "datasets": [
                    {
                        "key": "met_mast_data",
                        "purpose": "A dataset containing meteorological mast data"
                    },
                    {
                        "key": "scada_data",
                        "purpose": "A dataset containing scada data"
                    }
                ]
            },
            "output_manifest": {
                "datasets": [
                    {
                        "key": "output_files_data",
                        "purpose": "A dataset containing output results"
                    }
                ]
            }
        }
    """

    TWINE_WITH_INPUT_MANIFEST_WITH_TAG_TEMPLATE = """
        {
            "input_manifest": {
                "datasets": [
                    {
                        "key": "met_mast_data",
                        "purpose": "A dataset containing meteorological mast data",
                        "file_tags_template": {
                            "type": "object",
                            "properties": {
                                "manufacturer": {
                                    "type": "string"
                                },
                                "height": {
                                    "type": "number"
                                },
                                "is_recycled": {
                                    "type": "boolean"
                                },
                                "number_of_blades": {
                                    "type": "number"
                                }
                            },
                            "required": [
                                "manufacturer",
                                "height",
                                "is_recycled",
                                "number_of_blades"
                            ]
                        }
                    }
                ]
            }
        }
    """

    INPUT_MANIFEST_WITH_CORRECT_FILE_TAGS = """
        {
            "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
            "datasets": [
                {
                    "id": "7ead7669-8162-4f64-8cd5-4abe92509e17",
                    "name": "met_mast_data",
                    "tags": {},
                    "labels": ["met", "mast", "wind"],
                    "files": [
                        {
                            "path": "input/datasets/7ead7669/file_1.csv",
                            "cluster": 0,
                            "sequence": 0,
                            "extension": "csv",
                            "labels": ["mykeyword1", "mykeyword2"],
                            "tags": {
                                "manufacturer": "vestas",
                                "height": 500,
                                "is_recycled": true,
                                "number_of_blades": 3
                            },
                            "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                            "name": "file_1.csv"
                        },
                        {
                            "path": "input/datasets/7ead7669/file_1.csv",
                            "cluster": 0,
                            "sequence": 1,
                            "extension": "csv",
                            "labels": [],
                            "tags": {
                                "manufacturer": "vestas",
                                "height": 500,
                                "is_recycled": true,
                                "number_of_blades": 3
                            },
                            "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                            "name": "file_1.csv"
                        }
                    ]
                }
            ]
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

    def test_valid_manifest_files(self):
        """Ensures that a manifest file will validate."""
        valid_configuration_manifest = """
            {
                "id": "3ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": [
                    {
                        "id": "34ad7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "configuration_files_data",
                        "tags": {},
                        "labels": ["the", "config", "labels"],
                        "files": [
                            {
                                "path": "configuration/datasets/7ead7669/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": {},
                                "labels": [],
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
                                "tags": {},
                                "labels": [],
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
                        "name": "met_mast_data",
                        "tags": {},
                        "labels": ["met", "mast", "wind"],
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": {},
                                "labels": [],
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
                                "tags": {},
                                "labels": [],
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
                        "name": "output_files_data",
                        "tags": {},
                        "labels": ["the", "output", "labels"],
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": {},
                                "labels": [],
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
                                "tags": {},
                                "labels": [],
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

    def test_error_raised_when_required_tags_missing_for_validate_input_manifest(self):
        """Test that an error is raised when required tags from the file tags template for a dataset are missing when
        validating the input manifest.
        """
        input_manifest = """
            {
                "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": [
                    {
                        "id": "7ead7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "met_mast_data",
                        "tags": {},
                        "labels": ["met", "mast", "wind"],
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": {},
                                "labels": [],
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                                "name": "file_1.csv"
                            }
                        ]
                    }
                ]
            }
        """

        twine = Twine(source=self.TWINE_WITH_INPUT_MANIFEST_WITH_TAG_TEMPLATE)

        with self.assertRaises(exceptions.InvalidManifestContents):
            twine.validate_input_manifest(source=input_manifest)

    def test_validate_input_manifest_raises_error_if_required_tags_are_not_of_required_type(self):
        """Test that an error is raised if the required tags from the file tags template for a dataset are present but
        are not of the required type when validating an input manifest.
        """
        input_manifest = """
            {
                "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": [
                    {
                        "id": "7ead7669-8162-4f64-8cd5-4abe92509e17",
                        "name": "met_mast_data",
                        "tags": {},
                        "labels": ["met", "mast", "wind"],
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": %s,
                                "labels": [],
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                                "name": "file_1.csv"
                            }
                        ]
                    }
                ]
            }
        """

        twine = Twine(source=self.TWINE_WITH_INPUT_MANIFEST_WITH_TAG_TEMPLATE)

        for tags in (
            '{"manufacturer": "Vestas", "height": 350, "is_recycled": false, "number_of_blades": "3"}',
            '{"manufacturer": "Vestas", "height": 350, "is_recycled": "no", "number_of_blades": 3}',
            '{"manufacturer": false, "height": 350, "is_recycled": "false", "number_of_blades": 3}',
        ):
            with self.assertRaises(exceptions.InvalidManifestContents):
                twine.validate_input_manifest(source=input_manifest % tags)

    def test_validate_input_manifest_with_required_tags(self):
        """Test that validating an input manifest with required tags from the file tags template for a dataset works
        for tags meeting the requirements.
        """
        twine = Twine(source=self.TWINE_WITH_INPUT_MANIFEST_WITH_TAG_TEMPLATE)
        twine.validate_input_manifest(source=self.INPUT_MANIFEST_WITH_CORRECT_FILE_TAGS)

    def test_validate_input_manifest_with_required_tags_for_remote_tag_template_schema(self):
        """Test that a remote tag template can be used for validating tags on the datafiles in a manifest. """
        twine_with_input_manifest_with_remote_tag_template = """
            {
                "input_manifest": {
                    "datasets": [
                        {
                            "key": "met_mast_data",
                            "purpose": "A dataset containing meteorological mast data",
                            "file_tags_template": {
                                "$ref": "https://refs.schema.octue.com/octue/my-file-type-tag-template/0.0.0.json"
                            }
                        }
                    ]
                }
            }
        """

        twine = Twine(source=twine_with_input_manifest_with_remote_tag_template)
        twine.validate_input_manifest(source=self.INPUT_MANIFEST_WITH_CORRECT_FILE_TAGS)

    def test_validate_input_manifest_with_required_tags_in_several_datasets(self):
        """Test that required tags from the file tags template are validated separately and correctly for each dataset."""
        TWINE_WITH_INPUT_MANIFEST_WITH_REQUIRED_TAGS_FOR_MULTIPLE_DATASETS = """
            {
                "input_manifest": {
                    "datasets": [
                        {
                            "key": "first_dataset",
                            "purpose": "A dataset containing meteorological mast data",
                            "file_tags_template": {
                                "type": "object",
                                "properties": {
                                    "manufacturer": {
                                        "type": "string"
                                    },
                                    "height": {
                                        "type": "number"
                                    }
                                }
                            }
                        },
                        {
                            "key": "second_dataset",
                            "file_tags_template": {
                                "type": "object",
                                "properties": {
                                    "is_recycled": {
                                        "type": "boolean"
                                    },
                                    "number_of_blades": {
                                        "type": "number"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        """

        input_manifest = """
            {
                "id": "8ead7669-8162-4f64-8cd5-4abe92509e17",
                "datasets": [
                    {
                        "id": "7ead7669-8162-4f64-8cd5-4abe92509e19",
                        "name": "first_dataset",
                        "tags": {},
                        "labels": [],
                        "files": [
                            {
                                "path": "input/datasets/7ead7669/file_0.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": {
                                    "manufacturer": "Vestas",
                                    "height": 503.7
                                },
                                "labels": [],
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e86",
                                "name": "file_0.csv"
                            }
                        ]
                    },
                    {
                        "id": "7ead7669-8162-4f64-8cd5-4abe92509e18",
                        "name": "second_dataset",
                        "tags": {},
                        "labels": [],
                        "files": [
                            {
                                "path": "input/datasets/blah/file_1.csv",
                                "cluster": 0,
                                "sequence": 0,
                                "extension": "csv",
                                "tags": {
                                    "is_recycled": true,
                                    "number_of_blades": 3
                                },
                                "labels": [],
                                "id": "abff07bc-7c19-4ed5-be6d-a6546eae8e82",
                                "name": "file_1.csv"
                            }
                        ]
                    }
                ]
            }
        """

        twine = Twine(source=TWINE_WITH_INPUT_MANIFEST_WITH_REQUIRED_TAGS_FOR_MULTIPLE_DATASETS)
        twine.validate_input_manifest(source=input_manifest)


if __name__ == "__main__":
    unittest.main()
