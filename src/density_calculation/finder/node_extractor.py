"""
Define a class for extracting data from Tree-sitter nodes and comments.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from collections.abc import Callable
from pathlib import Path

import tree_sitter
from loguru import logger

from src.data_types import CommentData, CommentScope, CommentType

captures_type = dict[str, list[tree_sitter.Node]]


class NodeDataExtractor:
    """
    Extract data about found comment nodes and notify a callback action.
    """

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
                comment_data = self._comment_data_generation(node, code_bytes, filepath)

                if self.callback_found_comment:
                    self.callback_found_comment(comment_data)
        else:
            logger.error("Not find 'item' in captures from '{}'", filepath.name)

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
        """
        comment_text = code_bytes[node.start_byte : node.end_byte].decode("utf-8")

        start = node.start_point
        end = node.end_point

        comment_type = CommentType.INLINE if node.type == "comment" else CommentType.DOCSTRING

        return CommentData(
            file_path=filepath,
            start_line_number=start[0] + 1,
            end_line_number=end[0] + 1,
            column_start=start[1] + 1,
            column_end=end[1],
            text=comment_text,
            comment_type=comment_type,
            scope=self._get_node_scope(node),
        )
