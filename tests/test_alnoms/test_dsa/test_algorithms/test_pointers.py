from alnoms.dsa.algorithms.pointers.cycle_detector import CycleDetector
from alnoms.dsa.structures.node import Node


def test_cycle_detector_detects_cycle_and_no_cycle():
    # 1 -> 2 -> 3 -> 2 (cycle)
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n1.next = n2
    n2.next = n3
    n3.next = n2
    assert CycleDetector.has_cycle(n1)

    # 1 -> 2 -> 3 -> None
    n3.next = None
    assert not CycleDetector.has_cycle(n1)
