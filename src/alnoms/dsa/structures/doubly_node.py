"""
Doubly Linked Node.

Defines the node abstraction used in doubly linked data structures.
Each node stores a value and maintains references to both its successor
and predecessor, enabling bidirectional traversal with O(1) insertion
and removal at structural boundaries.

Classes:
    DoublyNode: Node representation for doubly linked structures.
"""

from typing import Optional, TypeVar

T = TypeVar("T")


class DoublyNode:
    """A node in a doubly linked structure.

    Stores a data value along with references to both the next and
    previous nodes in the sequence. This abstraction is used by
    doubly linked lists, deques, and other bidirectional structures.

    Attributes:
        data (T): The value stored in the node.
        next (Optional[DoublyNode]): Reference to the next node.
        prev (Optional[DoublyNode]): Reference to the previous node.
    """

    def __init__(self, data: T):
        """Initializes a doubly linked node with the given data.

        Args:
            data (T): The value to store in the node.
        """
        self.data = data
        self.next: Optional["DoublyNode"] = None
        self.prev: Optional["DoublyNode"] = None
