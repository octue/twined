import os

from twined import MANIFEST_STRANDS, Twine, exceptions
from .base import BaseTestCase


class TestTwine(BaseTestCase):
    """Testing operation of the Twine class"""

    def test_init_twine_with_filename(self):
        """Ensures that the twine class can be instantiated with a file"""
        Twine(source=os.path.join(self.path, "apps", "simple_app", "twine.json"))

    def test_init_twine_with_json(self):
        """Ensures that a twine can be instantiated with a json string"""
        with open(os.path.join(self.path, "apps", "simple_app", "twine.json"), "r", encoding="utf-8") as f:
            Twine(source=f.read())

    def test_no_twine(self):
        """Tests that the canonical-but-useless case of no twine provided validates empty"""
        Twine()

    def test_incorrect_version_twine(self):
        """Ensures exception is thrown on mismatch between installed and specified versions of twined"""
        incorrect_version_twine = """{"twined_version": "0.0.0"}"""
        with self.assertRaises(exceptions.TwineVersionConflict):
            Twine(source=incorrect_version_twine)

    def test_empty_twine(self):
        """Ensures that an empty twine file can be loaded"""
        with self.assertLogs(level="DEBUG") as log:
            Twine(source="{}")
            self.assertEqual(len(log.output), 3)
            self.assertEqual(len(log.records), 3)
            self.assertIn("Detected source", log.output[0])
            self.assertIn("Validated", log.output[1])

    def test_example_twine(self):
        """Ensures that the example (full) twine can be loaded and validated"""
        Twine(source=os.path.join(self.path, "apps", "example_app", "twine.json"))

    def test_simple_twine(self):
        """Ensures that the simple app schema can be loaded and used to parse some basic config and values data"""
        Twine(source=os.path.join(self.path, "apps", "simple_app", "twine.json"))

    def test_broken_json_twine(self):
        """Ensures that an invalid json file raises an InvalidTwine exception"""
        invalid_json_twine = """
            {
                "children": [
                "configuration_values_schema": {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "title": "The example configuration form",
                    "description": "The configuration strand of an example twine",
                    "type": "object",
                    "properties": {
                    }
                },
            }
        """

        with self.assertRaises(exceptions.InvalidTwineJson):
            Twine(source=invalid_json_twine)

    def test_available_strands_properties(self):
        """Test that the `available_strands` and `available_manifest_strands` properties work correctly."""
        twine = """
            {
                "configuration_values_schema": {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
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
                },
                "input_values_schema": {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "title": "Input Values",
                    "description": "The input values strand of an example twine, with a required height value",
                    "type": "object",
                    "properties": {
                        "height": {
                            "description": "An example of an integer value called 'height'",
                            "type": "integer",
                            "minimum": 2
                        }
                    },
                    "required": ["height"]
                },
                "output_values_schema": {
                    "title": "Output Values",
                    "description": "The output values strand of an example twine",
                    "type": "object",
                    "properties": {
                        "width": {
                            "description": "An example of an integer value called 'result'",
                            "type": "integer",
                            "minimum": 2
                        }
                    }
                },
                "output_manifest": {
                    "datasets": {
                        "my-dataset": {}
                    }
                }
            }
        """

        twine = Twine(source=twine)

        self.assertEqual(
            twine.available_strands,
            {"configuration_values", "input_values", "output_values", "output_manifest"},
        )

        self.assertEqual(twine.available_manifest_strands, {"output_manifest"})

    def test_deprecation_warning_issued_if_datasets_not_given_as_dictionary_in_manifest_strands(self):
        """Test that, if datasets are given as a list in the manifest strands, a deprecation warning is issued and the
        list (the old form) is converted to a dictionary (the new form).
        """
        for manifest_strand in MANIFEST_STRANDS:
            with self.subTest(manifest_strand=manifest_strand):
                invalid_twine = (
                    """
                {
                    "%s": {
                        "datasets": [
                            {
                                "key": "met_mast_data",
                                "purpose": "A dataset containing meteorological mast data"
                            }
                        ]
                    }
                }
                """
                    % manifest_strand
                )

                with self.assertWarns(DeprecationWarning):
                    twine = Twine(source=invalid_twine)

                self.assertEqual(
                    getattr(twine, manifest_strand)["datasets"],
                    {
                        "met_mast_data": {
                            "key": "met_mast_data",
                            "purpose": "A dataset containing meteorological mast data",
                        }
                    },
                )
