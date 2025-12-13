"""
Define the core class representing a single checking rule in the Comment Density Score (CDS) system.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from abc import ABC, abstractmethod

from src.data_types import CheckerData, CommentData
from src.density_calculation.checker.abc_rule.specification import Spec
from src.density_calculation.checker.abc_rule.strategy import Strategy


class CheckerRule(ABC):
    """
    Represent a single rule for checking comment quality, defined by a Specification
    for identifying issues and a Strategy for generating the corresponding error data.
    """

    def __init__(self) -> None:
        """
        Initialize the checking rule with a unique ID, a specification, and a strategy.

        Args:
            code (int): The unique identifier (ID) for the rule.
            spec (Spec): The specification object used to determine if the rule is violated.
            strategy (Strategy): The strategy object used to generate the penalty/error data.
        """

        self.code = self._set_code()
        self._spec = self._create_specification()
        self._strategy = self._create_strategy()

    def check(self, comment_data: CommentData) -> CheckerData | None:
        """
        Check a comment against the current rule specification.

        If the specification finds an error, the strategy generates the resulting CheckerData.

        Args:
            comment_data (CommentData): The detailed data of the comment to check.

        Returns:
            CheckerData | None: The resulting CheckerData if the rule is violated,
                                otherwise None.
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
