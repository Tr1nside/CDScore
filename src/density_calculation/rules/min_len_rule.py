from src.data_types import CheckerData, CommentData
from src.density_calculation.abc_rule.registry import register_rule
from src.density_calculation.abc_rule.rule import CheckerRule
from src.density_calculation.abc_rule.specification import Spec
from src.density_calculation.abc_rule.strategy import Strategy

MIN_LEN = 7
RULE_ID = 102


class MinLenSpec(Spec):
    """Спецификация: Комментарий короче минимальной длины."""

    def find_error(self, comment: CommentData) -> bool:
        """
        Возвращает True, если длина текста комментария меньше MIN_LEN.
        """
        return len(comment.text) < MIN_LEN


class MinLenStrategy(Strategy):
    """Стратегия: Генерация данных об ошибке недостаточной длины."""

    def generate_error_data(self, comment: CommentData) -> CheckerData:
        """
        Генерирует CheckerData для ошибки минимальной длины.
        """
        current_len = len(comment.text)
        error_msg = f"Комментарий слишком короткий ({current_len} символов). Минимально разрешенная длина: {MIN_LEN}."

        return CheckerData(
            score=-1,
            comment_data=comment,
            error_string=error_msg,
            rule_id=RULE_ID,
        )


rule = CheckerRule(RULE_ID, MinLenSpec(), MinLenStrategy())
register_rule(rule)
