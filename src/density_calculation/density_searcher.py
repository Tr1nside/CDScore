from pathlib import Path

from src.data_types import CheckerData, CommentData
from src.density_calculation.cds_scoring_manager import CDSScoringManager
from src.density_calculation.checker.comment_checker import CommentChecker
from src.density_calculation.comment_finder import CommentFinder
from src.density_calculation.output_formatter import OutputFormatter
from src.output import AbstractOutput


class DensitySearcher:
    def __init__(self) -> None:
        self._outputs: set[AbstractOutput] = set()
        self._finder = CommentFinder()
        self._checker = CommentChecker()
        self._output_formatter = OutputFormatter()
        self._scoring_manager = CDSScoringManager()

    def subscribe_output(self, output: AbstractOutput) -> None:
        self._outputs.add(output)

    def check(self, comment: CommentData) -> None:
        checker_datas = self._checker.check(comment)
        for check_data in checker_datas:
            self.notify_output(check_data)
            self.scoring(check_data.score)

    def notify_output(self, data_from_checker: CheckerData) -> None:
        if data_from_checker.score < 0:
            output_string = self._output_formatter.output_generation(data_from_checker)
            for output in self._outputs:
                output.message(output_string)

    def scoring(self, score: int) -> None:
        self._scoring_manager.add(score)

    def start_analysis(self, path: Path) -> float:
        TEST_SCORE = 0.7
        return TEST_SCORE
