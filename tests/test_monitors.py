from twined import Twine, exceptions
from .base import BaseTestCase


class TestMonitorsTwine(BaseTestCase):
    STRAND_WITH_MONITORS_SCHEMA = """
        {
            "monitors": {
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

    def test_validate_monitors_raises_error_if_monitors_schema_not_met(self):
        """Test that an error is raised if an invalid monitor update is validated."""
        twine = Twine(source=self.STRAND_WITH_MONITORS_SCHEMA)

        with self.assertRaises(exceptions.InvalidMonitorsUpdate):
            twine.validate_monitor_update([])

    def test_validate_monitors_with_valid_monitor_update(self):
        """Test that a valid monitor update validates successfully."""
        twine = Twine(source=self.STRAND_WITH_MONITORS_SCHEMA)
        twine.validate_monitor_update({"my_property": 3.7})
