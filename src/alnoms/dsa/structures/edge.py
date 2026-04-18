"""
Weighted Edge Abstraction.

Defines a lightweight representation of an undirected weighted edge.
Each edge connects two vertices and stores an associated weight. The
class provides comparison operators to support sorting, which is useful
in algorithms such as Kruskal's MST.

Classes:
    Edge: Undirected weighted edge with comparison support.
"""


class Edge:
    """Represents an undirected weighted edge.

    Each edge connects two vertices ``v`` and ``w`` and stores a numeric
    weight. The class supports comparison based on weight, enabling its
    use in priority queues, sorting routines, and MST algorithms.

    Attributes:
        _v (int): One endpoint of the edge.
        _w (int): The other endpoint of the edge.
        _weight (float): Weight associated with the edge.
    """

    def __init__(self, v: int, w: int, weight: float):
        """Initializes a weighted edge between vertices ``v`` and ``w``.

        Args:
            v (int): First endpoint.
            w (int): Second endpoint.
            weight (float): Weight of the edge.
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

    def either(self) -> int:
        """Returns one endpoint of the edge.

        Returns:
            int: One of the two endpoints.
        """
        return self._v

    def other(self, vertex: int) -> int:
        """Returns the opposite endpoint of the edge.

        Args:
            vertex (int): One endpoint of the edge.

        Returns:
            int: The other endpoint.

        Raises:
            ValueError: If ``vertex`` is not one of the endpoints.
        """
        if vertex == self._v:
            return self._w
        if vertex == self._w:
            return self._v
        raise ValueError("Illegal endpoint")

    def __lt__(self, other: "Edge") -> bool:
        """Compares this edge with another based on weight.

        Args:
            other (Edge): The edge to compare against.

        Returns:
            bool: True if this edge has a smaller weight.
        """
        return self.weight < other.weight

    def __str__(self) -> str:
        """Returns a human‑readable string representation of the edge.

        Returns:
            str: Formatted as ``v-w weight``.
        """
        return f"{self._v}-{self._w} {self._weight:.2f}"
