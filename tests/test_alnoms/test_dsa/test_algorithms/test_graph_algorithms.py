from alnoms.dsa.structures import Graph, Digraph, EdgeWeightedDigraph, DirectedEdge
from alnoms.dsa.algorithms.graph.breadth_first_paths import BreadthFirstPaths
from alnoms.dsa.algorithms.graph.dijkstra_sp import DijkstraSP
from alnoms.dsa.algorithms.graph.topological import Topological


def test_bfs_paths_basic():
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    bfs = BreadthFirstPaths(g, 0)
    assert bfs.has_path_to(2)
    path = list(bfs.path_to(2))
    assert path == [0, 1, 2]


def test_dijkstra_sp_basic():
    g = EdgeWeightedDigraph(3)
    g.add_edge(DirectedEdge(0, 1, 1.0))
    g.add_edge(DirectedEdge(1, 2, 2.0))
    sp = DijkstraSP(g, 0)
    assert sp.has_path_to(2)
    assert sp.dist_to(2) == 3.0


def test_topological_order_exists_for_simple_dag():
    dg = Digraph(3)
    dg.add_edge(0, 1)
    dg.add_edge(1, 2)
    topo = Topological(dg)
    assert topo.has_order()
    order = list(topo.order())
    # 0 must come before 1, 1 before 2
    assert order.index(0) < order.index(1) < order.index(2)
