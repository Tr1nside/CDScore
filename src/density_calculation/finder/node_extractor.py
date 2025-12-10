from collections.abc import Callable
from pathlib import Path

import tree_sitter
from loguru import logger

from src.data_types import CommentData, CommentScope

captures_type = dict[str, list[tree_sitter.Node]]


class NodeDataExtractor:
    def __init__(self) -> None:
        self.callback_found_comment: Callable[[CommentData], None] | None = None

    def connect_action(self, action: Callable[[CommentData], None]) -> None:
        self.callback_found_comment = action

    def extract(self, filepath: Path, code_bytes: bytes, captures: captures_type) -> None:
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
        Определяет область видимости (scope) для узла, поднимаясь по AST.
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
        comment_text = code_bytes[node.start_byte : node.end_byte].decode("utf-8")

        start_row, start_col = node.start_point
        end_row, end_col = node.end_point

        return CommentData(
            file_path=filepath,
            start_line_number=start_row + 1,
            end_line_number=end_row + 1,
            column_start=start_col + 1,
            column_end=end_col,
            text=comment_text,
            comment_type=node.type,
            scope=self._get_node_scope(node),
        )
