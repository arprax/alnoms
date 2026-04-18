"""
Directed Graph (Digraph).

Defines a lightweight adjacency‑list–based directed graph. Each vertex
maintains a list of outgoing edges, and indegree counts are tracked
explicitly. The structure supports efficient adjacency iteration,
constant‑time edge insertion, and construction of the graph's reverse.

Design Characteristics:
- Representation: Adjacency lists of integers.
- Performance:
    - Add edge: O(1)
    - Iterate outgoing edges: O(outdegree(v))
    - Compute reverse graph: O(V + E)
- Self‑loops and parallel edges are permitted.

Classes:
    Digraph: Directed graph with adjacency lists and indegree tracking.
"""

from typing import List, Iterable


class Digraph:
    """Directed graph implemented using adjacency lists.

    Each vertex maintains a list of outgoing edges. Indegree counts are
    stored explicitly to support algorithms that rely on incoming edge
    information. The structure is suitable for topological sorting,
    SCC algorithms, and general directed graph processing.
    """

    def __init__(self, V: int):
        """Initializes an empty digraph with ``V`` vertices.

        Args:
            V (int): Number of vertices.

        Raises:
            ValueError: If ``V`` is negative.
        """
        if V < 0:
            raise ValueError("Number of vertices must be non-negative")

        self._V = V
        self._E = 0
        self._adj: List[List[int]] = [[] for _ in range(V)]
        self._indegree: List[int] = [0] * V

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

    def add_edge(self, v: int, w: int) -> None:
        """Adds a directed edge from ``v`` to ``w``.

        Args:
            v (int): Source vertex.
            w (int): Destination vertex.

        Raises:
            IndexError: If either vertex index is out of bounds.
        """
        self._validate_vertex(v)
        self._validate_vertex(w)

        self._adj[v].append(w)
        self._indegree[w] += 1
        self._E += 1

    def adj(self, v: int) -> Iterable[int]:
        """Returns all vertices reachable from ``v`` via outgoing edges.

        Args:
            v (int): The source vertex.

        Returns:
            Iterable[int]: Outgoing neighbors of ``v``.
        """
        self._validate_vertex(v)
        return self._adj[v]

    def out_degree(self, v: int) -> int:
        """Returns the number of edges leaving vertex ``v``.

        Args:
            v (int): The vertex.

        Returns:
            int: Outdegree of ``v``.
        """
        self._validate_vertex(v)
        return len(self._adj[v])

    def in_degree(self, v: int) -> int:
        """Returns the number of edges entering vertex ``v``.

        Args:
            v (int): The vertex.

        Returns:
            int: Indegree of ``v``.
        """
        self._validate_vertex(v)
        return self._indegree[v]

    def reverse(self) -> "Digraph":
        """Returns a new digraph with all edges reversed.

        Useful for algorithms such as strongly connected components (SCC)
        where reverse graph traversal is required.

        Returns:
            Digraph: A new digraph with reversed edge directions.
        """
        R = Digraph(self._V)
        for v in range(self._V):
            for w in self._adj[v]:
                R.add_edge(w, v)
        return R

    def _validate_vertex(self, v: int) -> None:
        """Validates that ``v`` is a legal vertex index.

        Args:
            v (int): Vertex index to validate.

        Raises:
            IndexError: If ``v`` is outside the valid range.
        """
        if v < 0 or v >= self._V:
            raise IndexError(f"Vertex {v} is not between 0 and {self._V - 1}")
