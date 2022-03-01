from jsonschema import ValidationError


class TwineException(Exception):
    """All exceptions raised by the twine framework inherit from TwineException"""


class NotImplementedYet(TwineException):
    """Raised when you attempt to use a function whose high-level API is in place, but which is not implemented yet"""


class TwineValueException(TwineException, ValueError):
    """Raised when a python ValueError is appropriate to ensure all errors still also inherit from TwineException"""


class TwineTypeException(TwineException, TypeError):
    """Raised when a python TypeError is appropriate to ensure all errors still also inherit from TwineException"""


class TwineVersionConflict(TwineException):
    """Raised when the (optional) "twined_version" field in the twine file does not match the current installed version of twined"""


# --------------------- Exceptions relating to the twine itself ------------------------


class InvalidTwine(TwineException):
    """Raised when the specified twine is invalid for some reason"""


class InvalidTwineJson(InvalidTwine):
    """Raised when the JSON in the twine file is broken"""


class InvalidTwineContents(InvalidTwine, ValidationError):
    """Raised when the JSON in the twine file is not valid (eg doesn't match twine schema)"""


# --------------------- Exceptions relating to accessing/setting strands ------------------------


class UnknownStrand(TwineException, ValueError):
    """Raised when referencing a strand which is not defined in ALL_STRANDS"""


class StrandNotFound(TwineException, KeyError):
    """Raised when the attempting to access a strand not present in the twine"""


# --------------------- Exceptions relating to missing files/folders ------------------------


class FolderNotFound(TwineException):
    """Raised when a required folder (e.g. <data_dir>/input) cannot be found"""


class CredentialNotFound(TwineException):
    """Raised when a credential specified in the twine file is not present in either the environment or a .env file"""


class TwineFileNotFound(TwineException, FileNotFoundError):
    """Raised when the specified twine file is not present"""


class ConfigurationValuesFileNotFound(TwineException, FileNotFoundError):
    """Raised when attempting to read configuration values from a file that is missing"""


class ConfigurationManifestFileNotFound(TwineException, FileNotFoundError):
    """Raised when a configuration manifest file is required by a twine, but is not present in the input directory"""


class InputManifestFileNotFound(TwineException, FileNotFoundError):
    """Raised when an input manifest file is required by a twine, but is not present in the input directory"""


class InputValuesFileNotFound(TwineException, FileNotFoundError):
    """Raised when attempting to read input values from a file that is missing"""


class OutputManifestFileNotFound(TwineException, FileNotFoundError):
    """Raised when twined checks that output manifest file has been produced, but it is not present in the output directory"""


class OutputValuesFileNotFound(TwineException, FileNotFoundError):
    """Raised when attempting to read output values from a file that is missing"""


# --------------------- Exceptions relating to validation of JSON data (input, output, config values) ------------------


class InvalidSourceKindException(TwineException):
    """Raised when attempting to use the json loader for a disallowed kind"""


class InvalidValues(TwineException):
    """Raised when JSON data (like Config data, Input Values or Output Values) is invalid"""


class InvalidValuesJson(InvalidValues):
    """Raised when the JSON in the file or string is broken so cannot be parsed"""


class InvalidValuesContents(InvalidValues, ValidationError):
    """Raised when the JSON in the file is not valid according to its matching schema."""


# --------------------- Exceptions relating to validation of manifests ------------------------


class InvalidManifest(TwineException):
    """Raised when a manifest loaded from JSON does not pass validation"""


class InvalidManifestJson(InvalidManifest):
    """Raised when the json in the manifest file is broken"""


class InvalidManifestType(InvalidManifest):
    """Raised when user attempts to create a manifest of an invalid type"""


class InvalidManifestContents(InvalidManifest, ValidationError):
    """Raised when the manifest files are missing or do not match tags, sequences, clusters, extensions etc as required"""


# --------------------- Exceptions relating to access of data using the Twine instance ------------------------

# TODO This is related to filtering files from a manifest. Determine whether this belongs here,
#  or whether we should port the filtering code across from the SDK.
class UnexpectedNumberOfResults(TwineException):
    """Raise when searching for a single data file (or a particular number of data files) and the number of results exceeds that expected"""


# --------------------- Maps allowing customised exceptions per-strand (simplifies code elsewhere) ------------------


file_not_found_map = {
    "twine": TwineFileNotFound,
    "configuration_values": ConfigurationValuesFileNotFound,
    "input_values": InputValuesFileNotFound,
    "output_values": OutputValuesFileNotFound,
    "configuration_manifest": ConfigurationManifestFileNotFound,
    "input_manifest": InputManifestFileNotFound,
    "output_manifest": OutputManifestFileNotFound,
}

# TODO Specialised per-strand exceptions to help drill to the root of the issues
invalid_json_map = {
    "twine": InvalidTwineJson,
    "children": InvalidValuesJson,
    "configuration_values": InvalidValuesJson,
    "input_values": InvalidValuesJson,
    "output_values": InvalidValuesJson,
    "monitor_message": InvalidValuesJson,
    "configuration_manifest": InvalidManifestJson,
    "input_manifest": InvalidManifestJson,
    "output_manifest": InvalidManifestJson,
}

# TODO Specialised per-strand exceptions to help drill to the root of the issues
invalid_contents_map = {
    "twine": InvalidTwineContents,
    "children": InvalidValuesContents,
    "configuration_values": InvalidValuesContents,
    "input_values": InvalidValuesContents,
    "output_values": InvalidValuesContents,
    "monitor_message": InvalidValuesContents,
    "configuration_manifest": InvalidManifestContents,
    "input_manifest": InvalidManifestContents,
    "output_manifest": InvalidManifestContents,
}
