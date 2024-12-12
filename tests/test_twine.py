import os

from twined import Twine, exceptions

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

    def test_required_strands_property(self):
        """Test that the required strands property is correct."""
        twines = [
            {
                "configuration_values_schema": {},
                "input_values_schema": {},
                "output_values_schema": {},
                "output_manifest": {"datasets": {}},
            },
            {
                "configuration_values_schema": {"optional": True},
                "input_values_schema": {},
                "output_values_schema": {},
                "output_manifest": {"datasets": {}, "optional": True},
            },
            {
                "configuration_values_schema": {"optional": False},
                "input_values_schema": {},
                "output_values_schema": {},
                "output_manifest": {"datasets": {}, "optional": False},
            },
        ]

        expected_required_strands = [
            {"configuration_values", "input_values", "output_values", "output_manifest"},
            {"input_values", "output_values"},
            {"configuration_values", "input_values", "output_values", "output_manifest"},
        ]

        for twine, expected in zip(twines, expected_required_strands):
            with self.subTest(twine=twine):
                twine = Twine(source=twine)
                self.assertEqual(twine.required_strands, expected)
