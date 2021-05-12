def trim_suffix(text, suffix):
    """Strip a suffix from text, if it appears (otherwise return text unchanged)"""
    if not text.endswith(suffix):
        return text
    return text[: len(text) - len(suffix)]


class ConvertStringRepresentedBooleanToBooleanType:
    """An extension of `bool` that, when called, converts string-represented booleans to the `bool` type rather than
    converting all non-empty strings to `True`.
    """

    def __repr__(self):
        return repr(bool)

    def __name__(self):
        return "bool"

    def __call__(self, value):
        """Convert "true" to `True`, "false" to `False`, and anything else to `bool(value)`

        :raise TypeError: if the value given isn't the string "true" or "false"
        :return bool:
        """
        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        raise TypeError(f"Could not convert {value!r} to a boolean.")
