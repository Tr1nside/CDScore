from src.data_types import CheckerData


class OutputFormatter:
    def output_generation(self, checker_data: CheckerData) -> str: ...


"""
src/searcher.py
  10:5   error   Отрицательный Score. Проверьте логику.     CDS001
  25:12  warning  Использование устаревшего метода.         CDS002
"""
