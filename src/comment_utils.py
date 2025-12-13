import textwrap


def normalize_docstring(text: str) -> list[str]:
    """
    Return logical docstring lines without quotes and indentation.
    """
    text = text.strip()
    if text.startswith(('"""', "'''")):
        text = text[3:]
    if text.endswith(('"""', "'''")):
        text = text[:-3]

    text = textwrap.dedent(text)

    lines = [line for line in text.splitlines()]
    return lines


def normalize_inline(text: str) -> str:
    """
    Remove the comment marker (#) and leading whitespace from an inline comment.

    Args:
        text (str): The raw inline comment string (e.g., "# My comment").

    Returns:
        str: The normalized comment text (e.g., "My comment").
    """
    text = text.lstrip()

    if text.startswith("#"):
        text = text[1:]

    text = text.lstrip()

    return text
