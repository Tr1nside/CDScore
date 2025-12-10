from src.density_calculation.checker.abc_rule.rule import CheckerRule


class RuleRegistry:
    _rules: dict[int, CheckerRule] = {}

    @classmethod
    def register(cls, rule: CheckerRule) -> None:
        cls._rules[rule.code] = rule

    @classmethod
    def get_all(cls) -> list[CheckerRule]:
        return list(cls._rules.values())


def register_rule(rule: CheckerRule) -> CheckerRule:
    RuleRegistry.register(rule)
    return rule
