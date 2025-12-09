from src.data_types import CheckerData, CommentData
from src.density_calculation.abc_rule.registry import RuleRegistry
from src.density_calculation.abc_rule.rule import CheckerRule


class CommentChecker:
    """
    This class is responsible for taking a single comment and running it
    against a defined set of validation rules.
    It collects and returns all resulting errors or warnings.
    """

    _rules: list[CheckerRule] = RuleRegistry.get_all()

    def check(self, comment: CommentData) -> list[CheckerData]:
        """
        Validates a single comment against all registered rules.

        The method iterates through the list of rules and delegates the validation
        task to each rules `check` method. It collects the structured results
        (CheckerData) for all detected violations.

        Args:
            comment (CommentData): Comment details.

        Returns:
            list[CheckerData]: A list of structured results. Each item represents
                               a specific rule violation found in the comment.
                               Returns an empty list if no errors are found.
        """
        result_datas: list[CheckerData] = []
        for rule in self._rules:
            error_data = rule.check(comment)
            if error_data:
                result_datas.append(error_data)

        return result_datas
