"""
Define abstract base data classes for language configuration.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.data_types import CommentType


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


class LanguageNormalizer(ABC):
    """Abstract base class for normalizing comment and docstring text.

    Subclasses must implement language-specific logic to remove markers,
    quotes, prefixes, and common indentation.
    """

    def normalize(self, text: str, comment_type: CommentType) -> list[str]:
        """Normalizes the given comment or docstring text.

        Delegates the call to the appropriate abstract method based on the type.

        Args:
            text (str): The raw comment or docstring text.
            comment_type (CommentType): The type of comment (INLINE or DOCSTRING).

        Returns:
            list[str]: A list of lines of the normalized text.
        """
        if comment_type == CommentType.INLINE:
            return self._normalize_inline(text)
        elif comment_type == CommentType.DOCSTRING:
            return self._normalize_docstring(text)

    @abstractmethod
    def _normalize_inline(self, text: str) -> list[str]:
        """Abstract method: Normalizes an inline comment by removing its marker and leading whitespace.

        Args:
            text (str): The raw inline comment text.

        Returns:
            list[str]: A list of lines of the normalized text.
        """
        ...

    @abstractmethod
    def _normalize_docstring(self, text: str) -> list[str]:
        """Abstract method: Normalizes a docstring by removing quotes, prefixes, and common indentation.

        Args:
            text (str): The raw docstring text.

        Returns:
            list[str]: A list of lines of the normalized text.
        """
        ...
