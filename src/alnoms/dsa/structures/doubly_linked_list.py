"""
Doubly Linked List.

Provides a bidirectional linked list supporting O(1) insertion at both
the head and tail. Each node maintains references to its predecessor and
successor, enabling efficient traversal and structural updates.

Design Characteristics:
- Bidirectional traversal
- O(1) prepend and append
- O(N) search and removal
- Deterministic memory behavior

Classes:
    DoublyLinkedList: A doubly linked list supporting head/tail operations.
"""

from typing import Any, Optional, Iterator, TypeVar, Generic
from .doubly_node import DoublyNode

T = TypeVar("T")


class DoublyLinkedList(Generic[T]):
    """A doubly linked list supporting bidirectional traversal.

    The list maintains references to both the head and tail nodes,
    enabling O(1) insertion at either end. Removal of arbitrary values
    runs in O(N) time due to linear search.
    """

    def __init__(self):
        """Initializes an empty doubly linked list.

        Attributes:
            head (Optional[DoublyNode]): First node in the list.
            tail (Optional[DoublyNode]): Last node in the list.
            _size (int): Number of nodes in the list.
        """
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        """Returns the number of nodes in the list.

        Returns:
            int: The size of the list.
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
        """Checks whether the list is empty.

        Returns:
            bool: True if the list contains no elements.
        """
        return self.head is None

    def append(self, data: Any) -> None:
        """Appends a node to the end of the list.

        This operation runs in O(1) time.

        Args:
            data (Any): The value to append.
        """
        new_node = DoublyNode(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            if self.tail:
                self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def prepend(self, data: Any) -> None:
        """Inserts a node at the beginning of the list.

        This operation runs in O(1) time.

        Args:
            data (Any): The value to prepend.
        """
        new_node = DoublyNode(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self._size += 1

    def remove(self, data: Any) -> bool:
        """Removes the first occurrence of a specific value.

        This operation runs in O(N) time due to linear search.

        Args:
            data (Any): The value to remove.

        Returns:
            bool: True if a node was removed, otherwise False.
        """
        current = self.head

        while current:
            if current.data == data:
                # Update previous link
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                # Update next link
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self._size -= 1
                return True

            current = current.next

        return False

    def display_forward(self) -> str:
        """Returns a string representation from head to tail.

        Returns:
            str: A formatted representation of the list.
        """
        elements = [str(data) for data in self]
        return " <-> ".join(elements) if elements else "EMPTY"
