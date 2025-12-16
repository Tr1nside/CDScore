from src.data_types import CheckerData, CommentData
from src.density_calculation.checker.abc_rule.rule import CheckerRule
from src.density_calculation.checker.abc_rule.rule_decorator import rule
from src.density_calculation.checker.abc_rule.specification import Spec
from src.density_calculation.checker.abc_rule.strategy import Strategy

MIN_LEN = 4
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
        rule_list: list[bool] = []

        if len(comment.text) > 0:
            for line in comment.text:
                rule_list.append(len(line) < MIN_LEN)

        return any(rule_list)


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
