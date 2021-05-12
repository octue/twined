def trim_suffix(text, suffix):
    """Strip a suffix from text, if it appears (otherwise return text unchanged)"""
    if not text.endswith(suffix):
        return text
    return text[: len(text) - len(suffix)]


def convert_string_represented_boolean_to_boolean_type(value):
    """Convert "true" to `True`, "false" to `False`.

    :raise TypeError: if the value given isn't the string "true" or "false"
    :return bool:
    """
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    raise TypeError(f"Could not convert {value!r} to a boolean.")
