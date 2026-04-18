"""
Depth‑First Search Orderings.

Computes preorder, postorder, and reverse‑postorder vertex orderings for
a directed graph using depth‑first search (DFS). These orderings are
fundamental in algorithms such as topological sorting and strongly
connected components.

Design Characteristics:
- DFS‑based vertex ordering
- Reverse postorder supports topological sorting in DAGs
- Time Complexity: O(V + E)
- Space Complexity: O(V)
"""

from typing import Iterable, Deque
from collections import deque

from alnoms.dsa.structures.digraph import Digraph


class DepthFirstOrder:
    """Computes DFS‑based vertex orderings for a directed graph.

    This class performs a full DFS over all vertices of a directed graph
    and records the reverse postorder sequence. Reverse postorder is
    particularly useful for topological sorting in directed acyclic
    graphs (DAGs).

    Attributes:
        _marked (List[bool]): Marks whether each vertex has been visited.
        _reverse_post (Deque[int]): Vertices in reverse postorder.
    """

    def __init__(self, G: Digraph):
        """Initializes DFS order computation.

        Args:
            G (Digraph): The directed graph whose orderings are computed.
        """
        self._marked = [False] * G.V()
        self._reverse_post: Deque[int] = deque()

        for v in range(G.V()):
            if not self._marked[v]:
                self._dfs(G, v)

    def _dfs(self, G: Digraph, v: int) -> None:
        """Performs DFS from a vertex and records postorder.

        Args:
            G (Digraph): The graph being searched.
            v (int): The current vertex.
        """
        self._marked[v] = True
        for w in G.adj(v):
            if not self._marked[w]:
                self._dfs(G, w)

        # Postorder: add after exploring all descendants
        self._reverse_post.appendleft(v)

    def reverse_post(self) -> Iterable[int]:
        """Returns vertices in reverse postorder.

        Returns:
            Iterable[int]: A sequence of vertices in reverse postorder.
        """
        return self._reverse_post
