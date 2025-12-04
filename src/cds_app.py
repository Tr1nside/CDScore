import argparse
from pathlib import Path

from src.density_calculation.density_searcher import DensitySearcher
from src.output.cli_output import CLIOutput


class ArgsParser:
    def __init__(self, argv: list[str]):
        parser = argparse.ArgumentParser(
            description="A tool for analyzing the density of comments (CDS).",
            epilog="Example: cdscore.py ./my_project --min-cds 0.5",
        )

        parser.add_argument("path", type=Path, help="Path to the code base to be analyzed.")
        parser.add_argument("--min-cds", type=float, default=0.0, help="Minimum CDS threshold.")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")

        self.args = parser.parse_args(argv)

    def get_path(self) -> Path:
        return self.args.path

    def get_min_cds_threshold(self) -> float:
        return self.args.min_cds

    def is_verbose(self) -> bool:
        return self.args.verbose


class CDSApp:
    def __init__(self, argv: list[str]):
        self._args_parser = ArgsParser(argv)

        self.root_path = self._args_parser.get_path()
        self.min_cds_threshold = self._args_parser.get_min_cds_threshold()
        self.verbose = self._args_parser.is_verbose()

        self._output = CLIOutput()
        self._searcher = DensitySearcher()

    def run(self) -> int:
        """Запускает основной процесс анализа и возвращает код выхода (0 или 1)."""

        print(f"Анализ пути: {self.root_path}")
        print(f"Порог CDS: {self.min_cds_threshold}")

        final_score = self._searcher.start_analysis(self.root_path)

        if final_score < self.min_cds_threshold:
            return 1

        return 0
