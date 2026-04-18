"""
Edge‑Weighted Directed Graph.

Provides a directed graph where each edge carries an associated weight.
The structure is implemented using adjacency lists, with each vertex
maintaining a list of outgoing ``DirectedEdge`` objects. This design
supports efficient adjacency iteration and constant‑time edge insertion.

Design Characteristics:
- Representation: Adjacency lists of ``DirectedEdge`` objects.
- Performance:
    - Add edge: O(1)
    - Iterate outgoing edges: O(outdegree(v))
- Parallel edges and self‑loops are permitted.

Classes:
    EdgeWeightedDigraph: Directed weighted graph backed by adjacency lists.
"""

from typing import List, Iterable
from .directed_edge import DirectedEdge


class EdgeWeightedDigraph:
    """Directed weighted graph implemented using adjacency lists.

    Each vertex maintains a list of outgoing ``DirectedEdge`` objects.
    The structure is suitable for shortest‑path algorithms such as
    Dijkstra, Bellman‑Ford, and DAG relaxations.
    """

    def __init__(self, V: int):
        """Initializes an empty edge‑weighted digraph with ``V`` vertices.

        Args:
            V (int): Number of vertices.

        Raises:
            ValueError: If ``V`` is negative.
        """
        if V < 0:
            raise ValueError("Number of vertices must be non-negative")

        self._V = V
        self._E = 0
        self._adj: List[List[DirectedEdge]] = [[] for _ in range(V)]

    def V(self) -> int:
        """Returns the number of vertices in the digraph.

        Returns:
            int: Total vertex count.
        """
        return self._V

    def E(self) -> int:
        """Returns the number of edges in the digraph.

        Returns:
            int: Total edge count.
        """
        return self._E

    def add_edge(self, e: DirectedEdge) -> None:
        """Adds a directed weighted edge to the digraph.

        The edge is inserted into the adjacency list of its source
        vertex. Parallel edges and self‑loops are allowed.

        Args:
            e (DirectedEdge): The edge to add.

        Raises:
            IndexError: If either endpoint is out of bounds.
        """
        v = e.from_vertex()
        w = e.to_vertex()

        self._validate_vertex(v)
        self._validate_vertex(w)

        self._adj[v].append(e)
        self._E += 1

    def adj(self, v: int) -> Iterable[DirectedEdge]:
        """Returns all outgoing edges from vertex ``v``.

        Args:
            v (int): The source vertex.

        Returns:
            Iterable[DirectedEdge]: Outgoing edges from ``v``.
        """
        self._validate_vertex(v)
        return self._adj[v]

    def edges(self) -> Iterable[DirectedEdge]:
        """Returns all edges in the digraph.

        Returns:
            Iterable[DirectedEdge]: All directed edges.
        """
        all_edges = []
        for v in range(self._V):
            all_edges.extend(self._adj[v])
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
