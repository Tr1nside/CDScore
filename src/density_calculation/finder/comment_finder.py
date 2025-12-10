from pathlib import Path


class CommentFinder:
    def __init__(self) -> None:
        """Init comment finder"""
        ...

    def find_in_dir(self, path: Path) -> None:
        """Method for find comment in all files in dir"""
        ...
