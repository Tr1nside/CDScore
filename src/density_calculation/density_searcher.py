"""
Define the main orchestrator class for finding, checking, and scoring comments.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from pathlib import Path

from src.data_types import CheckerData, CommentData
from src.density_calculation.cds_scoring_manager import CDSScoringManager
from src.density_calculation.checker.comment_checker import CommentChecker
from src.density_calculation.finder.comment_finder import CommentFinder
from src.density_calculation.output_formatter import OutputFormatter
from src.output import AbstractOutput


class DensitySearcher:
    """
    Orchestrate the comment density analysis process:
    finds comments, checks them against rules, scores them, and notifies outputs.
    """

    def __init__(self) -> None:
        """
        Initialize the searcher, setup components, and connect the finder's action
        to the internal check method.
        """
        self._outputs: set[AbstractOutput] = set()
        self._checker = CommentChecker()
        self._output_formatter = OutputFormatter()
        self._scoring_manager = CDSScoringManager()

        self._finder = CommentFinder()
        self._finder.connect_check_action(self.check)

    def subscribe_output(self, output: AbstractOutput) -> None:
        """
        Subscribe an AbstractOutput object to receive notifications.

        Args:
            output (AbstractOutput): The output handler to subscribe.
        """
        self._outputs.add(output)

    def check(self, comment: CommentData) -> None:
        """
        Check a found comment against all defined rules, score it, and notify outputs.

        Args:
            comment (CommentData): The data object representing the found comment.
        """
        checker_datas = self._checker.check(comment)
        for check_data in checker_datas:
            self.notify_output(check_data)
            self.scoring(check_data.score)

    def notify_output(self, data_from_checker: CheckerData) -> None:
        """
        Generate and send a message to all subscribed outputs if the score is negative.

        Args:
            data_from_checker (CheckerData): The result data from the comment checker.
        """
        if data_from_checker.score < 0:
            output_string = self._output_formatter.output_generation(data_from_checker)
            for output in self._outputs:
                output.message(output_string)

    def scoring(self, score: int) -> None:
        """
        Add the given score to the total comment density score.

        Args:
            score (int): The score to add (can be positive or negative).
        """
        self._scoring_manager.add(score)

    def start_analysis(self, path: Path) -> float:
        """
        Start the recursive comment finding and analysis process for the given path.

        Args:
            path (pathlib.Path): The starting path (file or directory).

        Returns:
            float: The final calculated comment density score.
        """
        self._finder.find(path)

        result_score = self._scoring_manager.score
        return result_score
