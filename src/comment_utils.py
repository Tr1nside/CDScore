from pathlib import Path

from src.data_types import LanguagesEnum


def parse_language(filepath: Path) -> LanguagesEnum:
    """
    Parse the programming language from the file extension.

    Args:
        filepath (pathlib.Path): The path to the file.

    Returns:
        LanguagesEnum: The detected programming language. Defaults to PYTHON.
    """
    suffix_language: dict[str, LanguagesEnum] = {".py": LanguagesEnum.PYTHON}

    suffix = filepath.suffix
    return suffix_language.get(suffix, LanguagesEnum.PYTHON)
