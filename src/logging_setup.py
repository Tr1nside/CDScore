import sys

from loguru import logger


def setup_logging(verbose: bool = False) -> None:
    """
    Configures global logging using loguru.
    """
    logger.remove()

    if verbose:
        logger.add(
            sys.stdout,
            level="DEBUG",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
        )
    else:
        # Normal mode: only INFO and ERROR
        logger.add(sys.stdout, level="INFO", format="<level>{message}</level>")
