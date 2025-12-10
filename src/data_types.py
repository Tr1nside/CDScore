from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path


@dataclass(frozen=True)
class CommentData:
    """Data structure for storing information about found comments."""

    file_path: Path
    text: str

    start_line_number: int
    end_line_number: int
    column_start: int
    column_end: int

    comment_type: str
    scope: str


@dataclass(frozen=True)
class CheckerData:
    """
    Check Result for a single comment.

    Aggregates the final scoring result and detailed information about the
    error or warning found within a comment
    """

    score: int
    comment_data: CommentData
    error_string: str

    rule_id: int


class LanguagesEnum(Enum):
    PYTHON = auto()
