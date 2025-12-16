from pathlib import Path

from src.data_types import LanguagesEnum
from src.exceptions import FileTypeError


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
    language = suffix_language.get(suffix)
    if language:
        return language
    else:
        raise FileTypeError(f"Unknown type of file: {filepath.name}")
