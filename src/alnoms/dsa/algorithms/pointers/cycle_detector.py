"""
Pointer‑Based Algorithms.

Provides classic two‑pointer techniques, including Floyd’s Tortoise‑and‑Hare
cycle detection algorithm for singly linked lists. These algorithms rely
on constant‑space pointer manipulation and are widely used in linked‑list
processing and fast/slow traversal patterns.

Design Characteristics:
- O(1) auxiliary space
- O(N) cycle detection
- Works on any singly linked list with `next` references

Classes:
    CycleDetector: Implements Floyd’s cycle‑finding algorithm.
"""

from typing import Optional
from alnoms.dsa.structures.node import Node


class CycleDetector:
    """Cycle detection using Floyd’s Tortoise‑and‑Hare algorithm.

    Uses two pointers moving at different speeds to determine whether a
    singly linked list contains a cycle. If the fast pointer ever meets
    the slow pointer, a cycle exists.
    """

    @staticmethod
    def has_cycle(head: Optional[Node]) -> bool:
        """Detects whether a singly linked list contains a cycle.

        The algorithm advances a slow pointer by one step and a fast
        pointer by two steps. If the list contains a cycle, the two
        pointers eventually meet. If the fast pointer reaches the end of
        the list, no cycle exists.

        Args:
            head (Optional[Node]): Head of the singly linked list.

        Returns:
            bool: True if a cycle exists, otherwise False.

        Complexity:
            Time: O(N)
            Space: O(1)
        """
        if not head or not head.next:
            return False

        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow is fast:
                return True

        return False
