from loguru import logger

from src.output.abstract_output import AbstractOutput


class CLIOutput(AbstractOutput):
    def message(self, info_text: str) -> None:
        logger.info(f"{info_text}")
