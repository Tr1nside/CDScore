"""
Define the core class representing a single checking rule in the Comment Density Score (CDS) system.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from src.data_types import CheckerData, CommentData
from src.density_calculation.checker.abc_rule.specification import Spec
from src.density_calculation.checker.abc_rule.strategy import Strategy


class CheckerRule:
    """
    Represent a single rule for checking comment quality, defined by a Specification
    for identifying issues and a Strategy for generating the corresponding error data.
    """

    def __init__(self, code: int, spec: Spec, strategy: Strategy) -> None:
        """
        Initialize the checking rule with a unique ID, a specification, and a strategy.

        Args:
            code (int): The unique identifier (ID) for the rule.
            spec (Spec): The specification object used to determine if the rule is violated.
            strategy (Strategy): The strategy object used to generate the penalty/error data.
        """

        self.code = code
        self._spec = spec
        self._strategy = strategy

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
