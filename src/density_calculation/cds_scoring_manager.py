"""
Define a class for managing and calculating the comment density score (CDS).

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""


class CDSScoringManager:
    """
    Manage and calculate the total comment density score (CDS).
    """

    def __init__(self) -> None:
        """Initialize the manager with a zero score."""
        self._score = 0

    def add(self, score: int) -> None:
        """
        Add a score value to the total internal score.

        Args:
            score (int): The score value to add.
        """
        self._score += score

    @property
    def score(self) -> int:
        """
        Return the total calculated score.

        Returns:
            int: The current total score.
        """
        return self._score
