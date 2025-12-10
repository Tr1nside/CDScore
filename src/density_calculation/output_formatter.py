"""
Define a class for formatting comment checking results into a displayable string.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from pathlib import Path

from src.data_types import CheckerData


class OutputFormatter:
    """
    Format the results of a comment check (CheckerData) into a human-readable
    output string, grouping messages by file.
    """

    def __init__(self) -> None:
        """Initialize the formatter and track the currently processed file path."""
        self._current_file: None | Path = None

    def output_generation(self, checker_data: CheckerData) -> str:
        """
        Generate the complete output message, including the filename if it is new.

        Args:
            checker_data (CheckerData): Comment data and check results from CommentChecker.

        Returns:
            str: The formatted output message string.
        """
        comment_data = checker_data.comment_data
        output_parts: list[str] = []
        SPACE = "    "

        if self._check_current_file(comment_data.file_path):
            output_parts.append(f"{str(self._current_file)}:\n")

        comment_message = self._generate_comment_string(checker_data)
        output_parts.append(f"{SPACE}{comment_message}")

        return "".join(output_parts)

    def _generate_comment_string(self, checker_data: CheckerData) -> str:
        """
        Generate the detailed comment string part of the output message.

        Args:
            checker_data (CheckerData): Comment data and check results from CommentChecker.

        Returns:
            str: The formatted string detailing the comment location, error, and score.
        """
        comment_data = checker_data.comment_data
        score = checker_data.score if checker_data.score < 0 else f"-{checker_data.score}"

        comment_string = (
            f"line {comment_data.start_line_number}:{comment_data.end_line_number},"
            f" col {comment_data.column_start}:{comment_data.column_end},"
            f" {checker_data.error_string}, {score}, CDS{checker_data.rule_id}"
        )
        return comment_string

    def _check_current_file(self, filepath: Path) -> bool:
        """
        Check if the current file being processed has changed.

        If the file has changed, update the internal state to the new file path.

        Args:
            filepath (pathlib.Path): Path to the file containing the comment to be checked.

        Returns:
            bool: True if the file path has changed, False otherwise.
        """
        if self._current_file != filepath:
            self._current_file = filepath
            return True
        return False
