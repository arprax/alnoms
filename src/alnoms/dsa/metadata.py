"""
Alnoms: Sovereign Algorithmic Metadata Registry.

Serves as the central registry for algorithmic Big‑O profiles across all
Alnoms tiers (OSS, PRO, ENTERPRISE). This registry acts as the authoritative
mapping between algorithm names, their complexity classes, categories, and
module implementations within the Alnoms Algorithmic Pharmacy.
"""

from typing import Dict, Any, List


class MetadataRegistry:
    """Industrial registry for algorithmic Big‑O metadata.

    This class maintains a unified, tier‑aware registry of algorithmic
    complexity profiles. It functions as the *Single Source of Truth* for
    the Alnoms Pharmacy, enabling detectors, fixers, governance engines,
    and CLI tools to retrieve consistent metadata about algorithms,
    optimization strategies, and conceptual patterns.

    The registry supports:
        • Complexity lookup
        • Tier‑based filtering (OSS / PRO / ENTERPRISE)
        • Category‑based organization
        • Conceptual optimization stubs for OSS education
    """

    _REGISTRY = {
        # ==============================================================
        # Sorting
        # ==============================================================
        "bubble_sort": {
            "complexity": "O(n²)",
            "tier": "OSS",
            "category": "sorting",
            "module": "dsa.algorithms.sorting.BubbleSort",
        },
        "insertion_sort": {
            "complexity": "O(n²)",
            "tier": "OSS",
            "category": "sorting",
            "module": "dsa.algorithms.sorting.InsertionSort",
        },
        "selection_sort": {
            "complexity": "O(n²)",
            "tier": "OSS",
            "category": "sorting",
            "module": "dsa.algorithms.sorting.SelectionSort",
        },
        "merge_sort": {
            "complexity": "O(n log n)",
            "tier": "OSS",
            "category": "sorting",
            "module": "dsa.algorithms.sorting.MergeSort",
        },
        "quick_sort": {
            "complexity": "O(n log n)",
            "tier": "OSS",
            "category": "sorting",
            "module": "dsa.algorithms.sorting.QuickSort",
        },
        "shell_sort": {
            "complexity": "O(N¹·⁵)",
            "tier": "ENTERPRISE",
            "category": "sorting",
            "module": "alnoms_enterprise.dsa.algorithms.sorting.shell_sort",
        },
        "heap_sort": {
            "complexity": "O(N log N)",
            "tier": "ENTERPRISE",
            "category": "sorting",
            "module": "alnoms_enterprise.dsa.algorithms.sorting.heap_sort",
        },
        # ==============================================================
        # Searching
        # ==============================================================
        "binary_search": {
            "complexity": "O(log n)",
            "tier": "OSS",
            "category": "searching",
            "module": "dsa.algorithms.searching.BinarySearch",
        },
        "quick_select": {
            "complexity": "O(N)",
            "tier": "PRO",
            "category": "searching",
            "module": "alnoms_pro.dsa.algorithms.searching.quick_select",
        },
        # ==============================================================
        # Pointers
        # ==============================================================
        "has_cycle": {
            "complexity": "O(n)",
            "tier": "OSS",
            "category": "pointers",
            "module": "dsa.algorithms.pointers.CycleDetector",
        },
        "find_cycle_start": {
            "complexity": "O(N)",
            "tier": "PRO",
            "category": "pointers",
            "module": "alnoms_pro.dsa.algorithms.pointers.find_cycle_start",
        },
        # ==============================================================
        # Graph Algorithms
        # ==============================================================
        "bfs_paths": {
            "complexity": "O(V + E)",
            "tier": "OSS",
            "category": "graph",
            "module": "dsa.algorithms.graph.BreadthFirstPaths",
        },
        "dfs_paths": {
            "complexity": "O(V + E)",
            "tier": "OSS",
            "category": "graph",
            "module": "dsa.algorithms.graph.DepthFirstPaths",
        },
        "dfs_order": {
            "complexity": "O(V + E)",
            "tier": "OSS",
            "category": "graph",
            "module": "dsa.algorithms.graph.DepthFirstOrder",
        },
        "dijkstra": {
            "complexity": "O(E log V)",
            "tier": "OSS",
            "category": "graph",
            "module": "dsa.algorithms.graph.DijkstraSP",
        },
        "topological": {
            "complexity": "O(V + E)",
            "tier": "OSS",
            "category": "graph",
            "module": "dsa.algorithms.graph.Topological",
        },
        "bellman_ford": {
            "complexity": "O(V * E)",
            "tier": "ENTERPRISE",
            "category": "graph",
            "module": "alnoms_enterprise.dsa.algorithms.graph.bellman_ford_sp",
        },
        # ==============================================================
        # Structures
        # ==============================================================
        "stack": {
            "complexity": "O(1)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.Stack",
        },
        "queue": {
            "complexity": "O(1)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.Queue",
        },
        "bag": {
            "complexity": "O(1)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.Bag",
        },
        "singly_linked_list": {
            "complexity": "O(n)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.SinglyLinkedList",
        },
        "doubly_linked_list": {
            "complexity": "O(n)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.DoublyLinkedList",
        },
        "graph": {
            "complexity": "O(V + E)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.Graph",
        },
        "digraph": {
            "complexity": "O(V + E)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.Digraph",
        },
        "edge_weighted_graph": {
            "complexity": "O(E log V)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.EdgeWeightedGraph",
        },
        "edge_weighted_digraph": {
            "complexity": "O(E log V)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.EdgeWeightedDigraph",
        },
        "directed_edge": {
            "complexity": "O(1)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.DirectedEdge",
        },
        "edge": {
            "complexity": "O(1)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.Edge",
        },
        "bst_search": {
            "complexity": "O(log N) Avg",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.BinarySearchTree",
        },
        "separate_chaining_hash": {
            "complexity": "O(N/M)",
            "tier": "OSS",
            "category": "structure",
            "module": "dsa.structures.SeparateChainingHashST",
        },
        "linear_probing_hash": {
            "complexity": "O(1) Avg",
            "tier": "PRO",
            "category": "structures",
            "module": "alnoms_pro.dsa.structures.linear_probing_hash_st",
        },
        "red_black_bst": {
            "complexity": "O(log N) Guaranteed",
            "tier": "PRO",
            "category": "structures",
            "module": "alnoms_pro.dsa.structures.red_black_bst",
        },
        # --- lookup optimization ---
        "membership_test": {
            "category": "lookup",
            "tier": "OSS",
            "module": "builtin.set",
        },
        # --- optimization strategies (OSS stubs) ---
        "separate_chaining_hash_st": {
            "category": "hashing",
            "tier": "OSS",
            "module": "alnoms.dsa.structures.separate_chaining_hash_st",
        },
        "graph_traversal": {
            "category": "graph",
            "tier": "OSS",
            "module": None,  # conceptual, leave None
        },
        "pruning": {
            "category": "optimization",
            "tier": "OSS",
            "module": None,  # conceptual, leave None
        },
        "list_concat": {
            "category": "string/list building",
            "tier": "OSS",
            "module": "builtin.join",
        },
        "memoization": {
            "category": "caching",
            "tier": "OSS",
            "module": "functools.lru_cache",
        },
        "buffered_io": {"category": "io", "tier": "OSS", "module": "io.BufferedReader"},
    }

    @classmethod
    def get_metadata(cls, algo_name: str) -> Dict[str, Any]:
        """Retrieves metadata for a given algorithm or optimization concept.

        Args:
            algo_name (str): The canonical name of the algorithm or concept
                (e.g., ``"merge_sort"``, ``"binary_search"``, ``"memoization"``).

        Returns:
            Dict[str, Any]: A metadata dictionary containing:
                - ``complexity`` (str): Big‑O time complexity.
                - ``tier`` (str): OSS / PRO / ENTERPRISE.
                - ``category`` (str): Algorithmic domain.
                - ``module`` (str | None): Import path or conceptual placeholder.

            If the algorithm is unknown, a default OSS metadata entry is returned.
        """
        return cls._REGISTRY.get(
            algo_name,
            {
                "complexity": "Unknown",
                "tier": "OSS",
                "category": "general",
                "module": None,
            },
        )

    @classmethod
    def list_available_algorithms(cls, tier: str = "OSS") -> List[str]:
        """Lists algorithms filtered by access tier.

        Args:
            tier (str): The tier to filter by. Supported values:
                ``"OSS"``, ``"PRO"``, ``"ENTERPRISE"``, or ``"ALL"``.

        Returns:
            List[str]: A list of algorithm names available at the specified tier.
            When ``tier="ALL"``, all registry keys are returned.
        """
        if tier.upper() == "ALL":
            return list(cls._REGISTRY.keys())
        return [
            k for k, v in cls._REGISTRY.items() if v["tier"].upper() == tier.upper()
        ]

    @classmethod
    def get_all(cls) -> Dict[str, Dict[str, Any]]:
        """Returns the full Sovereign Registry.

        Returns:
            Dict[str, Dict[str, Any]]: The complete algorithmic metadata
            registry, including OSS, PRO, ENTERPRISE, and conceptual entries.
        """
        return cls._REGISTRY
