import io
import json
import logging

from twined.exceptions import InvalidSourceKindException


logger = logging.getLogger(__file__)


ALLOWED_KINDS = ("file-like", "filename", "string", "object")


def load_json(source, *args, **kwargs):
    """ Loads json, automatically detecting whether the input is a valid filename, a string containing json data,
    or a python dict already (in which case the result is returned directly).

    That makes this function suitable for use in a pipeline where it's not clear whether data has been loaded yet, or
    whether it's in a file or a raw string

    :parameter source: The data source, which can be a string filename ending in *.json (json loaded from disc to
    python dict), a file-like object, a string containing raw json data (json loaded from string to python dict), or
    any other valid python object (passed through).

    :parameter args, kwargs: Arguments passed through to json.load or json.loads, enabling use of custom encoders etc.
    """
    allowed_kinds = kwargs.pop("allowed_kinds", ALLOWED_KINDS)

    def check(kind):
        if kind not in allowed_kinds:
            raise InvalidSourceKindException(f"Attempted to load json from a {kind} data source")

    if isinstance(source, io.IOBase):
        logger.debug("Detected source is a file-like object, loading contents...")
        check("file-like")
        return json.load(source, *args, **kwargs)

    elif not isinstance(source, str):
        logger.debug("Source is not a string, bypassing (returning raw data)")
        check("object")
        return source

    elif source.endswith(".json"):
        logger.debug("Detected source is name of a *.json file, loading from %s", source)
        check("filename")
        with open(source) as f:
            return json.load(f, *args, **kwargs)

    else:
        logger.debug("Detected source is string containing json data, parsing...")
        check("string")
        return json.loads(source, *args, **kwargs)
