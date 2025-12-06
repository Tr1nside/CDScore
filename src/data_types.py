from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommentData:
    """Структура данных для хранения информации о найденном комментарии."""

    file_path: Path
    line_number: int

    text: str
    end_line_number: int | None = None
    column_start: int | None = None


@dataclass(frozen=True)
class CheckerData:
    score: int
    comment_data: CommentData

    rule_id: int
