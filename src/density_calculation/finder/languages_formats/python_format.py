"""
Define the configuration data structure for the Python programming language.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from dataclasses import dataclass

import tree_sitter_python as tspython

from src.density_calculation.finder.language_data import LanguageData


@dataclass(frozen=True)
class PythonData(LanguageData):
    """
    Represent the language-specific data for Python, including the Tree-sitter language parser
    and the query string for extracting comments and docstrings.
    """

    tree_sitter_language = tspython.language()
    query = r"""
        ;; 1. Capture regular comments
        (comment) @item

        ;; 2. Capture Docstrings in functions/methods
        (function_definition
            body: (block
                (expression_statement (string) @item .)))

        ;; 3. Capture Docstrings in classes
        (class_definition
            body: (block
                (expression_statement (string) @item .)))

        ;; 4. Capture module Docstrings (root level)
        (module (expression_statement (string) @item))

        ;; Ensure only nodes captured as @item are returned
        (#match-only item)
    """
