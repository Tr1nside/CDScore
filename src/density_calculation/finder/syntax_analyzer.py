"""
Module for code syntax analysis using the tree-sitter library.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

import tree_sitter

from src.data_types import LanguagesEnum
from src.density_calculation.finder.language_data import LanguageData
from src.density_calculation.finder.languages_formats import PythonData
from src.exceptions import FileTypeError


class SyntaxAnalyzer:
    """
    Perform syntax analysis and queries on the syntax tree.

    Analyzes code bytes and builds the AST using tree-sitter.
    """

    query_patterns: dict[LanguagesEnum, type[LanguageData]] = {LanguagesEnum.PYTHON: PythonData}

    def parse(self, code_bytes: bytes, language: LanguagesEnum) -> tree_sitter.Tree:
        """
        Perform syntax analysis of code bytes for the given language.

        Args:
            code_bytes (bytes): Code as bytes for analysis.
            language (LanguagesEnum): Programming language of the code.

        Returns:
            tree_sitter.Tree: The generated Abstract Syntax Tree (AST).
        """
        language_data = self.query_patterns.get(language)
        if language_data:
            language_object = tree_sitter.Language(language_data.tree_sitter_language)
            parser = tree_sitter.Parser(language_object)
            tree = parser.parse(code_bytes)

            return tree
        else:
            raise FileTypeError()

    def query_captures(self, tree: tree_sitter.Tree, language: LanguagesEnum) -> dict[str, list[tree_sitter.Node]]:
        """
        Execute a tree-sitter query and get the captured nodes.

        Args:
            tree (tree_sitter.Tree): The syntax tree to execute the query on.
            language (LanguagesEnum): The programming language for which to get the query.

        Returns:
            dict[str, list[tree_sitter.Node]]: Dictionary where the key is the capture name
                and the value is a list of corresponding nodes.
        """
        language_data = self.query_patterns.get(language, PythonData)
        language_object = tree_sitter.Language(language_data.tree_sitter_language)
        query = tree_sitter.Query(language_object, language_data.query)
        query_cursor = tree_sitter.QueryCursor(query)
        captures: dict[str, list[tree_sitter.Node]] = query_cursor.captures(tree.root_node)

        return captures
