from pathlib import Path

from src.data_types import CheckerData


class OutputFormatter:
    def __init__(self) -> None:
        """OutputFormatter initialization"""
        self._current_file: None | Path = None

    def output_generation(self, checker_data: CheckerData) -> str:
        """
        Generate output message

        Args:
            checker_data(CheckerData): Comment data from CommentChecker

        Returns:
            Output message
        """
        comment_data = checker_data.comment_data
        output_parts: list[str] = []
        SPACE = "    "

        if self._check_current_file(comment_data.file_path):
            output_parts.append(f"{str(self._current_file)}:\n")

        comment_message = self._generate_comment_string(checker_data)
        output_parts.append(f"{SPACE}{comment_message}\n")

        return "".join(output_parts)

    def _generate_comment_string(self, checker_data: CheckerData) -> str:
        """
        Generate comment string for output message.

        Args:
            checker_data(CheckerData): Comment data from CommentChecker.

        Returns:
            Comment string.
        """
        comment_data = checker_data.comment_data

        column = comment_data.column_start or ""
        score = checker_data.score if checker_data.score < 0 else f"-{checker_data.score}"

        comment_string = (
            f"{comment_data.start_line_number}:{comment_data.end_line_number}-{column} "
            f"{checker_data.error_string} {score} {checker_data.rule_id}"
        )
        return comment_string

    def _check_current_file(self, filepath: Path) -> bool:
        """
        Checking if the current file has changed.

        Args:
            filepath(Path): Path to the file containing the comment to be checked.

        Returns:
            True if file has changed, else False.
        """
        if self._current_file != filepath:
            self._current_file = filepath
            return True
        return False
