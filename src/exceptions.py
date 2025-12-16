class CommentTypeError(Exception):
    """Exception raised when an unknown or invalid comment type is detected.

    Args:
        message (str, optional): The error message describing the issue.
            Defaults to "Unknown type of comment".
    """

    def __init__(self, message: str = "Unknown type of comment") -> None:
        self.message = message
        super().__init__(self.message)


class FileTypeError(Exception):
    """Exception raised when an unknown or invalid file suffix is detected.

    Args:
        message (str, optional): The error message describing the issue.
            Defaults to "Unknown type of file".
    """

    def __init__(self, message: str = "Unknown type of file") -> None:
        self.message = message
        super().__init__(self.message)
