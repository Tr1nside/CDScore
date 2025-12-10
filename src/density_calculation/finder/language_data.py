from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LanguageData(ABC):
    tree_sitter_language: Any
    query: str
