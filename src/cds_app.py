"""
Define the command-line argument parser and the main application class for CDS analysis.

Author: Petr Lavrishchev
License: MIT License (see LICENSE file for details)
"""

import argparse
from pathlib import Path

from src.density_calculation import DensitySearcher
from src.logging_setup import setup_logging
from src.output.cli_output import CLIOutput


class ArgsParser:
    """
    Parse command-line arguments for the CDS analysis tool.
    """

    def __init__(self, argv: list[str]) -> None:
        """
        Initialize the parser and parse the arguments.

        Args:
            argv (list[str]): The list of arguments to parse (usually sys.argv[1:]).
        """
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
        """
        Return the path to the code base to be analyzed.

        Returns:
            pathlib.Path: The root path for analysis.
        """
        path: Path = self.args.path
        return path

    @property
    def min_cds_threshold(self) -> float:
        """
        Return the minimum required CDS threshold.

        Returns:
            float: The minimum CDS score allowed.
        """
        min_cds: float = self.args.min_cds
        return min_cds

    @property
    def verbose(self) -> bool:
        """
        Return the verbose output flag.

        Returns:
            bool: True if verbose output is enabled, False otherwise.
        """
        verbose: bool = self.args.verbose
        return verbose


class CDSApp:
    """
    The main application class that orchestrates argument parsing, logging, and CDS analysis.
    """

    def __init__(self, argv: list[str]) -> None:
        """
        Initialize the application, parse arguments, setup logging, and configure the searcher.

        Args:
            argv (list[str]): The command-line arguments.
        """
        self._args_parser = ArgsParser(argv)
        self.root_path = self._args_parser.path
        self.min_cds_threshold = self._args_parser.min_cds_threshold
        self._verbose = self._args_parser.verbose
        setup_logging(self._verbose)

        self._output = CLIOutput()

        self._searcher = DensitySearcher()
        self._searcher.subscribe_output(self._output)

    def run(self) -> int:
        """
        Start the main analysis process and return the exit code (0 for success, 1 for failure).

        Returns:
            int: The application exit code.
        """
        self._output.message(f"Анализ пути: {self.root_path}")
        self._output.message(f"Порог CDS: {self.min_cds_threshold}")

        final_score = self._searcher.start_analysis(self.root_path)
        if final_score < self.min_cds_threshold:
            return 1

        return 0
