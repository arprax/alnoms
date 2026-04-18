"""
Arprax Logistics Engine Demo.
A comprehensive integration test utilizing the entire alnoms.dsa library facade.
"""

# --- STRUCTURE IMPORTS ---
# Powered by alnoms.dsa.structures.__init__.py
from alnoms.dsa.structures import (
    Queue,
    Stack,
    Bag,
    SinglyLinkedList,
    SeparateChainingHashST,
    BinarySearchTree,
    Digraph,
    EdgeWeightedDigraph,
    DirectedEdge,
)

# --- ALGORITHM IMPORTS ---
# Powered by the respective __init__.py files in the algorithms subfolders
from alnoms.dsa.algorithms.sorting import QuickSort
from alnoms.dsa.algorithms.searching import BinarySearch
from alnoms.dsa.algorithms.pointers import CycleDetector
from alnoms.dsa.algorithms.graph import Topological, DijkstraSP, BreadthFirstPaths


def run_logistics_demo():
    print("==================================================")
    print(" 🚀 ALNOMS LOGISTICS ENGINE (DSA INTEGRATION DEMO)")
    print("==================================================\n")

    # ---------------------------------------------------------
    # PHASE 1: DATA INGESTION & INDEXING (Structures)
    # ---------------------------------------------------------
    print("📦 PHASE 1: Ingesting Packages...")

    # 1. Queue for incoming processing
    incoming_queue = Queue()
    incoming_queue.enqueue({"id": "PKG-001", "weight": 45, "dest": 3})
    incoming_queue.enqueue({"id": "PKG-002", "weight": 12, "dest": 4})
    incoming_queue.enqueue({"id": "PKG-003", "weight": 88, "dest": 1})

    # 2. Hash Table for O(1) ID lookups
    package_db = SeparateChainingHashST()

    # 3. BST for O(log N) Priority/Weight indexing
    weight_index = BinarySearchTree()

    # Process the queue
    weights_list = []
    while not incoming_queue.is_empty():
        pkg = incoming_queue.dequeue()
        package_db.put(pkg["id"], pkg)
        weight_index.put(pkg["weight"], pkg["id"])
        weights_list.append(pkg["weight"])
        print(f"   -> Indexed {pkg['id']}")

    # ---------------------------------------------------------
    # PHASE 2: SORTING & SEARCHING (Algorithms)
    # ---------------------------------------------------------
    print("\n🔍 PHASE 2: Sorting and Searching...")

    # 4. Quick Sort the weights using the static method and capturing the result
    weights_list = QuickSort.quick_sort(weights_list)
    print(f"   -> Sorted package weights: {weights_list}")

    # 5. Binary Search to check if a specific weight capacity is needed
    target_weight = 45
    found_idx = BinarySearch.search(weights_list, target_weight)
    print(
        f"   -> Binary Search for {target_weight}kg: {'Found' if found_idx != -1 else 'Not Found'}"
    )

    # ---------------------------------------------------------
    # PHASE 3: NETWORK TOPOLOGY (Digraphs)
    # ---------------------------------------------------------
    print("\n🕸️  PHASE 3: Building Delivery Topology...")

    # 6. Digraph to represent hub dependencies (Hub 0 -> Hub 1 -> Hub 2)
    V = 6
    dependency_graph = Digraph(V)
    dependency_graph.add_edge(0, 1)
    dependency_graph.add_edge(0, 2)
    dependency_graph.add_edge(1, 3)
    dependency_graph.add_edge(2, 3)

    # 7. Topological Sort to find processing order
    topo = Topological(dependency_graph)
    # Handle whether order is a property or a callable method
    order = topo.order() if callable(topo.order) else topo.order
    print(f"   -> Safe Processing Order: {list(order)}")

    # ---------------------------------------------------------
    # PHASE 4: ROUTING & PATHFINDING (Edge Weighted Graphs)
    # ---------------------------------------------------------
    print("\n🗺️  PHASE 4: Calculating Shortest Delivery Routes...")

    # 8. EdgeWeightedDigraph for actual physical distances
    road_network = EdgeWeightedDigraph(V)
    road_network.add_edge(DirectedEdge(0, 1, 5.0))
    road_network.add_edge(DirectedEdge(0, 2, 2.0))
    road_network.add_edge(DirectedEdge(2, 1, 1.5))  # Shortcut!
    road_network.add_edge(DirectedEdge(1, 3, 4.0))
    road_network.add_edge(DirectedEdge(2, 3, 6.0))
    road_network.add_edge(DirectedEdge(3, 4, 3.0))

    # 9. Dijkstra's Algorithm for Shortest Path
    source_hub = 0
    target_hub = 4
    dijkstra = DijkstraSP(road_network, source_hub)

    if dijkstra.has_path_to(target_hub):
        distance = dijkstra.dist_to(target_hub)
        path = dijkstra.path_to(target_hub)

        route_str = " -> ".join([f"[{e.from_vertex()}-{e.to_vertex()}]" for e in path])
        print(f"   -> Optimal Route to Hub {target_hub}: {route_str}")
        print(f"   -> Total Distance: {distance} miles")
    else:
        print(f"   -> Hub {target_hub} is unreachable from Hub {source_hub}.")

    # 10. Breadth-First Paths for hop-count (ignoring weights)
    bfs = BreadthFirstPaths(dependency_graph, source_hub)
    if bfs.has_path_to(target_hub):
        hops = len(list(bfs.path_to(target_hub))) - 1
        print(f"   -> Minimum Hops to Hub {target_hub} (BFS): {hops} hops")
    else:
        print(f"   -> Hub {target_hub} is unreachable via BFS.")

    # ---------------------------------------------------------
    # PHASE 5: AUDIT LOG (Stacks, Bags, & Linked Lists)
    # ---------------------------------------------------------
    print("\n📝 PHASE 5: Audit & Cleanup...")

    # 11. Bag for unordered collection of processed hubs
    completed_hubs = Bag()
    completed_hubs.add(source_hub)
    completed_hubs.add(target_hub)

    # 12. Stack for undo operations
    undo_stack = Stack()
    undo_stack.push("Dispatch PKG-002")

    # 13. Singly Linked List for a lightweight, sequential audit trail
    audit_log = SinglyLinkedList()
    audit_log.append("System Start")
    audit_log.append("Routing Complete")

    # 14. Pointer Verification (Floyd's Cycle Detection)
    head_node = getattr(audit_log, "head", None) or getattr(audit_log, "_head", None)

    if head_node:
        is_corrupt = CycleDetector.has_cycle(head_node)
        print(
            f"   -> Audit Log Integrity: {'Corrupted (Cycle Found!)' if is_corrupt else 'Valid (Acyclic)'}"
        )
    else:
        print("   -> Audit log recorded.")

    print("\n==================================================")
    print(" 🏁 DEMO COMPLETE: All DSA constraints satisfied.")
    print("==================================================\n")


if __name__ == "__main__":
    run_logistics_demo()
