import argparse
from pathlib import Path

from src.density_calculation.density_searcher import DensitySearcher
from src.logging_setup import setup_logging
from src.output.cli_output import CLIOutput


class ArgsParser:
    def __init__(self, argv: list[str]) -> None:
        parser = argparse.ArgumentParser(
            description="A tool for analyzing the density of comments (CDS).",
            epilog="Example: cdscore.py ./my_project --min-cds 0.5",
        )

        parser.add_argument("path", type=Path, help="Path to the code base to be analyzed.")
        parser.add_argument("--min-cds", type=float, default=float(0), help="Minimum CDS threshold.")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")

        self.args = parser.parse_args(argv)

    @property
    def path(self) -> Path:
        path: Path = self.args.path
        return path

    @property
    def min_cds_threshold(self) -> float:
        min_cds: float = self.args.min_cds
        return min_cds

    @property
    def verbose(self) -> bool:
        verbose: bool = self.args.verbose
        return verbose


class CDSApp:
    def __init__(self, argv: list[str]) -> None:
        self._args_parser = ArgsParser(argv)
        self.root_path = self._args_parser.path
        self.min_cds_threshold = self._args_parser.min_cds_threshold
        self._verbose = self._args_parser.verbose
        setup_logging(self._verbose)

        self._output = CLIOutput()

        self._searcher = DensitySearcher()
        self._searcher.subscribe_output(self._output)

    def run(self) -> int:
        """Запускает основной процесс анализа и возвращает код выхода (0 или 1)."""
        self._output.message(f"Анализ пути: {self.root_path}")
        self._output.message(f"Порог CDS: {self.min_cds_threshold}")

        final_score = self._searcher.start_analysis(self.root_path)
        if final_score < self.min_cds_threshold:
            return 1

        return 0
