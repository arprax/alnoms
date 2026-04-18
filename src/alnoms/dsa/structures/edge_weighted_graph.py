"""
Edge‑Weighted Graph.

Provides an undirected graph where each edge carries an associated
weight. This structure is used in classical graph algorithms such as
Minimum Spanning Trees (MST) and Shortest Paths. The graph is stored
using adjacency lists, with each vertex maintaining a list of incident
weighted edges.

Design Characteristics:
- Representation: Adjacency lists of ``Edge`` objects.
- Performance:
    - Add edge: O(1)
    - Iterate adjacency: O(degree(v))
- Parallel edges and self‑loops are permitted.

Classes:
    EdgeWeightedGraph: Undirected weighted graph backed by adjacency lists.
"""

from typing import List, Iterable
from alnoms.dsa.structures.edge import Edge


class EdgeWeightedGraph:
    """Undirected weighted graph implemented using adjacency lists.

    Each vertex maintains a list of incident ``Edge`` objects. The graph
    supports efficient adjacency iteration and constant‑time edge
    insertion. This structure is suitable for MST and shortest‑path
    algorithms that operate on weighted graphs.
    """

    def __init__(self, V: int):
        """Initializes an empty weighted graph with ``V`` vertices.

        Args:
            V (int): Number of vertices.

        Raises:
            ValueError: If ``V`` is negative.
        """
        if V < 0:
            raise ValueError("Number of vertices must be non-negative")

        self._V = V
        self._E = 0
        self._adj: List[List[Edge]] = [[] for _ in range(V)]

    def V(self) -> int:
        """Returns the number of vertices in the graph.

        Returns:
            int: Total vertex count.
        """
        return self._V

    def E(self) -> int:
        """Returns the number of edges in the graph.

        Returns:
            int: Total edge count.
        """
        return self._E

    def add_edge(self, e: Edge) -> None:
        """Adds a weighted undirected edge to the graph.

        The edge is inserted into the adjacency lists of both endpoints.
        Parallel edges and self‑loops are allowed.

        Args:
            e (Edge): The edge to add.

        Raises:
            IndexError: If either endpoint is out of bounds.
        """
        v = e.either()
        w = e.other(v)

        self._validate_vertex(v)
        self._validate_vertex(w)

        self._adj[v].append(e)
        self._adj[w].append(e)
        self._E += 1

    def adj(self, v: int) -> Iterable[Edge]:
        """Returns all weighted edges incident to vertex ``v``.

        Args:
            v (int): The vertex whose incident edges are requested.

        Returns:
            Iterable[Edge]: List of edges adjacent to ``v``.
        """
        self._validate_vertex(v)
        return self._adj[v]

    def edges(self) -> Iterable[Edge]:
        """Returns all edges in the graph without duplicates.

        For each undirected edge, only the instance where the opposite
        endpoint is greater than the current vertex is included.

        Returns:
            Iterable[Edge]: All unique edges in the graph.
        """
        all_edges = []
        for v in range(self._V):
            for e in self._adj[v]:
                if e.other(v) > v:
                    all_edges.append(e)
        return all_edges

    def _validate_vertex(self, v: int) -> None:
        """Validates that ``v`` is a legal vertex index.

        Args:
            v (int): Vertex index to validate.

        Raises:
            IndexError: If ``v`` is outside the valid range.
        """
        if v < 0 or v >= self._V:
            raise IndexError(f"Vertex {v} is not between 0 and {self._V - 1}")
