"""
Graph Data Structures.

Provides a lightweight, adjacency‑list–based undirected graph optimized
for algorithmic experimentation, teaching, and benchmarking. The graph
supports efficient edge insertion and adjacency iteration while
maintaining predictable memory usage proportional to ``V + E``.

Design Characteristics:
- Representation: Adjacency lists (space complexity O(V + E)).
- Performance:
    - Add edge: O(1)
    - Iterate adjacency: O(degree(v))
    - Check membership: O(degree(v))
- Self‑loops and parallel edges are permitted by default.

Classes:
    Graph: Undirected graph implemented using adjacency lists.
"""

from typing import List, Iterable


class Graph:
    """Undirected graph implemented using adjacency lists.

    Each vertex maintains a list of its adjacent vertices. The structure
    is optimized for sparse graphs and supports efficient adjacency
    iteration and constant‑time edge insertion.
    """

    def __init__(self, V: int):
        """Initializes an empty graph with ``V`` vertices and zero edges.

        Args:
            V (int): Number of vertices in the graph.

        Raises:
            ValueError: If ``V`` is negative.
        """
        if V < 0:
            raise ValueError("Number of vertices must be non-negative")

        self._V = V
        self._E = 0
        self._adj: List[List[int]] = [[] for _ in range(V)]

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

    def add_edge(self, v: int, w: int) -> None:
        """Adds an undirected edge between vertices ``v`` and ``w``.

        Both vertices must be valid indices in the range ``0`` to
        ``V - 1``. Parallel edges and self‑loops are allowed.

        Args:
            v (int): First vertex.
            w (int): Second vertex.

        Raises:
            IndexError: If either vertex index is out of bounds.
        """
        self._validate_vertex(v)
        self._validate_vertex(w)

        self._adj[v].append(w)
        self._adj[w].append(v)
        self._E += 1

    def adj(self, v: int) -> Iterable[int]:
        """Returns the vertices adjacent to ``v``.

        Args:
            v (int): The vertex whose neighbors are requested.

        Returns:
            Iterable[int]: A list of adjacent vertices.
        """
        self._validate_vertex(v)
        return self._adj[v]

    def degree(self, v: int) -> int:
        """Returns the degree of vertex ``v``.

        Args:
            v (int): The vertex whose degree is requested.

        Returns:
            int: Number of adjacent vertices.
        """
        self._validate_vertex(v)
        return len(self._adj[v])

    def _validate_vertex(self, v: int) -> None:
        """Validates that ``v`` is a legal vertex index.

        Args:
            v (int): Vertex index to validate.

        Raises:
            IndexError: If ``v`` is outside the valid range.
        """
        if v < 0 or v >= self._V:
            raise IndexError(f"Vertex {v} is not between 0 and {self._V - 1}")

    def __repr__(self) -> str:
        """Returns a string representation of the graph.

        The format lists each vertex followed by its adjacency list.

        Returns:
            str: Human‑readable representation of the graph.
        """
        lines = [f"{self._V} vertices, {self._E} edges\n"]
        for v in range(self._V):
            neighbors = " ".join(str(w) for w in self._adj[v])
            lines.append(f"{v}: {neighbors}\n")
        return "".join(lines)
