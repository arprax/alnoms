"""
Dijkstra's Shortest Paths.

Implements the single‑source shortest‑path algorithm for edge‑weighted
directed graphs with non‑negative edge weights. The algorithm computes
the shortest path tree rooted at a specified source vertex using a
binary heap–based priority queue.

Design Characteristics:
- Supports arbitrary directed graphs with non‑negative weights
- Produces shortest‑path distances and predecessor edges
- Uses lazy deletion in the priority queue
- Time Complexity: O(E log V)
- Space Complexity: O(V)
"""

from typing import List, Iterable, Optional, Deque
from collections import deque
import heapq

from alnoms.dsa.structures.edge_weighted_digraph import EdgeWeightedDigraph
from alnoms.dsa.structures.directed_edge import DirectedEdge


class DijkstraSP:
    """Computes shortest paths in a weighted directed graph.

    This class computes the shortest path from a single source vertex to
    all other vertices in an edge‑weighted digraph with non‑negative edge
    weights. Distances and predecessor edges are stored for subsequent
    queries.

    Attributes:
        _dist_to (List[float]): Shortest known distance to each vertex.
        _edge_to (List[Optional[DirectedEdge]]): Last edge on the shortest
            known path to each vertex.
        _pq (List[tuple]): Min‑heap storing (distance, vertex) pairs.
    """

    def __init__(self, G: EdgeWeightedDigraph, s: int):
        """Initializes the shortest‑path computation from a source vertex.

        Args:
            G (EdgeWeightedDigraph): The input directed graph.
            s (int): The source vertex.

        Raises:
            ValueError: If any edge in the graph has a negative weight.
        """
        self._validate_edges(G)

        self._dist_to = [float("inf")] * G.V()
        self._edge_to: List[Optional[DirectedEdge]] = [None] * G.V()
        self._pq: List[tuple] = []

        self._dist_to[s] = 0.0
        heapq.heappush(self._pq, (0.0, s))

        while self._pq:
            dist, v = heapq.heappop(self._pq)

            # Skip stale entries
            if dist > self._dist_to[v]:
                continue

            for e in G.adj(v):
                self._relax(e)

    def _relax(self, e: DirectedEdge) -> None:
        """Relaxes an edge and updates state if a shorter path is found.

        Args:
            e (DirectedEdge): The directed edge to relax.
        """
        v, w = e.from_vertex(), e.to_vertex()
        new_dist = self._dist_to[v] + e.weight

        if self._dist_to[w] > new_dist:
            self._dist_to[w] = new_dist
            self._edge_to[w] = e
            heapq.heappush(self._pq, (new_dist, w))

    def _validate_edges(self, G: EdgeWeightedDigraph) -> None:
        """Ensures that the graph contains no negative‑weight edges.

        Args:
            G (EdgeWeightedDigraph): The graph to validate.

        Raises:
            ValueError: If any edge weight is negative.
        """
        for e in G.edges():
            if e.weight < 0:
                raise ValueError(f"Edge has negative weight: {e}")

    def has_path_to(self, v: int) -> bool:
        """Checks whether a path exists from the source to a vertex.

        Args:
            v (int): The vertex to check.

        Returns:
            bool: True if a path exists, otherwise False.
        """
        return self._dist_to[v] < float("inf")

    def dist_to(self, v: int) -> float:
        """Returns the shortest‑path distance to a vertex.

        Args:
            v (int): The vertex whose distance is requested.

        Returns:
            float: The shortest distance, or infinity if unreachable.
        """
        return self._dist_to[v]

    def path_to(self, v: int) -> Optional[Iterable[DirectedEdge]]:
        """Returns the shortest path from the source to a vertex.

        Args:
            v (int): The destination vertex.

        Returns:
            Optional[Iterable[DirectedEdge]]: A sequence of edges forming
            the shortest path, or None if no path exists.
        """
        if not self.has_path_to(v):
            return None

        path: Deque[DirectedEdge] = deque()
        e = self._edge_to[v]

        while e is not None:
            path.appendleft(e)
            e = self._edge_to[e.from_vertex()]

        return path
