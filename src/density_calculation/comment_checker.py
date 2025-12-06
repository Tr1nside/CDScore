from src.data_types import CheckerData, CommentData


class CommentChecker:
    def __init__(self) -> None:
        """Init comment checker"""
        ...

    def check(self, comment: CommentData) -> CheckerData: ...
