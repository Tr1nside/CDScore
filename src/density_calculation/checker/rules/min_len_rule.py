from src.comment_utils import normalize_docstring
from src.data_types import CheckerData, CommentData, CommentType
from src.density_calculation.checker.abc_rule.rule import CheckerRule
from src.density_calculation.checker.abc_rule.rule_decorator import rule
from src.density_calculation.checker.abc_rule.specification import Spec
from src.density_calculation.checker.abc_rule.strategy import Strategy

MIN_LEN = 7
RULE_ID = 102


class MinLenSpec(Spec):
    """
    Specification: The comment is shorter than the minimum allowed length.
    """

    def find_error(self, comment: CommentData) -> bool:
        """
        Check if the comment text length is less than MIN_LEN.

        Args:
            comment (CommentData): Comment details.

        Returns:
            bool: True if the text length is less than MIN_LEN, False otherwise.
        """
        if comment.comment_type == CommentType.DOCSTRING:
            return self._find_docstring(comment.text)
        else:
            return self._find_inline(comment.text)

    def _find_docstring(self, comment_text: str) -> bool:
        lines = normalize_docstring(comment_text)
        return any(self._find_inline(line) for line in lines)

    def _find_inline(self, comment_text: str) -> bool:
        return len(comment_text) < MIN_LEN


class MinLenStrategy(Strategy):
    """
    Strategy: Generate error data for minimum length violation.
    """

    def generate_error_data(self, comment: CommentData) -> CheckerData:
        """
        Generate CheckerData for the minimum length error.

        Args:
            comment (CommentData): Comment details that violated the rule.

        Returns:
            CheckerData: The error data structure.
        """
        current_len = len(comment.text)
        error_msg = f"The comment too short ({current_len}). Minimum length: {MIN_LEN}."

        return CheckerData(
            score=-1,
            comment_data=comment,
            error_string=error_msg,
            rule_id=RULE_ID,
        )


@rule
class MinLenRule(CheckerRule):
    """
    Rule to check if a comment is shorter than the minimum allowed length (MIN_LEN).
    """

    def _create_specification(self) -> Spec:
        """
        Create the specification object.

        Returns:
            Spec: An instance of MinLenSpec.
        """
        return MinLenSpec()

    def _create_strategy(self) -> Strategy:
        """
        Create the strategy object.

        Returns:
            Strategy: An instance of MinLenStrategy.
        """
        return MinLenStrategy()

    def _set_code(self) -> int:
        """
        Set the unique identifier code for the rule.

        Returns:
            int: The rule's unique code (RULE_ID).
        """
        return RULE_ID
