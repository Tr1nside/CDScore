from abc import ABC, abstractmethod

from src.data_types import CheckerData, CommentData
from src.density_calculation.checker.abc_rule.specification import Spec
from src.density_calculation.checker.abc_rule.strategy import Strategy


class CheckerRule(ABC):
    """
    Abstract base class for defining a comment checking rule.
    """

    def __init__(self) -> None:
        """
        Initialize the rule by setting its code, specification, and strategy.
        """

        self.code = self._set_code()
        self._spec = self._create_specification()
        self._strategy = self._create_strategy()

    def check(self, comment_data: CommentData) -> CheckerData | None:
        """
        Check a comment against the current rule.

        Args:
            comment_data (CommentData): Details of the comment to check.

        Returns:
            CheckerData | None: The result of the check (error data) or None if no violation found.
        """
        if self._spec.find_error(comment_data):
            error_data = self._strategy.generate_error_data(comment_data)
            return error_data

        return None

    @abstractmethod
    def _create_specification(self) -> Spec:
        """
        Create and return the specification object for the rule.

        Returns:
            Spec: The concrete specification instance.
        """
        ...

    @abstractmethod
    def _create_strategy(self) -> Strategy:
        """
        Create and return the strategy object for generating error data.

        Returns:
            Strategy: The concrete strategy instance.
        """
        ...

    @abstractmethod
    def _set_code(self) -> int:
        """
        Set and return the unique identifier code for the rule.

        Returns:
            int: The rule's unique code.
        """
        ...
