"""
Topological Sorting.

Provides a topological ordering of a directed acyclic graph (DAG) using
depth‑first search finishing times. The implementation relies on the
reverse postorder of a DFS traversal. If the graph contains a cycle, the
resulting order is not a valid topological sort, but the algorithm still
produces an ordering based on DFS structure.

Design Characteristics:
- O(V + E) time
- Uses DFS reverse‑postorder
- Assumes the input graph is a DAG unless validated externally

Classes:
    Topological: Computes a topological order of a directed graph.
"""

from typing import Iterable, Optional
from alnoms.dsa.structures.digraph import Digraph
from alnoms.dsa.algorithms.graph.depth_first_order import DepthFirstOrder


class Topological:
    """Computes a topological order of a directed graph.

    The ordering is derived from the reverse postorder of a depth‑first
    search. This yields a valid topological order if and only if the
    graph is acyclic. Cycle detection is not performed here; callers
    should validate DAG properties externally if correctness is required.
    """

    def __init__(self, G: Digraph):
        """Initializes the topological sort computation.

        Args:
            G (Digraph): Directed graph on which to compute the ordering.
        """
        finder = DepthFirstOrder(G)
        self._order: Optional[Iterable[int]] = finder.reverse_post()

    def has_order(self) -> bool:
        """Indicates whether a topological order is available.

        Returns:
            bool: True if an order was computed. This does not guarantee
            that the graph is acyclic; it only reflects that an ordering
            exists based on DFS finishing times.
        """
        return self._order is not None

    def order(self) -> Iterable[int]:
        """Returns the computed topological order.

        Returns:
            Iterable[int]: Vertices in topological order.
        """
        return self._order
