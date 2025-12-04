from loguru import logger

from src.output.abstract_output import AbstractOutput


class CLIOutput(AbstractOutput):
    def message_error(self, error_text: str) -> None:
        logger.error(f"Error: {error_text}")

    def message_info(self, info_text: str) -> None:
        logger.info(f"Error: {info_text}")
