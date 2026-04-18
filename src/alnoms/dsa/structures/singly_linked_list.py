"""
Singly Linked List (Foundational Data Structure).

Provides a minimal, textbook‑grade implementation of a singly linked list
supporting O(1) insertions at the head and linear‑time traversal. This
structure is useful for workloads requiring predictable insertion
performance without the resizing overhead of array‑backed lists.

Features:
    • O(1) insertion at the head
    • Linear‑time traversal and search
    • Node‑based dynamic memory allocation
    • Pythonic iteration support

This module is part of the Alnoms Data Structures suite and is designed
for clarity, determinism, and mkdocstrings‑compatible documentation.
"""

from typing import Any, Optional, Iterator, TypeVar
from .node import Node

T = TypeVar("T")


class SinglyLinkedList:
    """A foundational singly linked list implementation.

    This structure supports O(1) insertions at the head and linear-time
    traversal from head to tail. It is suitable for workloads requiring
    predictable insertion performance without the resizing overhead of
    array-backed lists.
    """

    def __init__(self):
        """Initializes an empty singly linked list.

        Attributes:
            head (Optional[Node]): Reference to the first node in the list.
            _size (int): Number of nodes currently stored.
        """
        self.head: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        """Returns the number of nodes in the list.

        Returns:
            int: The total number of elements.
        """
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Iterates through the list from head to tail.

        Yields:
            Any: The data stored in each node.
        """
        current = self.head
        while current:
            yield current.data
            current = current.next

    def is_empty(self) -> bool:
        """Checks whether the list contains any elements.

        Returns:
            bool: True if the list is empty, otherwise False.
        """
        return self.head is None

    def insert_at_head(self, data: Any) -> None:
        """Inserts a new node at the beginning of the list.

        This operation runs in O(1) time by updating the head pointer.

        Args:
            data (Any): The value to insert.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def append(self, data: Any) -> None:
        """Appends a new node to the end of the list.

        This operation runs in O(N) time due to the need to traverse
        to the tail.

        Args:
            data (Any): The value to append.
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self._size += 1
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node
        self._size += 1

    def remove(self, data: Any) -> bool:
        """Removes the first occurrence of a value from the list.

        This operation runs in O(N) time due to linear search.

        Args:
            data (Any): The value to remove.

        Returns:
            bool: True if a node was removed, otherwise False.
        """
        if not self.head:
            return False

        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next

        return False

    def display(self) -> str:
        """Returns a string representation of the list.

        Useful for debugging and visualization.

        Returns:
            str: A formatted representation such as ``"1 -> 2 -> NULL"``.
        """
        elements = [str(data) for data in self]
        return " -> ".join(elements) + " -> NULL" if elements else "EMPTY"
