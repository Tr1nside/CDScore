"""
Define a concrete implementation of AbstractOutput for logging messages to the CLI.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

from loguru import logger

from src.output.abstract_output import AbstractOutput


class CLIOutput(AbstractOutput):
    """
    Implement the output handler that prints messages to the console using loguru's logger.
    """

    def message(self, info_text: str) -> None:
        """
        Output the given information text to the standard output using logger.info.

        Args:s
            info_text (str): The formatted message string to output.
        """
        logger.info(f"{info_text}")
