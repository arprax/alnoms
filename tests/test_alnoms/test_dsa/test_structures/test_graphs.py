from alnoms.dsa.structures import Graph, Digraph


def test_graph_add_edge_and_adj():
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert g.E() == 2
    assert set(g.adj(1)) == {0, 2}


def test_digraph_add_edge_and_reverse():
    dg = Digraph(3)
    dg.add_edge(0, 1)
    dg.add_edge(1, 2)
    rev = dg.reverse()
    assert set(rev.adj(1)) == {0}
    assert set(rev.adj(2)) == {1}
