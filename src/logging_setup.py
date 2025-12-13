"""
Define a function for setting up global logging configuration using the loguru library.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

import sys

from loguru import logger


def setup_logging(verbose: bool = False) -> None:
    """
    Configure global logging using loguru, setting different levels for verbose and normal modes.

    In verbose mode, logging level is set to DEBUG.
    In normal mode, logging level is set to INFO, and only the message is displayed.

    Args:
        verbose (bool): If True, enable detailed DEBUG level logging; otherwise, use INFO level. Defaults to False.

    Returns:
        None: The function does not return a value.
    """
    logger.remove()

    if verbose:
        logger.add(
            sys.stdout,
            level="DEBUG",
            format="<level><green>{time:YYYY-MM-DD HH:mm:ss}</green></level> | "
            "<level>{level}</level> | "
            "<level><cyan>{name}</cyan>:<cyan>{line}</cyan></level> - "
            "{message}",
        )
    else:
        logger.add(sys.stdout, level="INFO", format="{message}")
