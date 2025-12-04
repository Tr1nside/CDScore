from abc import ABC, abstractmethod


class AbstractOutput(ABC):
    @abstractmethod
    def message_error(self, error_text: str) -> None:
        """Abstract function for error message"""
        ...

    @abstractmethod
    def message_info(self, info_text: str) -> None:
        """Abstract function for info message"""
        ...
