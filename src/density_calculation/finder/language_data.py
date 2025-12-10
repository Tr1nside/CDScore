"""
Define abstract base data classes for language configuration.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LanguageData(ABC):
    """
    Represent abstract base data for a programming language configuration.

    Attributes:
        tree_sitter_language (Any): The Tree-sitter language object.
        query (str): The Tree-sitter query string used for matching nodes.
    """

    tree_sitter_language: Any
    query: str
