"""Testes da biblioteca ``graphs``, parametrizados para as duas representações."""

import xml.etree.ElementTree as ET

import pytest

from graphs import (
    AdjacencyListGraph,
    AdjacencyMatrixGraph,
    EdgeNotFoundError,
    InvalidVertexError,
    SelfLoopError,
)
from graphs.abstract_graph import AbstractGraph


@pytest.fixture(params=[AdjacencyMatrixGraph, AdjacencyListGraph], ids=["matrix", "list"])
def graph_factory(request):
    return request.param


# Construtor

class TestConstructor:
    def test_default_state_has_no_edges(self, graph_factory):
        g = graph_factory(5)
        assert g.getVertexCount() == 5
        assert g.getEdgeCount() == 0
        assert g.isEmptyGraph() is True

    def test_zero_vertices_allowed(self, graph_factory):
        g = graph_factory(0)
        assert g.getVertexCount() == 0
        assert g.getEdgeCount() == 0

    def test_default_vertex_weights_are_one(self, graph_factory):
        g = graph_factory(4)
        for v in range(4):
            assert g.getVertexWeight(v) == AbstractGraph.DEFAULT_WEIGHT
            assert g.getVertexWeight(v) == 1.0

    @pytest.mark.parametrize("bad", [-1, -5])
    def test_negative_vertex_count_raises_value_error(self, graph_factory, bad):
        with pytest.raises(ValueError):
            graph_factory(bad)

    @pytest.mark.parametrize("bad", [3.0, "3", None, [3], 3.5])
    def test_non_int_vertex_count_raises_value_error(self, graph_factory, bad):
        with pytest.raises(ValueError):
            graph_factory(bad)

    @pytest.mark.parametrize("bad", [True, False])
    def test_bool_vertex_count_raises_value_error(self, graph_factory, bad):
        with pytest.raises(ValueError):
            graph_factory(bad)


# addEdge / removeEdge / hasEdge / isSuccessor / isPredecessor

