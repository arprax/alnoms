"""
Breadth‑First Search Paths.

Provides a breadth‑first search (BFS)–based shortest‑path finder for
undirected graphs. BFS computes the shortest path in terms of number of
edges from a designated source vertex to all reachable vertices.

Design Characteristics:
- Computes unweighted shortest paths
- Produces predecessor links and distance levels
- Time Complexity: O(V + E)
- Space Complexity: O(V)
"""

from typing import Iterable, Optional, Deque
from collections import deque

from alnoms.dsa.structures.graphs import Graph


class BreadthFirstPaths:
    """Computes BFS‑based shortest paths from a single source vertex.

    This class performs a breadth‑first search from a specified source
    vertex and records both predecessor links and distance levels. BFS
    guarantees shortest paths in unweighted graphs.

    Attributes:
        _s (int): The source vertex.
        _marked (List[bool]): Marks whether each vertex has been visited.
        _edge_to (List[int]): Predecessor links for path reconstruction.
        _dist_to (List[float]): Number of edges in the shortest path.
    """

    def __init__(self, G: Graph, s: int):
        """Initializes BFS search from a source vertex.

        Args:
            G (Graph): The graph to search.
            s (int): The source vertex.

        Raises:
            IndexError: If the source vertex is out of bounds.
        """
        self._s = s
        self._marked = [False] * G.V()
        self._edge_to = [0] * G.V()
        self._dist_to = [float("inf")] * G.V()

        self._validate_vertex(s, G.V())
        self._bfs(G, s)

    def _bfs(self, G: Graph, s: int) -> None:
        """Performs BFS from the source vertex.

        Args:
            G (Graph): The graph being searched.
            s (int): The source vertex.
        """
        q: Deque[int] = deque()
        self._marked[s] = True
        self._dist_to[s] = 0
        q.append(s)

        while q:
            v = q.popleft()
            for w in G.adj(v):
                if not self._marked[w]:
                    self._marked[w] = True
                    self._edge_to[w] = v
                    self._dist_to[w] = self._dist_to[v] + 1
                    q.append(w)

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

    def dist_to(self, v: int) -> float:
        """Returns the BFS shortest‑path distance to a vertex.

        Args:
            v (int): The vertex whose distance is requested.

        Returns:
            float: Number of edges in the shortest path.

        Raises:
            IndexError: If the vertex is out of bounds.
        """
        self._validate_vertex(v, len(self._marked))
        return self._dist_to[v]

    def path_to(self, v: int) -> Optional[Iterable[int]]:
        """Returns the shortest path from the source to a vertex.

        Args:
            v (int): The destination vertex.

        Returns:
            Optional[Iterable[int]]: A sequence of vertices forming the
            shortest path, or None if no path exists.

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
