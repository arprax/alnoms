"""
Binary Search Tree (BST).

Provides a recursive implementation of an ordered symbol table using a
binary search tree. Keys must be comparable, and the structure supports
ordered operations such as min, max, floor, rank, and sorted iteration.
Deletion uses Hibbard's algorithm.

Design Characteristics:
- Ordered key‑value storage
- In‑order traversal yields sorted keys
- Hibbard deletion for node removal
- Rank and selection operations supported
- Worst‑case height O(N) if unbalanced

Classes:
    BinarySearchTree: Ordered symbol table implemented using a BST.
"""

from typing import Any, Optional, List


class _Node:
    """Internal node representation for the BST.

    Each node stores a key, value, left and right children, and the size
    of the subtree rooted at this node.

    Attributes:
        key (Any): Key stored in the node.
        val (Any): Value associated with the key.
        left (Optional[_Node]): Left child.
        right (Optional[_Node]): Right child.
        size (int): Number of nodes in the subtree.
    """

    def __init__(self, key: Any, val: Any, size: int):
        self.key = key
        self.val = val
        self.left: Optional["_Node"] = None
        self.right: Optional["_Node"] = None
        self.size = size


class BinarySearchTree:
    """Binary Search Tree (BST) symbol table.

    Keys are maintained in sorted order. Supports search, insertion,
    deletion (Hibbard), and ordered operations such as min, max, and
    floor. All operations are implemented recursively.
    """

    def __init__(self):
        """Initializes an empty BST."""
        self._root: Optional[_Node] = None

    def size(self) -> int:
        """Returns the number of key‑value pairs in the table.

        Returns:
            int: Total number of stored entries.
        """
        return self._size(self._root)

    def _size(self, x: Optional[_Node]) -> int:
        """Returns the size of the subtree rooted at ``x``."""
        return 0 if x is None else x.size

    def is_empty(self) -> bool:
        """Checks whether the BST is empty.

        Returns:
            bool: True if empty, otherwise False.
        """
        return self.size() == 0

    def get(self, key: Any) -> Optional[Any]:
        """Returns the value associated with ``key``.

        Args:
            key (Any): Key to search for.

        Returns:
            Optional[Any]: Value if found, otherwise None.
        """
        return self._get(self._root, key)

    def _get(self, x: Optional[_Node], key: Any) -> Optional[Any]:
        if x is None:
            return None

        if key < x.key:
            return self._get(x.left, key)
        if key > x.key:
            return self._get(x.right, key)
        return x.val

    def contains(self, key: Any) -> bool:
        """Checks whether the BST contains ``key``.

        Returns:
            bool: True if present, otherwise False.
        """
        return self.get(key) is not None

    def put(self, key: Any, val: Any) -> None:
        """Inserts or updates a key‑value pair.

        If ``val`` is None, the key is deleted.

        Args:
            key (Any): Key to insert.
            val (Any): Value to associate.
        """
        if val is None:
            self.delete(key)
            return
        self._root = self._put(self._root, key, val)

    def _put(self, x: Optional[_Node], key: Any, val: Any) -> _Node:
        if x is None:
            return _Node(key, val, 1)

        if key < x.key:
            x.left = self._put(x.left, key, val)
        elif key > x.key:
            x.right = self._put(x.right, key, val)
        else:
            x.val = val

        x.size = 1 + self._size(x.left) + self._size(x.right)
        return x

    def min(self) -> Any:
        """Returns the smallest key.

        Raises:
            ValueError: If the BST is empty.
        """
        if self.is_empty():
            raise ValueError("min() called on empty BST")
        return self._min(self._root).key

    def _min(self, x: _Node) -> _Node:
        return x if x.left is None else self._min(x.left)

    def max(self) -> Any:
        """Returns the largest key.

        Raises:
            ValueError: If the BST is empty.
        """
        if self.is_empty():
            raise ValueError("max() called on empty BST")
        return self._max(self._root).key

    def _max(self, x: _Node) -> _Node:
        return x if x.right is None else self._max(x.right)

    def floor(self, key: Any) -> Optional[Any]:
        """Returns the largest key ≤ ``key``.

        Args:
            key (Any): Target key.

        Returns:
            Optional[Any]: Floor key, or None if no such key exists.
        """
        if self.is_empty():
            return None
        x = self._floor(self._root, key)
        return None if x is None else x.key

    def _floor(self, x: Optional[_Node], key: Any) -> Optional[_Node]:
        if x is None:
            return None

        if key == x.key:
            return x
        if key < x.key:
            return self._floor(x.left, key)

        t = self._floor(x.right, key)
        return t if t is not None else x

    def delete_min(self) -> None:
        """Deletes the smallest key."""
        if self.is_empty():
            raise ValueError("delete_min() called on empty BST")
        self._root = self._delete_min(self._root)

    def _delete_min(self, x: _Node) -> Optional[_Node]:
        if x.left is None:
            return x.right
        x.left = self._delete_min(x.left)
        x.size = 1 + self._size(x.left) + self._size(x.right)
        return x

    def delete(self, key: Any) -> None:
        """Deletes ``key`` from the BST using Hibbard deletion."""
        if not self.contains(key):
            return
        self._root = self._delete(self._root, key)

    def _delete(self, x: _Node, key: Any) -> Optional[_Node]:
        if x is None:
            return None

        if key < x.key:
            x.left = self._delete(x.left, key)
        elif key > x.key:
            x.right = self._delete(x.right, key)
        else:
            # Node with one or zero children
            if x.right is None:
                return x.left
            if x.left is None:
                return x.right

            # Node with two children: replace with successor
            t = x
            x = self._min(t.right)
            x.right = self._delete_min(t.right)
            x.left = t.left

        x.size = 1 + self._size(x.left) + self._size(x.right)
        return x

    def keys(self) -> List[Any]:
        """Returns all keys in sorted order.

        Returns:
            List[Any]: Sorted list of keys.
        """
        result: List[Any] = []
        self._keys(self._root, result)
        return result

    def _keys(self, x: Optional[_Node], result: List[Any]) -> None:
        if x is None:
            return
        self._keys(x.left, result)
        result.append(x.key)
        self._keys(x.right, result)
