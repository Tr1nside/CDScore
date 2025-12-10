"""
Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from abc import ABC, abstractmethod

from src.data_types import CheckerData, CommentData


class Strategy(ABC):
    """
    Strategy for generate error data
    """

    @abstractmethod
    def generate_error_data(self, comment: CommentData) -> CheckerData:
        """
        Generate data from checking comment

        Args:
            comment (CommentData): Comment details

        Returns:
            CheckerData: Result data from checking comment
        """
        ...
