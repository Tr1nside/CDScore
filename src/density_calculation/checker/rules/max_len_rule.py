from src.data_types import CheckerData, CommentData
from src.density_calculation.checker.abc_rule.rule import CheckerRule
from src.density_calculation.checker.abc_rule.rule_decorator import rule
from src.density_calculation.checker.abc_rule.specification import Spec
from src.density_calculation.checker.abc_rule.strategy import Strategy

MAX_LEN = 120
RULE_ID = 101


class MaxLenSpec(Spec):
    """
    Specification: The comment exceeds the maximum allowed length.
    """

    def find_error(self, comment: CommentData) -> bool:
        """
        Check if the comment text length exceeds the MAX_LEN.

        Args:
            comment (CommentData): Comment details.

        Returns:
            bool: True if the text length exceeds MAX_LEN, False otherwise.
        """
        return len(comment.text) > MAX_LEN


class MaxLenStrategy(Strategy):
    """
    Strategy: Generate error data for maximum length violation.
    """

    def generate_error_data(self, comment: CommentData) -> CheckerData:
        """
        Generate CheckerData for the maximum length error.

        Args:
            comment (CommentData): Comment details that violated the rule.

        Returns:
            CheckerData: The error data structure.
        """
        current_len = len(comment.text)
        error_msg = f"Комментарий слишком длинный ({current_len} символов). Максимально разрешенная длина: {MAX_LEN}."

        return CheckerData(
            score=-5,
            comment_data=comment,
            error_string=error_msg,
            rule_id=RULE_ID,
        )


@rule
class MaxLenRule(CheckerRule):
    """
    Rule to check if a comment exceeds the maximum allowed length (MAX_LEN).
    """

    def _create_strategy(self) -> Strategy:
        """
        Create the strategy object.

        Returns:
            Strategy: An instance of MaxLenStrategy.
        """
        return MaxLenStrategy()

    def _create_specification(self) -> Spec:
        """
        Create the specification object.

        Returns:
            Spec: An instance of MaxLenSpec.
        """
        return MaxLenSpec()

    def _set_code(self) -> int:
        """
        Set the unique identifier code for the rule.

        Returns:
            int: The rule's unique code (RULE_ID).
        """
        return RULE_ID
