class CDSScoringManager:
    def __init__(self) -> None:
        """Init scoring manager"""
        self._score = 0

    def add(self, score: int) -> None:
        self._score += score

    @property
    def score(self) -> int:
        return self._score
