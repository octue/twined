import os
import unittest


class BaseTestCase(unittest.TestCase):
    """ Base test case for twined:
        - sets a path to the test data directory
    """

    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), "data")
        super().setUp()
