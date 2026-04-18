"""
Linked-List-Based Stack.

Implements a generic LIFO (Last-In First-Out) stack using a linked list
backing. This design guarantees O(1) worst-case push and pop operations
by avoiding array resizing and capacity management.

Features:
    - O(1) push and pop
    - Dynamic, node-based storage
    - Type-parameterized (generic) API
    - Safe iteration from top to bottom
"""

from typing import Optional, Iterator, TypeVar, Generic
from .node import Node

T = TypeVar("T")


class Stack(Generic[T]):
    """A LIFO (Last‑In First‑Out) stack implemented using a linked list.

    This implementation guarantees O(1) worst‑case time for both `push`
    and `pop` operations by avoiding the resizing overhead associated
    with array‑based stacks. The stack grows dynamically through linked
    nodes, making it suitable for workloads requiring predictable
    constant‑time operations.
    """

    def __init__(self):
        """Initializes an empty stack.

        Attributes:
            _first (Optional[Node]): Reference to the top node.
            _n (int): Number of items currently stored.
        """
        self._first: Optional[Node] = None
        self._n: int = 0

    def is_empty(self) -> bool:
        """Checks whether the stack is empty.

        Returns:
            bool: True if the stack contains no items, otherwise False.
        """
        return self._first is None

    def size(self) -> int:
        """Returns the number of items in the stack.

        Returns:
            int: The number of elements stored.
        """
        return self._n

    def push(self, item: T) -> None:
        """Pushes an item onto the top of the stack.

        This operation runs in O(1) time by inserting a new node at the
        head of the linked list.

        Args:
            item (T): The item to push onto the stack.
        """
        old_first = self._first
        self._first = Node(item)
        self._first.next = old_first
        self._n += 1

    def pop(self) -> T:
        """Removes and returns the most recently added item.

        This operation runs in O(1) time by removing the head node.

        Returns:
            T: The item previously at the top of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack underflow")

        item = self._first.data
        self._first = self._first.next
        self._n -= 1
        return item

    def peek(self) -> T:
        """Returns the item at the top of the stack without removing it.

        Returns:
            T: The item currently at the top.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack underflow")
        return self._first.data

    def __iter__(self) -> Iterator[T]:
        """Iterates over the stack from top to bottom.

        Yields:
            T: Items in LIFO order, starting from the top.
        """
        current = self._first
        while current:
            yield current.data
            current = current.next
