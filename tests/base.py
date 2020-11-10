import os
import unittest


VALID_SCHEMA_TWINE = """
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
        },
        "input_values_schema": {
            "$schema": "http://json-schema.org/2019-09/schema#",
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
        }
    }
"""


class BaseTestCase(unittest.TestCase):
    """ Base test case for twined:
        - sets a path to the test data directory
    """

    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), "data")
        super().setUp()
