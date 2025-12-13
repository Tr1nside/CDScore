"""
Find comments in files and directories recursively.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from collections.abc import Callable
from pathlib import Path

from loguru import logger

from src.comment_utils import parse_language
from src.data_types import CommentData
from src.density_calculation.finder.node_extractor import NodeDataExtractor
from src.density_calculation.finder.syntax_analyzer import SyntaxAnalyzer


class CommentFinder:
    """
    Provide methods for recursively finding comments in files and directories
    using a syntax analyzer and node extractor.
    """

    def __init__(self) -> None:
        """Initialize the comment finder."""
        self.syntax_analyzer = SyntaxAnalyzer()
        self.node_extractor = NodeDataExtractor()

    def connect_check_action(self, check_action: Callable[[CommentData], None]) -> None:
        """
        Connect a callback function to the node extractor.

        Args:
            check_action (Callable[[CommentData], None]): The function to call
                for each found comment.
        """
        self.node_extractor.connect_action(check_action)

    def find(self, path: Path) -> None:
        """
        Recursively find comments in the given path (file or directory).

        Args:
            path (pathlib.Path): The path to the file or directory to search in.
        """
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
        """
        Find comments in a single file.

        Args:
            filepath (pathlib.Path): The path to the file.
        """
        logger.debug("Start find in '{}'", filepath.name)

        language = parse_language(filepath)
        with open(filepath, "rb") as file_for_check:
            code_bytes = file_for_check.read()

        tree = self.syntax_analyzer.parse(code_bytes, language)
        logger.debug("The tree was created")
        captures = self.syntax_analyzer.query_captures(tree, language)
        logger.debug("The captures were received")

        self.node_extractor.extract(filepath, code_bytes, captures)

    def _check_exist(self, path: Path) -> bool:
        """
        Check if the given path exists.

        Args:
            path (pathlib.Path): The path to check.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        if path.exists():
            logger.debug("'{}' exists.", path)
            return True
        else:
            logger.error("'{}' does not exist.", path)
            return False
