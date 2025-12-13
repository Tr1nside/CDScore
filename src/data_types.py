"""
Define core data structures (dataclasses and enums) used across the CDS analysis tool.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path


@dataclass(frozen=True)
class CommentData:
    """
    Represent detailed information about a single found comment.

    Attributes:
        file_path (pathlib.Path): The path to the file containing the comment.
        text (str): The raw text content of the comment.
        start_line_number (int): The starting line number (1-based).
        end_line_number (int): The ending line number (1-based).
        column_start (int): The starting column number (1-based).
        column_end (int): The ending column number (0-based).
        comment_type (str): The type of the comment node (e.g., 'comment', 'string').
        scope (CommentScope): The context (function, class, module) where the comment was found.
    """

    file_path: Path
    text: str

    start_line_number: int
    end_line_number: int
    column_start: int
    column_end: int

    comment_type: CommentType
    scope: CommentScope


@dataclass(frozen=True)
class CheckerData:
    """
    Represent the check result for a single comment against a specific rule.

    Attributes:
        score (int): The score adjustment applied (usually negative for penalty).
        comment_data (CommentData): The original data of the comment that was checked.
        error_string (str): A human-readable description of the error/warning.
        rule_id (int): The unique identifier of the rule that triggered this result.
    """

    score: int
    comment_data: CommentData
    error_string: str

    rule_id: int


class LanguagesEnum(Enum):
    """
    Define supported programming languages.
    """

    PYTHON = auto()


class CommentScope(Enum):
    """
    Define the structural scope where a comment resides within the code.
    """

    FUNCTION = auto()
    MODULE = auto()
    CLASS = auto()
    UNKNOWN = auto()


class CommentType(Enum):
    INLINE = auto()
    DOCSTRING = auto()
