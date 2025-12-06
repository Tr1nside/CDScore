from abc import ABC, abstractmethod


class AbstractOutput(ABC):
    @abstractmethod
    def message(self, error_text: str) -> None:
        """Abstract function for error message"""
        ...
