"""
Alnoms Data Structure: FIFO Queue (Linked‑List Backed).

Provides a generic, type‑safe FIFO (First‑In First‑Out) queue
implementation using a singly linked list with explicit head and tail
references. This design guarantees O(1) enqueue and dequeue operations
without requiring array resizing or circular‑buffer bookkeeping.

The queue supports:

- O(1) enqueue at the tail
- O(1) dequeue from the head
- Safe iteration from front to back
- Deterministic memory behavior with no hidden reallocations

This module is part of the Alnoms OSS data‑structures suite and is
optimized for teaching, benchmarking, and algorithmic experimentation.
All operations are implemented with predictable worst‑case complexity.
"""

from typing import Optional, Iterator, TypeVar, Generic
from .node import Node

T = TypeVar("T")


class Queue(Generic[T]):
    """A FIFO (First‑In First‑Out) queue implemented using a linked list.

    This implementation maintains references to both the head (``_first``)
    and tail (``_last``) nodes, ensuring O(1) enqueue and dequeue
    operations. The queue grows dynamically without requiring array
    resizing, making it suitable for workloads requiring predictable
    constant‑time behavior.
    """

    def __init__(self):
        """Initializes an empty queue.

        Attributes:
            _first (Optional[Node]): Reference to the front of the queue.
            _last (Optional[Node]): Reference to the end of the queue.
            _n (int): Number of items currently stored.
        """
        self._first: Optional[Node] = None
        self._last: Optional[Node] = None
        self._n: int = 0

    def is_empty(self) -> bool:
        """Checks whether the queue is empty.

        Returns:
            bool: True if the queue contains no items, otherwise False.
        """
        return self._first is None

    def size(self) -> int:
        """Returns the number of items in the queue.

        Returns:
            int: The number of elements stored.
        """
        return self._n

    def enqueue(self, item: T) -> None:
        """Adds an item to the end of the queue.

        This operation runs in O(1) time by inserting a new node at the
        tail of the linked list.

        Args:
            item (T): The item to add to the queue.
        """
        old_last = self._last
        self._last = Node(item)
        self._last.next = None

        if self.is_empty():
            self._first = self._last
        else:
            old_last.next = self._last

        self._n += 1

    def dequeue(self) -> T:
        """Removes and returns the item at the front of the queue.

        This operation runs in O(1) time by removing the head node.

        Returns:
            T: The item previously at the front of the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue underflow")

        item = self._first.data
        self._first = self._first.next
        self._n -= 1

        if self.is_empty():
            self._last = None  # Avoid loitering

        return item

    def peek(self) -> T:
        """Returns the item at the front of the queue without removing it.

        Returns:
            T: The item currently at the front.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue underflow")
        return self._first.data

    def __iter__(self) -> Iterator[T]:
        """Iterates over the queue from front to back.

        Yields:
            T: Items in FIFO order, starting from the front.
        """
        current = self._first
        while current:
            yield current.data
            current = current.next
