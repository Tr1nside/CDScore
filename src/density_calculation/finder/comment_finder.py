from collections.abc import Callable
from pathlib import Path

from loguru import logger

from src.data_types import CommentData, LanguagesEnum
from src.density_calculation.finder.node_extractor import NodeDataExtractor
from src.density_calculation.finder.syntax_analyzer import SyntaxAnalyzer


class CommentFinder:
    def __init__(self) -> None:
        """Init comment finder"""
        self.syntax_analyzer = SyntaxAnalyzer()
        self.node_extractor = NodeDataExtractor()

    def connect_check_action(self, check_action: Callable[[CommentData], None]) -> None:
        self.node_extractor.connect_action(check_action)

    def find(self, path: Path) -> None:
        if self._check_exist(path):
            if path.is_dir():
                for dir_item in path.iterdir():
                    self.find(dir_item)
            elif path.is_file():
                self._find_in_file(path)
            else:
                logger.error("'{}' is not a file or folder", path)
        else:
            logger.error("Searching in '{}' is not possible.", path)

    def _find_in_file(self, filepath: Path) -> None:
        logger.debug("Start find in '{}'", filepath.name)

        language = self._parse_language(filepath)
        with open(filepath, "rb") as file_for_check:
            code_bytes = file_for_check.read()

        tree = self.syntax_analyzer.parse(code_bytes, language)
        logger.debug("The tree was created")
        captures = self.syntax_analyzer.query_captures(tree, language)
        logger.debug("The captures were received")

        self.node_extractor.extract(filepath, code_bytes, captures)

    def _parse_language(self, filepath: Path) -> LanguagesEnum:
        suffix_language: dict[str, LanguagesEnum] = {".py": LanguagesEnum.PYTHON}

        suffix = filepath.suffix
        return suffix_language.get(suffix, LanguagesEnum.PYTHON)

    def _check_exist(self, path: Path) -> bool:
        if path.exists():
            logger.debug("'{}' exists.", path)
            return True
        else:
            logger.error("'{}' does not exist.", path)
            return False
