from src.data_types import CheckerData, CommentData
from src.density_calculation.checker.abc_rule.registry import register_rule
from src.density_calculation.checker.abc_rule.rule import CheckerRule
from src.density_calculation.checker.abc_rule.specification import Spec
from src.density_calculation.checker.abc_rule.strategy import Strategy

MAX_LEN = 120
RULE_ID = 101


class MaxLenSpec(Spec):
    """Спецификация: Комментарий превышает максимальную длину."""

    def find_error(self, comment: CommentData) -> bool:
        """
        Возвращает True, если длина текста комментария превышает MAX_LEN.
        """
        return len(comment.text) > MAX_LEN


class MaxLenStrategy(Strategy):
    """Стратегия: Генерация данных об ошибке превышения длины."""

    def generate_error_data(self, comment: CommentData) -> CheckerData:
        """
        Генерирует CheckerData для ошибки максимальной длины.
        """
        current_len = len(comment.text)
        error_msg = f"Комментарий слишком длинный ({current_len} символов). Максимально разрешенная длина: {MAX_LEN}."

        return CheckerData(
            score=-5,
            comment_data=comment,
            error_string=error_msg,
            rule_id=RULE_ID,
        )


rule = CheckerRule(RULE_ID, MaxLenSpec(), MaxLenStrategy())
register_rule(rule)
