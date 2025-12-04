from src.output.abstract_output import AbstractOutput


class CLIOutput(AbstractOutput):
    def error(self, error_text: str) -> None:
        print(f"Error: {error_text}")

    def info(self, info_text: str) -> None:
        print(f"Error: {info_text}")
