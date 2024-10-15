from twined import Twine, exceptions

from .base import BaseTestCase


class TestMonitorMessageTwine(BaseTestCase):
    STRAND_WITH_MONITOR_MESSAGE_SCHEMA = """
        {
            "monitor_message_schema": {
                "type": "object",
                "properties": {
                    "my_property": {
                        "type": "number"
                    }
                },
                "required": ["my_property"]
            }
        }
    """

    def test_validate_monitor_message_raises_error_if_monitor_message_schema_not_met(self):
        """Test that an error is raised if an invalid monitor update is validated."""
        twine = Twine(source=self.STRAND_WITH_MONITOR_MESSAGE_SCHEMA)

        with self.assertRaises(exceptions.InvalidValuesContents):
            twine.validate_monitor_message([])

    def test_validate_monitor_message_with_valid_monitor_update(self):
        """Test that a valid monitor update validates successfully."""
        twine = Twine(source=self.STRAND_WITH_MONITOR_MESSAGE_SCHEMA)
        twine.validate_monitor_message({"my_property": 3.7})
