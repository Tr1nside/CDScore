from src.data_types import CheckerData, CommentData
from src.density_calculation.abc_rule.specification import Spec
from src.density_calculation.abc_rule.strategy import Strategy


class CheckerRule:
    """Rule for checking comment"""

    def __init__(self, code: int, spec: Spec, strategy: Strategy) -> None:
        """
        Init rule.

        Args:
            code(int): Rule ID
            spec(Spec): Specification for checking comment
            strategy(Strategy): Strategy for generate error data
        """

        self.code = code
        self._spec = spec
        self._strategy = strategy

    def check(self, comment_data: CommentData) -> CheckerData | None:
        """
        Checking a comment against the current rule

        Args:
            comment_data (CommentData): Comment details

        Returns:
            CheckerData | None: Result of checking
        """
        if self._spec.find_error(comment_data):
            error_data = self._strategy.generate_error_data(comment_data)
            return error_data

        return None
