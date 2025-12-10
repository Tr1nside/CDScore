from dataclasses import dataclass

import tree_sitter_python as tspython

from src.density_calculation.finder.language_data import LanguageData


@dataclass(frozen=True)
class PythonData(LanguageData):
    tree_sitter_language = tspython.language()
    query = r"""
        ;; 1. Захват обычных комментариев
        (comment) @item

        ;; 2. Захват Docstrings в функциях/методах
        (function_definition
            body: (block
                (expression_statement (string) @item .)))

        ;; 3. Захват Docstrings в классах
        (class_definition
            body: (block
                (expression_statement (string) @item .)))

        ;; 4. Захват Docstrings модуля (корневой уровень)
        (module (expression_statement (string) @item))

        ;; Гарантируем, что захватываются только узлы с @item
        (#match-only item)
    """
