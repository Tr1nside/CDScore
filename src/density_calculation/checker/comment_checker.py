from src.data_types import CheckerData, CommentData
from src.density_calculation.checker.abc_rule.rule import CheckerRule


class CommentChecker:
    """
    Take a single comment and run it against a defined set of validation rules.

    This class collects and returns all resulting errors or warnings from the rule checks.
    """

    _rule_classes: list[type[CheckerRule]] = []
    _rules_loaded: bool = False

    @classmethod
    def register_rule_class(cls, rule_class: type[CheckerRule]) -> None:
        """
        Add a rule class to the registry.

        This method is automatically called by the `@rule` decorator.

        Args:
            rule_class (type[CheckerRule]): The class inheriting from CheckerRule to be registered.
        """
        if rule_class not in cls._rule_classes:
            cls._rule_classes.append(rule_class)

    @classmethod
    def get_rules(cls) -> list[CheckerRule]:
        """
        Create instances of all registered rules.

        Returns:
            list[CheckerRule]: A list of initialized rule objects.
        """
        return [rule_class() for rule_class in cls._rule_classes]

    @classmethod
    def load_all_rules(cls) -> None:
        """
        Ensure all rule modules are imported and registered.

        Imports all rule modules using `rule_loader` only if they haven't been loaded yet.
        """
        if cls._rules_loaded:
            return

        from src.density_calculation.checker.rules.loader import rule_loader

        rule_loader()
        cls._rules_loaded = True

    def check(self, comment: CommentData) -> list[CheckerData]:
        """
        Validate a single comment against all registered rules.

        The method iterates through the list of rules and delegates the validation
        task to each rule's `check` method. It collects the structured results
        (CheckerData) for all detected violations.

        Args:
            comment (CommentData): Comment details.

        Returns:
            list[CheckerData]: A list of structured results. Each item represents
                               a specific rule violation found in the comment.
                               Returns an empty list if no errors are found.
        """
        self.load_all_rules()

        result_datas: list[CheckerData] = []
        for rule in self.get_rules():
            error_data = rule.check(comment)
            if error_data:
                result_datas.append(error_data)

        return result_datas
