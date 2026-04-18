"""
Directed Weighted Edge.

Defines an immutable representation of a weighted directed edge. Each
edge stores a source vertex, a destination vertex, and a numeric weight.
This abstraction is used by edge‑weighted digraphs and shortest‑path
algorithms.

Classes:
    DirectedEdge: Immutable weighted directed edge.
"""


class DirectedEdge:
    """Represents a weighted edge in a directed graph.

    The edge is immutable and stores a source vertex, a destination
    vertex, and an associated weight. This abstraction is used in
    shortest‑path algorithms and edge‑weighted digraphs.

    Attributes:
        _v (int): Source vertex.
        _w (int): Destination vertex.
        _weight (float): Weight of the directed edge.
    """

    def __init__(self, v: int, w: int, weight: float):
        """Initializes a directed edge from ``v`` to ``w`` with a weight.

        Args:
            v (int): The source vertex.
            w (int): The destination vertex.
            weight (float): The weight of the edge.
        """
        self._v = v
        self._w = w
        self._weight = weight

    @property
    def weight(self) -> float:
        """Returns the weight of the edge.

        Returns:
            float: The edge weight.
        """
        return self._weight

    def from_vertex(self) -> int:
        """Returns the source (tail) vertex of the directed edge.

        Returns:
            int: The source vertex.
        """
        return self._v

    def to_vertex(self) -> int:
        """Returns the destination (head) vertex of the directed edge.

        Returns:
            int: The destination vertex.
        """
        return self._w

    def __str__(self) -> str:
        """Returns a human‑readable string representation of the edge.

        Returns:
            str: Formatted as ``v->w weight``.
        """
        return f"{self._v}->{self._w} {self._weight:.2f}"
