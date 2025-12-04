from abc import ABC, abstractmethod


class AbstractOutput(ABC):
    @abstractmethod
    def error(self, error_text: str) -> None: ...

    @abstractmethod
    def info(self, info_text: str) -> None: ...