class TestEdgeMutation:
    def test_add_edge_creates_edge(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        assert g.hasEdge(0, 1) is True
        assert g.getEdgeCount() == 1

    def test_add_edge_is_directed(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        assert g.hasEdge(1, 0) is False

    def test_add_edge_idempotent_does_not_duplicate_count(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        g.addEdge(0, 1)
        g.addEdge(0, 1)
        assert g.getEdgeCount() == 1

    def test_add_edge_idempotent_preserves_weight(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        g.setEdgeWeight(0, 1, 42.0)
        g.addEdge(0, 1)
        assert g.getEdgeWeight(0, 1) == 42.0

    def test_new_edge_has_default_weight(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        assert g.getEdgeWeight(0, 1) == AbstractGraph.DEFAULT_WEIGHT
        assert g.getEdgeWeight(0, 1) == 1.0

    def test_add_edge_self_loop_raises(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(SelfLoopError):
            g.addEdge(1, 1)

    @pytest.mark.parametrize("u,v", [(-1, 0), (0, -1), (3, 0), (0, 3), (10, 10)])
    def test_add_edge_invalid_vertex_raises(self, graph_factory, u, v):
        g = graph_factory(3)
        with pytest.raises(InvalidVertexError):
            g.addEdge(u, v)

    def test_remove_edge_removes_existing(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        g.removeEdge(0, 1)
        assert g.hasEdge(0, 1) is False
        assert g.getEdgeCount() == 0

    def test_remove_edge_noop_if_absent(self, graph_factory):
        g = graph_factory(3)
        g.removeEdge(0, 1)
        assert g.getEdgeCount() == 0

    def test_remove_edge_then_readd_resets_to_default_weight(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        g.setEdgeWeight(0, 1, 99.0)
        g.removeEdge(0, 1)
        g.addEdge(0, 1)
        assert g.getEdgeWeight(0, 1) == AbstractGraph.DEFAULT_WEIGHT

    @pytest.mark.parametrize("u,v", [(-1, 0), (0, -1), (3, 0), (0, 3)])
    def test_remove_edge_invalid_vertex_raises(self, graph_factory, u, v):
        g = graph_factory(3)
        with pytest.raises(InvalidVertexError):
            g.removeEdge(u, v)

    def test_has_edge_invalid_vertex_raises(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(InvalidVertexError):
            g.hasEdge(0, 5)
        with pytest.raises(InvalidVertexError):
            g.hasEdge(5, 0)

    def test_is_successor_and_predecessor_reflect_edge(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        assert g.isSuccessor(0, 1) is True
        assert g.isPredecessor(0, 1) is True
        assert g.isSuccessor(1, 0) is False
        assert g.isPredecessor(1, 0) is False


# Predicados estruturais: isDivergent / isConvergent / isIncident

class TestStructuralPredicates:
    def test_is_divergent_true_when_same_source_diff_target(self, graph_factory):
        g = graph_factory(4)
        assert g.isDivergent(0, 1, 0, 2) is True

    def test_is_divergent_false_when_diff_source(self, graph_factory):
        g = graph_factory(4)
        assert g.isDivergent(0, 1, 1, 2) is False

    def test_is_divergent_false_when_identical_edge(self, graph_factory):
        g = graph_factory(4)
        assert g.isDivergent(0, 1, 0, 1) is False

    def test_is_convergent_true_when_same_target_diff_source(self, graph_factory):
        g = graph_factory(4)
        assert g.isConvergent(0, 2, 1, 2) is True

    def test_is_convergent_false_when_diff_target(self, graph_factory):
        g = graph_factory(4)
        assert g.isConvergent(0, 1, 0, 2) is False

    def test_is_convergent_false_when_identical_edge(self, graph_factory):
        g = graph_factory(4)
        assert g.isConvergent(0, 1, 0, 1) is False

    @pytest.mark.parametrize(
        "u,v,x,expected",
        [
            (0, 1, 0, True),
            (0, 1, 1, True),
            (0, 1, 2, False),
        ],
    )
    def test_is_incident(self, graph_factory, u, v, x, expected):
        g = graph_factory(4)
        assert g.isIncident(u, v, x) is expected

    def test_structural_predicates_do_not_require_edge_existence(self, graph_factory):
        g = graph_factory(4)
        assert g.getEdgeCount() == 0
        assert g.isDivergent(2, 3, 2, 0) is True
        assert g.isConvergent(3, 0, 1, 0) is True
        assert g.isIncident(2, 3, 3) is True

    @pytest.mark.parametrize(
        "method,args",
        [
            ("isDivergent", (5, 0, 0, 1)),
            ("isDivergent", (0, 5, 0, 1)),
            ("isDivergent", (0, 1, 5, 1)),
            ("isDivergent", (0, 1, 0, 5)),
            ("isConvergent", (5, 0, 0, 1)),
            ("isConvergent", (0, 5, 0, 1)),
            ("isIncident", (5, 0, 1)),
            ("isIncident", (0, 5, 1)),
            ("isIncident", (0, 1, 5)),
        ],
    )
    def test_structural_predicates_invalid_vertex_raises(self, graph_factory, method, args):
        g = graph_factory(4)
        with pytest.raises(InvalidVertexError):
            getattr(g, method)(*args)


# Graus de vértice

class TestDegrees:
    def test_in_and_out_degree_counts(self, graph_factory):
        g = graph_factory(4)
        g.addEdge(0, 1)
        g.addEdge(0, 2)
        g.addEdge(3, 1)
        assert g.getVertexOutDegree(0) == 2
        assert g.getVertexOutDegree(1) == 0
        assert g.getVertexInDegree(1) == 2
        assert g.getVertexInDegree(2) == 1
        assert g.getVertexInDegree(0) == 0

    def test_degree_updates_after_remove(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        g.removeEdge(0, 1)
        assert g.getVertexOutDegree(0) == 0
        assert g.getVertexInDegree(1) == 0

    def test_in_degree_invalid_vertex_raises(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(InvalidVertexError):
            g.getVertexInDegree(-1)
        with pytest.raises(InvalidVertexError):
            g.getVertexInDegree(3)

    def test_out_degree_invalid_vertex_raises(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(InvalidVertexError):
            g.getVertexOutDegree(-1)
        with pytest.raises(InvalidVertexError):
            g.getVertexOutDegree(3)


# Pesos de vértice

class TestVertexWeights:
    def test_round_trip(self, graph_factory):
        g = graph_factory(3)
        g.setVertexWeight(1, 3.14)
        assert g.getVertexWeight(1) == 3.14

    def test_set_invalid_vertex_raises(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(InvalidVertexError):
            g.setVertexWeight(-1, 1.0)
        with pytest.raises(InvalidVertexError):
            g.setVertexWeight(3, 1.0)

    def test_get_invalid_vertex_raises(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(InvalidVertexError):
            g.getVertexWeight(-1)
        with pytest.raises(InvalidVertexError):
            g.getVertexWeight(3)


# Pesos de aresta

class TestEdgeWeights:
    def test_round_trip(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        g.setEdgeWeight(0, 1, 7.5)
        assert g.getEdgeWeight(0, 1) == 7.5

    def test_get_nonexistent_edge_raises(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(EdgeNotFoundError):
            g.getEdgeWeight(0, 1)

    def test_set_nonexistent_edge_raises(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(EdgeNotFoundError):
            g.setEdgeWeight(0, 1, 5.0)

    def test_get_nonexistent_edge_after_removal_raises(self, graph_factory):
        g = graph_factory(3)
        g.addEdge(0, 1)
        g.removeEdge(0, 1)
        with pytest.raises(EdgeNotFoundError):
            g.getEdgeWeight(0, 1)

    def test_weight_invalid_vertex_raises_invalid_vertex_error(self, graph_factory):
        g = graph_factory(3)
        with pytest.raises(InvalidVertexError):
            g.getEdgeWeight(0, 5)
        with pytest.raises(InvalidVertexError):
            g.setEdgeWeight(0, 5, 1.0)


# isEmptyGraph / isCompleteGraph

class TestEmptyAndComplete:
    def test_empty_graph_true_initially(self, graph_factory):
        g = graph_factory(4)
        assert g.isEmptyGraph() is True

    def test_empty_graph_false_after_adding_edge(self, graph_factory):
        g = graph_factory(4)
        g.addEdge(0, 1)
        assert g.isEmptyGraph() is False

    def test_empty_graph_true_again_after_removing_only_edge(self, graph_factory):
        g = graph_factory(4)
        g.addEdge(0, 1)
        g.removeEdge(0, 1)
        assert g.isEmptyGraph() is True

    def test_complete_graph_true_when_all_edges_present(self, graph_factory):
        n = 4
        g = graph_factory(n)
        for u in range(n):
            for v in range(n):
                if u != v:
                    g.addEdge(u, v)
        assert g.getEdgeCount() == n * (n - 1)
        assert g.isCompleteGraph() is True

    def test_complete_graph_false_when_missing_one_edge(self, graph_factory):
        n = 4
        g = graph_factory(n)
        for u in range(n):
            for v in range(n):
                if u != v:
                    g.addEdge(u, v)
        g.removeEdge(0, 1)
        assert g.isCompleteGraph() is False

    def test_complete_graph_empty_graph_with_zero_or_one_vertex(self, graph_factory):
        g0 = graph_factory(0)
        assert g0.isCompleteGraph() is True  # 0 == 0*(0-1)
        g1 = graph_factory(1)
        assert g1.isCompleteGraph() is True  # 0 == 1*0


# isConnected

class TestConnectivity:
    def test_zero_vertex_graph_is_connected(self, graph_factory):
        g = graph_factory(0)
        assert g.isConnected() is True
        assert g.isConnected(strong=True) is True

    def test_single_vertex_graph_is_connected(self, graph_factory):
        g = graph_factory(1)
        assert g.isConnected() is True
        assert g.isConnected(strong=True) is True

    def test_strongly_connected_cycle(self, graph_factory):
        n = 4
        g = graph_factory(n)
        for i in range(n):
            g.addEdge(i, (i + 1) % n)
        assert g.isConnected(strong=False) is True
        assert g.isConnected(strong=True) is True

    def test_weakly_but_not_strongly_connected(self, graph_factory):
        # Caminho 0->1->2->3: fracamente conectado, mas não fortemente.
        n = 4
        g = graph_factory(n)
        g.addEdge(0, 1)
        g.addEdge(1, 2)
        g.addEdge(2, 3)
        assert g.isConnected(strong=False) is True
        assert g.isConnected(strong=True) is False

    def test_disconnected_graph(self, graph_factory):
        n = 4
        g = graph_factory(n)
        g.addEdge(0, 1)
        g.addEdge(2, 3)
        assert g.isConnected(strong=False) is False
        assert g.isConnected(strong=True) is False

    def test_empty_graph_with_multiple_vertices_is_not_connected(self, graph_factory):
        g = graph_factory(3)
        assert g.isConnected(strong=False) is False
        assert g.isConnected(strong=True) is False


# exportToGEPHI

def _local_tag(elem):
    """Tag sem o prefixo de namespace XML."""
    tag = elem.tag
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


class TestExportToGephi:
    def test_invalid_extension_raises_value_error(self, graph_factory, tmp_path):
        g = graph_factory(3)
        bad_path = tmp_path / "g.txt"
        with pytest.raises(ValueError):
            g.exportToGEPHI(str(bad_path))

    def test_invalid_extension_case_sensitivity_still_raises_for_wrong_ext(
        self, graph_factory, tmp_path
    ):
        g = graph_factory(3)
        bad_path = tmp_path / "g.gexfx"
        with pytest.raises(ValueError):
            g.exportToGEPHI(str(bad_path))

    def test_uppercase_extension_is_accepted(self, graph_factory, tmp_path):
        g = graph_factory(2)
        g.addEdge(0, 1)
        path = tmp_path / "g.GEXF"
        g.exportToGEPHI(str(path))
        assert path.exists()

    def test_export_writes_well_formed_gexf_with_correct_counts(self, graph_factory, tmp_path):
        n = 4
        g = graph_factory(n)
        g.addEdge(0, 1)
        g.addEdge(1, 2)
        g.addEdge(2, 0)
        g.setVertexWeight(0, 2.5)
        g.setEdgeWeight(0, 1, 9.0)

        path = tmp_path / "g.gexf"
        g.exportToGEPHI(str(path))

        assert path.exists()

        tree = ET.parse(str(path))
        root = tree.getroot()

        nodes_elem = None
        edges_elem = None
        for elem in root.iter():
            if _local_tag(elem) == "nodes":
                nodes_elem = elem
            elif _local_tag(elem) == "edges":
                edges_elem = elem

        assert nodes_elem is not None
        assert edges_elem is not None

        node_elems = [e for e in nodes_elem if _local_tag(e) == "node"]
        edge_elems = [e for e in edges_elem if _local_tag(e) == "edge"]

        assert len(node_elems) == g.getVertexCount()
        assert len(edge_elems) == g.getEdgeCount()

    def test_export_empty_graph(self, graph_factory, tmp_path):
        g = graph_factory(0)
        path = tmp_path / "empty.gexf"
        g.exportToGEPHI(str(path))

        tree = ET.parse(str(path))
        root = tree.getroot()

        nodes_elem = next(e for e in root.iter() if _local_tag(e) == "nodes")
        edges_elem = next(e for e in root.iter() if _local_tag(e) == "edges")

        assert len([e for e in nodes_elem if _local_tag(e) == "node"]) == 0
        assert len([e for e in edges_elem if _local_tag(e) == "edge"]) == 0


# Teste de paridade explícito entre as duas representações

def _build_sample_graph(cls):
    """Mesmo grafo de exemplo para comparar as duas representações."""
    n = 5
    g = cls(n)
    edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 0), (1, 4)]
    for u, v in edges:
        g.addEdge(u, v)
    g.setVertexWeight(0, 10.0)
    g.setVertexWeight(3, -2.5)
    g.setEdgeWeight(0, 1, 3.3)
    g.setEdgeWeight(2, 3, 7.0)
    return g, n


class TestMatrixListParity:
    def test_full_api_parity_between_representations(self):
        matrix_graph, n = _build_sample_graph(AdjacencyMatrixGraph)
        list_graph, _ = _build_sample_graph(AdjacencyListGraph)

        assert matrix_graph.getEdgeCount() == list_graph.getEdgeCount()

        for u in range(n):
            for v in range(n):
                if u == v:
                    continue
                assert matrix_graph.hasEdge(u, v) == list_graph.hasEdge(u, v), (
                    f"hasEdge mismatch at ({u}, {v})"
                )

        for v in range(n):
            assert matrix_graph.getVertexInDegree(v) == list_graph.getVertexInDegree(v)
            assert matrix_graph.getVertexOutDegree(v) == list_graph.getVertexOutDegree(v)
            assert matrix_graph.getVertexWeight(v) == list_graph.getVertexWeight(v)

        for u in range(n):
            for v in range(n):
                if u != v and matrix_graph.hasEdge(u, v):
                    assert matrix_graph.getEdgeWeight(u, v) == list_graph.getEdgeWeight(u, v)

        assert matrix_graph.isEmptyGraph() == list_graph.isEmptyGraph()
        assert matrix_graph.isCompleteGraph() == list_graph.isCompleteGraph()
        assert matrix_graph.isConnected() == list_graph.isConnected()
        assert matrix_graph.isConnected(strong=True) == list_graph.isConnected(strong=True)
