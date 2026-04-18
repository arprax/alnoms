"""
Alnoms Data Structures.

Provides a curated collection of high‑performance, pedagogically clean
data structures used throughout the Alnoms ecosystem. The package
includes linear containers, graph representations, and ordered symbol
tables. All implementations emphasize predictable worst‑case behavior,
clarity, and suitability for algorithmic experimentation.

Available Categories:
- Linear Structures: Stack, Queue, Bag, SinglyLinkedList, DoublyLinkedList
- Graphs: Undirected, Directed, Weighted, and Edge abstractions
- Symbol Tables: Binary Search Tree, Hash Table (Separate Chaining)

This module exposes the primary public API for convenient imports.
"""

# Linear Structures
from .stack import Stack
from .queue import Queue
from .bag import Bag
from .singly_linked_list import SinglyLinkedList
from .doubly_linked_list import DoublyLinkedList

# Graphs
from .graphs import Graph
from .digraph import Digraph
from .edge_weighted_graph import EdgeWeightedGraph
from .edge_weighted_digraph import EdgeWeightedDigraph
from .directed_edge import DirectedEdge
from .edge import Edge

# Search Trees & Symbol Tables
from .binary_search_tree import BinarySearchTree
from .separate_chaining_hash_st import SeparateChainingHashST

__all__ = [
    "Stack",
    "Queue",
    "Bag",
    "SinglyLinkedList",
    "DoublyLinkedList",
    "Graph",
    "Digraph",
    "EdgeWeightedGraph",
    "EdgeWeightedDigraph",
    "DirectedEdge",
    "Edge",
    "BinarySearchTree",
    "SeparateChainingHashST",
]
