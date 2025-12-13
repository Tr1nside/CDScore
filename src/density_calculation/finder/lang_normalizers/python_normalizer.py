import textwrap

from src.density_calculation.finder.language_data import LanguageNormalizer


class PythonNormalizer(LanguageNormalizer):
    """Implementation of LanguageNormalizer for the Python language.

    This class provides Python-specific logic for cleaning up docstrings
    (removing quotes and indentation) and inline comments (removing the '#' marker).
    """

    def _normalize_docstring(self, text: str) -> list[str]:
        """Normalizes a Python docstring.

        Removes triple quotes (single or double), common indentation,
        and leading/trailing whitespace.

        Args:
            text (str): The raw docstring text.

        Returns:
            List[str]: A list of lines of the normalized docstring.
        """
        text = text.strip()
        if text.startswith(('"""', "'''")):
            text = text[3:]
        if text.endswith(('"""', "'''")):
            text = text[:-3]

        text = textwrap.dedent(text)

        lines = [line for line in text.splitlines() if len(line) > 0]
        return lines

    def _normalize_inline(self, text: str) -> list[str]:
        """Normalizes a Python inline comment.

        Removes the '#' marker and any surrounding leading whitespace.

        Args:
            text (str): The raw inline comment text (e.g., " # My comment").

        Returns:
            List[str]: A single-item list containing the normalized comment text.
        """
        text = text.lstrip()

        if text.startswith("#"):
            text = text[1:]

        text = text.lstrip()

        return [text]
