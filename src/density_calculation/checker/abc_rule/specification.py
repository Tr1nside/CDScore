from abc import ABC, abstractmethod

from src.data_types import CommentData


class Spec(ABC):
    @abstractmethod
    def find_error(self, comment: CommentData) -> bool:
        """
        The specification that comment must meet

        Args:
            comment (CommentData): Comment details

        Returns:
            bool: True if the comment violates the specification.
                  False if the comment meets the specification.
        """
        ...
