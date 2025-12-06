class CDSScoringManager:
    def __init__(self) -> None:
        """Init scoring manager"""
        self.score = 0

    def add(self, score: int) -> None:
        self.score += score
