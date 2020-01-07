

class TwineException(Exception):
    """ All exceptions raised by the twine framework inherits from TwineException"""


class InvalidTwine(TwineException):
    """ Raised when the specified twine is invalid
    """


class MissingTwine(TwineException):
    """ Raised when the specified twine file is not present
    """


class InvalidInput(TwineException):
    """ Raised when an object is instantiated or a function called with invalid inputs
    """


class FolderNotPresent(InvalidInput):
    """ Raised when a required folder (e.g. <data_dir>/input) cannot be found
    """


class ManifestNotFound(InvalidInput):
    """ Raised when a multi manifest can not be refined to a single manifest in a search
    """


class InvalidManifest(InvalidInput):
    """ Raised when a manifest loaded from JSON does not pass validation
    """


class InvalidManifestType(InvalidManifest):
    """ Raised when user attempts to create a manifest of a type other than 'input', 'output' or 'build'
    """


class NotImplementedYet(TwineException):
    """ Raised when you attempt to use a function whose high-level API is in place, but which is not implemented yet
    """


class UnexpectedNumberOfResults(TwineException):
    """ Raise when searching for a single data file (or a particular number of data files) and the number of results exceeds that expected
    """
