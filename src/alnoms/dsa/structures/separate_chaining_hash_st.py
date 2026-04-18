"""
Hash Table Implementations.

Provides classic symbol table implementations based on hashing, including
separate chaining and (optionally) linear probing variants. Designed as
textbook-grade, inspectable data structures for algorithmic education
and performance governance experiments.

Features:
    - Hash-based key-value storage
    - Separate chaining collision handling
    - Hashable keys, arbitrary values
    - Deterministic, reference-friendly implementation

"""

from typing import Any, List, Optional, Tuple


class SeparateChainingHashST:
    """Hash table implementation using separate chaining.

    This symbol table stores key–value pairs in an array of buckets,
    where each bucket is a Python list of ``(key, value)`` tuples.
    Collisions are resolved by chaining, and average search time is
    proportional to ``O(N / M)`` where:

        • ``N`` = number of key–value pairs
        • ``M`` = number of buckets

    This implementation is simple, predictable, and suitable for workloads
    where hash distribution is reasonably uniform.
    """

    def __init__(self, m: int = 997):
        """Initializes the hash table.

        Args:
            m (int): Number of buckets (chains). Defaults to 997, a prime
                number that helps reduce clustering.

        Attributes:
            _m (int): Number of buckets.
            _n (int): Number of stored key–value pairs.
            _st (List[List[Tuple[Any, Any]]]): Array of buckets.
        """
        self._m = m
        self._n = 0
        self._st: List[List[Tuple[Any, Any]]] = [[] for _ in range(m)]

    def _hash(self, key: Any) -> int:
        """Computes the bucket index for a given key.

        Args:
            key (Any): A hashable key.

        Returns:
            int: The bucket index in the range ``[0, M)``.
        """
        return (hash(key) & 0x7FFFFFFF) % self._m

    def size(self) -> int:
        """Returns the number of key–value pairs stored.

        Returns:
            int: Total number of entries.
        """
        return self._n

    def is_empty(self) -> int:
        """Checks whether the table contains any entries.

        Returns:
            bool: True if the table is empty, otherwise False.
        """
        return self._n == 0

    def contains(self, key: Any) -> bool:
        """Checks whether the table contains the given key.

        Args:
            key (Any): The key to search for.

        Returns:
            bool: True if the key exists, otherwise False.
        """
        return self.get(key) is not None

    def get(self, key: Any) -> Optional[Any]:
        """Retrieves the value associated with a key.

        Args:
            key (Any): The key to search for.

        Returns:
            Optional[Any]: The associated value if found, otherwise None.
        """
        i = self._hash(key)
        for k, v in self._st[i]:
            if k == key:
                return v
        return None

    def put(self, key: Any, val: Any) -> None:
        """Inserts or updates a key–value pair.

        If the key already exists, its value is updated.
        If ``val`` is ``None``, the key is removed.

        Args:
            key (Any): The key to insert.
            val (Any): The value to associate with the key.
        """
        if val is None:
            self.delete(key)
            return

        i = self._hash(key)

        # Update existing key
        for idx, (k, v) in enumerate(self._st[i]):
            if k == key:
                self._st[i][idx] = (key, val)
                return

        # Insert new key–value pair
        self._st[i].append((key, val))
        self._n += 1

    def delete(self, key: Any) -> None:
        """Removes a key and its associated value.

        Args:
            key (Any): The key to remove.
        """
        i = self._hash(key)
        bucket = self._st[i]

        for idx, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[idx]
                self._n -= 1
                return

    def keys(self) -> List[Any]:
        """Returns all keys stored in the table.

        Returns:
            List[Any]: A list containing all keys.
        """
        all_keys = []
        for bucket in self._st:
            for k, _ in bucket:
                all_keys.append(k)
        return all_keys
