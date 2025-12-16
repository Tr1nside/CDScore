"""
Define a class for extracting data from Tree-sitter nodes and comments.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from collections.abc import Callable
from pathlib import Path

import tree_sitter
from loguru import logger

from src.comment_utils import parse_language
from src.data_types import CommentData, CommentScope, CommentType, LanguagesEnum
from src.density_calculation.finder.lang_normalizers.python_normalizer import PythonNormalizer
from src.density_calculation.finder.language_data import LanguageNormalizer
from src.exceptions import CommentTypeError

INLINE_NODE_TYPES = ("comment", "line_comment", "block_comment")
DOCSTRING_NODE_TYPES = ("string", "string_literal")

captures_type = dict[str, list[tree_sitter.Node]]


class NodeDataExtractor:
    """
    Extract data about found comment nodes and notify a callback action.
    """

    normalizers: dict[LanguagesEnum, type[LanguageNormalizer]] = {LanguagesEnum.PYTHON: PythonNormalizer}

    def __init__(self) -> None:
        """Initialize the extractor with no action connected."""
        self.callback_found_comment: Callable[[CommentData], None] | None = None

    def connect_action(self, action: Callable[[CommentData], None]) -> None:
        """
        Connect a callback function to be executed when a comment is found.

        Args:
            action (Callable[[CommentData], None]): The function to call
                for each found comment node data.
        """
        self.callback_found_comment = action

    def extract(self, filepath: Path, code_bytes: bytes, captures: captures_type) -> None:
        """
        Extract data from the captured nodes and execute the connected action.

        Args:
            filepath (pathlib.Path): The path to the file being processed.
            code_bytes (bytes): The byte content of the code file.
            captures (dict[str, list[tree_sitter.Node]]): The result of the Tree-sitter query
                containing captured nodes.
        """
        if "item" in captures:
            logger.debug("Start find comment in '{}'", filepath.name)
            unique_nodes = set(captures.get("item", []))

            for node in unique_nodes:
                try:
                    comment_data = self._comment_data_generation(node, code_bytes, filepath)
                except CommentTypeError as error:
                    logger.error(error)
                    continue
                if self.callback_found_comment:
                    self.callback_found_comment(comment_data)
        else:
            logger.debug("Not find comment in '{}'", filepath.name)

    def _get_node_scope(self, node: tree_sitter.Node) -> CommentScope:
        """
        Determine the scope of the node by traversing up the Abstract Syntax Tree (AST).

        Args:
            node (tree_sitter.Node): The starting node (the comment node).

        Returns:
            CommentScope: The detected scope (FUNCTION, CLASS, MODULE, or UNKNOWN).
        """
        current_node = node
        while current_node is not None:
            node_type = current_node.type
            if node_type == "function_definition":
                return CommentScope.FUNCTION
            if node_type == "class_definition":
                return CommentScope.CLASS
            if node_type == "module":
                return CommentScope.MODULE
            current_node = current_node.parent
        return CommentScope.UNKNOWN

    def _comment_data_generation(self, node: tree_sitter.Node, code_bytes: bytes, filepath: Path) -> CommentData:
        """
        Generate a CommentData object from a Tree-sitter node.

        Args:
            node (tree_sitter.Node): The Tree-sitter node corresponding to the comment.
            code_bytes (bytes): The byte content of the file.
            filepath (pathlib.Path): The path to the file.

        Returns:
            CommentData: The data object containing details about the comment.

        Raises:
            CommentTypeError: If node type is unknow
        """
        start = node.start_point
        end = node.end_point

        comment_type = self._get_comment_type(node.type)

        if comment_type:
            return CommentData(
                file_path=filepath,
                start_line_number=start[0] + 1,
                end_line_number=end[0] + 1,
                column_start=start[1] + 1,
                column_end=end[1],
                text=self._get_comment_text(node, code_bytes, filepath, comment_type),
                comment_type=comment_type,
                scope=self._get_node_scope(node),
            )
        else:
            raise CommentTypeError()

    def _get_comment_type(self, node_type: str) -> CommentType | None:
        if node_type in INLINE_NODE_TYPES:
            return CommentType.INLINE
        elif node_type in DOCSTRING_NODE_TYPES:
            return CommentType.DOCSTRING

        return None

    def _get_comment_text(
        self, node: tree_sitter.Node, code_bytes: bytes, filepath: Path, comment_type: CommentType
    ) -> list[str]:
        language = parse_language(filepath)
        comment_text = code_bytes[node.start_byte : node.end_byte].decode("utf-8")

        normalizer = self.normalizers.get(language)
        if normalizer:
            normalized_lines = normalizer().normalize(comment_text, comment_type)
            return normalized_lines

        else:
            raise TypeError("Normalizer not found")
