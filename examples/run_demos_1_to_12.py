import subprocess
import sys
import os

DEMO_DIR = ""

# All demo files in the correct order
DEMO_FILES = [
    "1_cubic_matrix.py",
    "2_quadratic_duplicates.py",
    "3_nested_membership.py",
    "4_concat_in_loop.py",
    "5_list_extend_vs_append.py",
    "6_redundant_sort.py",
    "7_manual_bubble_sort.py",
    "8_linear_search_in_loop.py",
    "9_naive_find.py",
    "10_dfs_like_loop.py",
    "11_cycle_detection_manual.py",
    "12_execution_entrypoint.py",
]


def run_demo(file):
    path = os.path.join(DEMO_DIR, file)
    print("\n" + "=" * 80)
    print(f"▶ Running demo: {file}")
    print("=" * 80)

    cmd = [sys.executable, "-m", "alnoms", "analyze", path, "--deep"]
    # cmd = [sys.executable, "-m", "alnoms", "analyze", path]

    # Run the command and stream output
    subprocess.run(cmd)


if __name__ == "__main__":
    for f in DEMO_FILES:
        run_demo(f)
