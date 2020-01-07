import unittest
from twined import Twine


class TestTwineSchema(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_twine_with_filename(self):
        """ Ensures that the simple app schema can be loaded and used to parse some basic config and values data
        """
        twine_file = 'data/simple_app/twine.json'
        twine = Twine(twine_file)

    def test_empty_twine(self):
        """ Ensures that an empty twine can be loaded
        """
        twine_file = 'data/empty_app/twine.json'
        twine = Twine(twine_file)

    def test_example_twine(self):
        """ Ensures that the example (full) twine can be loaded
        """
        twine_file = 'data/example_app/twine.json'
        twine = Twine(twine_file)

    def test_twine_simple_configuration(self):
        """ Ensures that the simple app schema can be loaded and used to parse some basic config and values data
        """

        twine_file = 'data/simple_app/twine.json'
        twine = Twine(twine_file)


class TestConfiguration(unittest.TestCase):

    def test_configuration(self):
        """
        """
        twine_file = 'data/simple_app/twine.json'
        twine = Twine(twine_file)


class TestCredentials(unittest.TestCase):

    def test_empty_credentials(self):
        """ Test that a twine with no credentials will end up with empty credentials object
        """

    def test_valid_credentials_in_twine(self):
        """ Test that where credentials in environment and twine match, that they import successfully and that no extra
        credentials are imported
        """

    def test_exception_on_invalid_credentials(self):
        """ Test that where a credential is specified in the twine that does not appear in the environment,
        an exception is raised
        """
        pass


if __name__ == '__main__':
    unittest.main()
