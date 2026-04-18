"""
Depth‑First Search Paths.

Provides a depth‑first search (DFS)–based path finder for undirected
graphs. Starting from a designated source vertex, the algorithm explores
all reachable vertices and records predecessor links that allow path
reconstruction.

Design Characteristics:
- Computes reachability from a single source
- Produces DFS tree predecessor links
- Paths are not guaranteed to be shortest
- Time Complexity: O(V + E)
- Space Complexity: O(V)
"""

from typing import Iterable, Optional, Deque
from collections import deque

from alnoms.dsa.structures.graphs import Graph


class DepthFirstPaths:
    """Computes DFS‑based paths from a single source vertex.

    This class performs a depth‑first search from a specified source
    vertex and records the predecessor of each visited vertex. These
    predecessor links allow reconstruction of any path from the source
    to a reachable vertex.

    Attributes:
        _s (int): The source vertex.
        _marked (List[bool]): Marks whether each vertex has been visited.
        _edge_to (List[int]): Predecessor links for path reconstruction.
    """

    def __init__(self, G: Graph, s: int):
        """Initializes DFS search from a source vertex.

        Args:
            G (Graph): The graph to search.
            s (int): The source vertex.

        Raises:
            IndexError: If the source vertex is out of bounds.
        """
        self._s = s
        self._marked = [False] * G.V()
        self._edge_to = [0] * G.V()

        self._validate_vertex(s, G.V())
        self._dfs(G, s)

    def _dfs(self, G: Graph, v: int) -> None:
        """Performs recursive DFS from a vertex.

        Args:
            G (Graph): The graph being searched.
            v (int): The current vertex.
        """
        self._marked[v] = True
        for w in G.adj(v):
            if not self._marked[w]:
                self._edge_to[w] = v
                self._dfs(G, w)

    def has_path_to(self, v: int) -> bool:
        """Checks whether a path exists from the source to a vertex.

        Args:
            v (int): The vertex to check.

        Returns:
            bool: True if reachable, otherwise False.

        Raises:
            IndexError: If the vertex is out of bounds.
        """
        self._validate_vertex(v, len(self._marked))
        return self._marked[v]

    def path_to(self, v: int) -> Optional[Iterable[int]]:
        """Returns a path from the source to a vertex.

        Args:
            v (int): The destination vertex.

        Returns:
            Optional[Iterable[int]]: A sequence of vertices forming a path
            from the source to `v`, or None if no such path exists.

        Raises:
            IndexError: If the vertex is out of bounds.
        """
        self._validate_vertex(v, len(self._marked))
        if not self.has_path_to(v):
            return None

        path: Deque[int] = deque()
        x = v
        while x != self._s:
            path.appendleft(x)
            x = self._edge_to[x]
        path.appendleft(self._s)
        return path

    def _validate_vertex(self, v: int, V: int) -> None:
        """Validates that a vertex index is within bounds.

        Args:
            v (int): The vertex to validate.
            V (int): Total number of vertices.

        Raises:
            IndexError: If the vertex is out of bounds.
        """
        if v < 0 or v >= V:
            raise IndexError(f"Vertex {v} is out of bounds")
