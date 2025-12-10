"""
Define the abstract base class for output handlers.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from abc import ABC, abstractmethod


class AbstractOutput(ABC):
    """
    Represent an abstract base class for different output methods (e.g., console, file).
    """

    @abstractmethod
    def message(self, error_text: str) -> None:
        """
        Send a formatted error or message string to the defined output channel.

        Args:
            error_text (str): The formatted message string to output.
        """
        ...
