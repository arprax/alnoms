import os
import textwrap
import pytest


# ------------------------------------------------------------
# 1. Disable PRO / ENTERPRISE extensions for all OSS tests
# ------------------------------------------------------------
@pytest.fixture(autouse=True, scope="session")
def disable_paid_tiers():
    """
    Ensures OSS tests never accidentally load PRO/ENTERPRISE registries.
    """
    os.environ.pop("ALNOMS_PRO_KEY", None)
    os.environ.pop("ALNOMS_ENTERPRISE_KEY", None)


# ------------------------------------------------------------
# 2. Helper: write a Python script to a temp directory
# ------------------------------------------------------------
@pytest.fixture
def write_script(tmp_path):
    """
    Creates a Python script file in a temporary directory.

    Usage:
        path = write_script(\"\"\"
            def foo():
                return 42
        \"\"\")
    """

    def _writer(content: str, filename: str = "script.py"):
        path = tmp_path / filename
        path.write_text(textwrap.dedent(content), encoding="utf-8")
        return str(path)

    return _writer


# ------------------------------------------------------------
# 3. Helper: small sample arrays for sorting/searching tests
# ------------------------------------------------------------
@pytest.fixture
def sample_array():
    return [5, 1, 4, 2, 8]


@pytest.fixture
def sorted_array():
    return [1, 2, 4, 5, 8]


# ------------------------------------------------------------
# 4. Helper: simple graph builder for BFS/DFS/Dijkstra tests
# ------------------------------------------------------------
@pytest.fixture
def simple_graph():
    from alnoms.dsa.structures import Graph

    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    return g


@pytest.fixture
def simple_weighted_digraph():
    from alnoms.dsa.structures import EdgeWeightedDigraph, DirectedEdge

    g = EdgeWeightedDigraph(4)
    g.add_edge(DirectedEdge(0, 1, 1.0))
    g.add_edge(DirectedEdge(1, 2, 2.0))
    g.add_edge(DirectedEdge(0, 3, 10.0))
    return g


# ------------------------------------------------------------
# 5. Helper: linked list builder for cycle detection tests
# ------------------------------------------------------------
@pytest.fixture
def linked_list_nodes():
    """
    Returns a helper that builds linked lists with or without cycles.

    Usage:
        n1, n2, n3 = linked_list_nodes(3)
        n1.next = n2
        n2.next = n3
    """
    from alnoms.dsa.structures.node import Node

    def _builder(n):
        nodes = [Node(i) for i in range(n)]
        for i in range(n - 1):
            nodes[i].next = nodes[i + 1]
        return nodes

    return _builder
