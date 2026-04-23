"""
Alnoms: Automatic Synthetic Input Generator.

Provides a deterministic, OSS‑tier‑aligned fallback for empirical scaling when
no user‑defined `data_gen(n)` is available. The AutoGen module infers simple
structural patterns from a target function's AST and generates execution‑ready
tuple arguments suitable for doubling tests and performance experiments.

Design goals:
    • Eliminate hard dependency on script‑local generators
    • Preserve deterministic, reproducible behavior across runs
    • Use lightweight, transparent heuristics instead of adaptive learning
    • Produce structurally compatible, not semantically rich, input data

AutoGen is intentionally conservative and is designed to be safe for open‑source
governance workflows. Higher tiers (PRO/ENT) may extend or override these
generators with domain‑aware strategies.
"""

import ast
import random
import string
from typing import Tuple, Any


class AutoGen:
    """Deterministic synthetic input generator for empirical scaling.

    AutoGen provides a governance‑aligned fallback mechanism for scripts that
    do not define a `data_gen(n)` function. It infers structurally compatible
    input distributions directly from the target function's AST and produces
    execution‑ready tuple arguments suitable for empirical doubling tests.

    Responsibilities:
        • Classify function structure using lightweight AST heuristics
        • Select an appropriate synthetic input model (list, string, hash‑heavy array)
        • Generate deterministic, reproducible input samples
        • Guarantee OSS‑tier transparency with no adaptive or probabilistic behavior

    OSS‑Tier Guarantees:
        • No dynamic learning or runtime adaptation
        • No multi‑suite or probabilistic generators
        • No external dependencies beyond the Python standard library
        • Fully deterministic behavior across runs

    Notes:
        AutoGen is intentionally conservative. It aims to produce inputs that
        are structurally valid for empirical scaling, not semantically meaningful.
        PRO/ENT tiers may override this with richer, domain‑aware generators.
    """

    # -------------------------------------------------
    # ENTRY POINT
    # -------------------------------------------------
    @staticmethod
    def infer_and_generate(func_ast: ast.AST, n: int) -> Tuple[Any, ...]:
        """Infer an input model from AST structure and generate synthetic data.

        Args:
            func_ast (ast.AST): AST node representing the target function.
            n (int): Input size for synthetic data generation.

        Returns:
            Tuple[Any, ...]: Execution‑ready tuple of arguments for empirical tests.
        """
        pattern = AutoGen._classify(func_ast)
        return AutoGen.generate(pattern, n)

    # -------------------------------------------------
    # AST CLASSIFICATION (HEURISTIC LAYER)
    # -------------------------------------------------
    @staticmethod
    def _classify(func_ast: ast.AST) -> str:
        """Classify a function's structural pattern using lightweight AST heuristics.

        The classifier inspects loop structure, container usage, and sorting calls
        to map the function into one of several synthetic input model categories.

        Args:
            func_ast (ast.AST): AST node representing the target function.

        Returns:
            str: One of:
                • "nested_loops"
                • "hash_heavy"
                • "sorting"
                • "sequential"
                • "generic"
        """
        # --- Detect scalar-only nested-loop functions ---
        # If the function has exactly one parameter and that parameter is used
        # only inside range(param), treat it as a scalar function.
        params = func_ast.args.args
        if len(params) == 1:
            pname = params[0].arg
            scalar_only = True

            for node in ast.walk(func_ast):
                if isinstance(node, ast.Name) and node.id == pname:
                    parent = getattr(node, "parent", None)

                    # Allowed: range(n)
                    if (
                        isinstance(parent, ast.Call)
                        and getattr(parent.func, "id", None) == "range"
                    ):
                        continue

                    # Anything else means it's not scalar-only
                    scalar_only = False
                    break

            if scalar_only:
                return "scalar"
        loop_count = 0
        has_dict = False
        has_set = False
        has_sort = False

        for node in ast.walk(func_ast):
            if isinstance(node, (ast.For, ast.While)):
                loop_count += 1

            if isinstance(node, ast.Call):
                # Case: a.sort()
                if isinstance(node.func, ast.Attribute) and node.func.attr == "sort":
                    has_sort = True

                # Case: sort(a)
                if hasattr(node.func, "id") and node.func.id == "sort":
                    has_sort = True

            if isinstance(node, ast.Dict):
                has_dict = True

            if isinstance(node, ast.Set):
                has_set = True

        # Classification rules
        if loop_count >= 2:
            return "nested_loops"
        if has_dict or has_set:
            return "hash_heavy"
        if has_sort:
            return "sorting"
        if loop_count == 1:
            return "sequential"
        return "generic"

    # -------------------------------------------------
    # GENERATION DISPATCH
    # -------------------------------------------------
    @staticmethod
    def generate(pattern: str, n: int) -> Tuple[Any, ...]:
        """Generate synthetic input based on a structural pattern classification.

        Args:
            pattern (str): Pattern label returned by `_classify()`.
            n (int): Input size for synthetic data generation.

        Returns:
            Tuple[Any, ...]: Execution‑ready tuple of arguments.
        """
        if pattern == "scalar":
            return (n,)

        if pattern == "nested_loops":
            return (list(range(n)),)

        if pattern == "hash_heavy":
            return (AutoGen._hash_collision_array(n),)

        if pattern == "sorting":
            return (AutoGen._random_list(n),)

        if pattern == "sequential":
            return (AutoGen._sequential_string(n),)

        return (AutoGen._random_string(n),)

    # -------------------------------------------------
    # INPUT MODELS
    # -------------------------------------------------
    @staticmethod
    def _sequential_string(n: int) -> str:
        """Generate a deterministic sequential lowercase string.

        Args:
            n (int): Length of the string.

        Returns:
            str: A cyclic alphabetic sequence of length `n`.
        """
        return "".join(chr((i % 26) + 97) for i in range(n))

    @staticmethod
    def _random_string(n: int) -> str:
        """Generate a deterministic pseudo‑random lowercase string.

        Args:
            n (int): Length of the string.

        Returns:
            str: A reproducible pseudo‑random string of length `n`.
        """
        random.seed(n)
        return "".join(random.choice(string.ascii_lowercase) for _ in range(n))

    @staticmethod
    def _random_list(n: int) -> list:
        """Generate a deterministic pseudo‑random integer list.

        Args:
            n (int): Number of elements.

        Returns:
            list: A list of integers in the range [0, n].
        """
        return [random.randint(0, n) for _ in range(n)]

    @staticmethod
    def _hash_collision_array(n: int) -> list:
        """Generate a collision‑heavy integer array for hash‑based patterns.

        Args:
            n (int): Number of elements.

        Returns:
            list: A list engineered to produce frequent hash collisions.
        """
        return [i % max(1, n // 10) for i in range(n)]
