from alnoms.dsa.structures import (
    Edge,
    EdgeWeightedGraph,
    EdgeWeightedDigraph,
    DirectedEdge,
)


def test_edge_weighted_graph_edges():
    g = EdgeWeightedGraph(3)
    e1 = Edge(0, 1, 1.0)
    e2 = Edge(1, 2, 2.0)
    g.add_edge(e1)
    g.add_edge(e2)
    edges = list(g.edges())
    assert len(edges) == 2
    assert {tuple(sorted((e.either(), e.other(e.either())))) for e in edges} == {
        (0, 1),
        (1, 2),
    }


def test_edge_weighted_digraph_edges():
    dg = EdgeWeightedDigraph(3)
    e = DirectedEdge(0, 1, 1.5)
    dg.add_edge(e)
    assert list(dg.edges())[0].to_vertex() == 1
