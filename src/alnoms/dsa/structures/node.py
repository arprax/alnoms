"""
Alnoms: Linear Data Structures.

Provides foundational linear data structures optimized for predictable,
worst‑case performance. This module defines the core node abstraction
used across all linked data structures in the Alnoms ecosystem,
including lists, stacks, queues, and bags.

The design emphasizes:

- O(1) insertion and removal at structural boundaries
- Deterministic memory usage with no dynamic array resizing
- Simplicity suitable for teaching, benchmarking, and algorithmic analysis

Classes:
    Node: The fundamental building block for singly linked structures.
"""

from typing import Optional, TypeVar, Generic

T = TypeVar("T")


class Node(Generic[T]):
    """A node in a singly linked structure.

    Represents a single element in a linked list–based data structure.
    Each node stores a data value and a reference to the next node in
    the sequence.

    Attributes:
        data (T): The value stored in the node.
        next (Optional[Node[T]]): Reference to the next node, or None if
            this is the final node.
    """

    def __init__(self, data: T):
        """Initializes a node with the given data.

        Args:
            data (T): The value to store in the node.
        """
        self.data = data
        self.next: Optional["Node[T]"] = None
