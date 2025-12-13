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

    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return lines
