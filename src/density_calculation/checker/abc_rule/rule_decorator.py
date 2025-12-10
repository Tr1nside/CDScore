from src.density_calculation.checker.abc_rule.rule import CheckerRule
from src.density_calculation.checker.comment_checker import CommentChecker


def rule(cls: type[CheckerRule]) -> type[CheckerRule]:
    """
    Register a rule class automatically in CommentChecker.

    Decorator to automatically register the rule class in `CommentChecker`.
    Usage:
        @rule
        class MyAwesomeRule(CheckerRule):
            ...

    Args:
        cls (type[CheckerRule]): The class inheriting from CheckerRule to be registered.

    Returns:
        type[CheckerRule]: The decorated class.

    Raises:
        TypeError: If the decorated class does not inherit from CheckerRule.
    """
    if not issubclass(cls, CheckerRule):
        raise TypeError(f"Класс {cls.__name__} должен наследоваться от CheckerRule")

    CommentChecker.register_rule_class(cls)
    return cls
