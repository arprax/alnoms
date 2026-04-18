"""
Bag (Unordered Collection).

Defines a lightweight collection type that supports insertion but does
not support removal. A Bag is useful for collecting items and iterating
over them without imposing any ordering guarantees. Internally, the Bag
is backed by a singly linked list, enabling O(1) insertion.

Design Characteristics:
- Unordered collection
- O(1) insertion at the front
- O(N) iteration
- No removal operations

Classes:
    Bag: A simple unordered collection supporting fast insertion.
"""

from typing import Optional, Iterator, TypeVar, Generic
from .node import Node

T = TypeVar("T")


class Bag(Generic[T]):
    """An unordered collection supporting fast insertion.

    Items are stored in a singly linked list. The Bag does not support
    removal; its purpose is to collect items and allow iteration over
    them. The iteration order is LIFO due to front insertion, but the
    order is not semantically meaningful.
    """

    def __init__(self):
        """Initializes an empty Bag.

        Attributes:
            _first (Optional[Node]): Reference to the first node.
            _n (int): Number of items stored.
        """
        self._first: Optional[Node] = None
        self._n: int = 0

    def is_empty(self) -> bool:
        """Checks whether the Bag is empty.

        Returns:
            bool: True if the Bag contains no items.
        """
        return self._first is None

    def size(self) -> int:
        """Returns the number of items in the Bag.

        Returns:
            int: Total number of stored items.
        """
        return self._n

    def add(self, item: T) -> None:
        """Adds an item to the Bag.

        This operation runs in O(1) time by inserting the new item at the
        front of the linked list.

        Args:
            item (T): The item to add.
        """
        old_first = self._first
        self._first = Node(item)
        self._first.next = old_first
        self._n += 1

    def __iter__(self) -> Iterator[T]:
        """Iterates over the items in the Bag.

        Yields:
            T: Items stored in the Bag. Order is LIFO but not meaningful.
        """
        current = self._first
        while current:
            yield current.data
            current = current.next
