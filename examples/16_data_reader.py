"""
Demo 16: DataReader (I/O Utilities)

Shows how to load integers, strings, and lines from files using the
industrial-grade I/O utilities in Alnoms.
"""

import os
from alnoms.core.io import DataReader


def create_temp_files():
    """Creates small temporary files for demonstration."""
    os.makedirs("data", exist_ok=True)

    # Integers file
    with open("data/ints.txt", "w") as f:
        f.write("10 20 30\n40 50")

    # Strings file
    with open("data/strings.txt", "w") as f:
        f.write("alpha beta gamma\ndelta epsilon")

    # Lines file
    with open("data/lines.txt", "w") as f:
        f.write("line1\n\nline3\nline4")


def demo_data_reader():
    print("\n=== DataReader Demo ===\n")

    create_temp_files()

    # 1. Read all integers
    ints = DataReader.read_all_ints("data/ints.txt")
    print("1) Integers loaded:")
    print(ints, "\n")

    # 2. Read all strings
    strings = DataReader.read_all_strings("data/strings.txt")
    print("2) Strings loaded:")
    print(strings, "\n")

    # 3. Read lines (preserves empty lines)
    lines = DataReader.read_lines("data/lines.txt")
    print("3) Lines loaded:")
    print(lines, "\n")


if __name__ == "__main__":
    demo_data_reader()
