"""Modul to manipulate strings."""
import string


def sanatize(value: str) -> str:
    """Sanatize a given `value` that there are only ascii, digits,

    space, dash and underscore allowed"""
    return "".join(
        char
        for char in value
        if char
        in iter(
            string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits
            + " "
            + "-"
            + "_"
        )
    ).strip()


def new_sanatize(value: str) -> str:
    invalid = (
        "~",
        '"',
        "#",
        "%",
        "&",
        "*",
        ":",
        "<",
        ">",
        "?",
        "/",
        "\\",
        "{",
        "|",
        "}",
    )
    return "".join(char for char in value if char not in invalid).strip()
