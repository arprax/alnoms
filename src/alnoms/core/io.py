"""
Input/Output utilities for loading research‑grade test datasets.

This module provides lightweight, dependency‑free helpers for reading
whitespace‑separated integers, tokens, or lines from files. These utilities
are used throughout the Alnoms ecosystem for:

- Sorting and searching benchmarks
- Trie and string‑processing tests
- Large‑scale dataset ingestion
- Reproducible algorithm experiments

Example:
    >>> from alnoms.core.io import DataReader
    >>> ints = DataReader.read_all_ints("tests/data/1Kints.txt")
"""

import os
from typing import List


class DataReader:
    """Utility functions for loading test datasets from files.

    All methods are static and designed for predictable, dependency‑free
    behavior. They support common formats used in algorithm benchmarking,
    including whitespace‑separated integers, tokens, and raw lines.
    """

    @staticmethod
    def read_all_ints(path: str) -> List[int]:
        """Read all whitespace‑separated integers from a file.

        The file may contain integers separated by spaces, tabs, or newlines.
        This format is commonly used for sorting and searching benchmarks.

        Args:
            path (str): Absolute or relative path to the input file.

        Returns:
            List[int]: A list of parsed integers.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If any token cannot be parsed as an integer.
        """
        DataReader._validate_path(path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            tokens = content.split()
            return [int(token) for token in tokens]

    @staticmethod
    def read_all_strings(path: str) -> List[str]:
        """Read all whitespace‑separated tokens from a file.

        Useful for loading datasets for Trie benchmarks, MSD/LSD string sorts,
        and token‑based algorithm tests.

        Args:
            path (str): Absolute or relative path to the input file.

        Returns:
            List[str]: A list of string tokens.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        DataReader._validate_path(path)
        with open(path, "r", encoding="utf-8") as f:
            return f.read().split()

    @staticmethod
    def read_lines(path: str) -> List[str]:
        """Read all lines from a file, stripping leading and trailing whitespace.

        Empty lines are preserved as empty strings. This is useful for
        line‑oriented algorithms, text processing, and structured input formats.

        Args:
            path (str): Absolute or relative path to the input file.

        Returns:
            List[str]: A list of cleaned lines.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        DataReader._validate_path(path)
        lines = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line.strip())
        return lines

    @staticmethod
    def _validate_path(path: str) -> None:
        """Validate that a file exists before attempting to read it.

        Args:
            path (str): Path to validate.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
