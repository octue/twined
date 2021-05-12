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

    def __call__(self, value):
        """Convert "true" to `True`, "false" to `False`, and anything else to `bool(value)`

        :return bool:
        """
        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        return bool(value)
