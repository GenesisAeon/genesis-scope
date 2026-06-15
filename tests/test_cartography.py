"""Tests for genesis_scope.cartography."""

from __future__ import annotations

import pytest

from genesis_scope.cartography import (
    DEFAULT_MAP,
    NodeKind,
    PheromoneTrace,
    RelationKind,
    SemanticEdge,
    SemanticMap,
    SemanticNode,
    compare_maps,
    compare_perspectives,
)


def _two_node_map(weight: float = 0.5) -> SemanticMap:
    semantic_map = SemanticMap(name="m")
    semantic_map.add_node(SemanticNode(id="a", label="A"))
    semantic_map.add_node(SemanticNode(id="b", label="B"))
    semantic_map.add_edge(SemanticEdge("a", "b", RelationKind.INFLUENCES, weight))
    return semantic_map


def test_edge_weight_must_be_in_unit_interval():
    with pytest.raises(ValueError):
        SemanticEdge("a", "b", RelationKind.INFLUENCES, 1.5)


def test_add_edge_requires_known_nodes():
    semantic_map = SemanticMap()
    semantic_map.add_node(SemanticNode(id="a", label="A"))
    with pytest.raises(ValueError):
        semantic_map.add_edge(SemanticEdge("a", "b", RelationKind.INFLUENCES))


def test_outgoing_and_incoming():
    semantic_map = _two_node_map()
    assert [e.target for e in semantic_map.outgoing("a")] == ["b"]
    assert [e.source for e in semantic_map.incoming("b")] == ["a"]
    assert semantic_map.outgoing("b") == []


def test_trace_same_node():
    semantic_map = _two_node_map()
    assert semantic_map.trace("a", "a") == ["a"]


def test_trace_direct_path():
    semantic_map = _two_node_map()
    assert semantic_map.trace("a", "b") == ["a", "b"]


def test_trace_no_path():
    semantic_map = _two_node_map()
    assert semantic_map.trace("b", "a") is None


def test_trace_unknown_node_raises():
    semantic_map = _two_node_map()
    with pytest.raises(ValueError):
        semantic_map.trace("a", "missing")


def test_attractors_ranks_by_weighted_in_degree():
    semantic_map = SemanticMap()
    for node_id in ("a", "b", "c"):
        semantic_map.add_node(SemanticNode(id=node_id, label=node_id.upper()))
    semantic_map.add_edge(SemanticEdge("a", "c", RelationKind.INFLUENCES, 0.9))
    semantic_map.add_edge(SemanticEdge("b", "c", RelationKind.INFLUENCES, 0.5))
    semantic_map.add_edge(SemanticEdge("a", "b", RelationKind.INFLUENCES, 0.2))

    ranked = semantic_map.attractors(top_n=2)
    assert ranked[0] == ("c", pytest.approx(1.4))
    assert ranked[1][0] == "b"


def test_attractors_top_n_must_be_positive():
    semantic_map = _two_node_map()
    with pytest.raises(ValueError):
        semantic_map.attractors(top_n=0)


def test_to_dict_from_dict_round_trip():
    semantic_map = _two_node_map(weight=0.7)
    restored = SemanticMap.from_dict(semantic_map.to_dict())

    assert restored.name == semantic_map.name
    assert set(restored.nodes) == set(semantic_map.nodes)
    assert restored.nodes["a"].kind == NodeKind.CONCEPT
    assert [e.key() for e in restored.edges] == [e.key() for e in semantic_map.edges]
    assert restored.edges[0].weight == pytest.approx(0.7)


def test_compare_maps_detects_added_and_removed():
    previous = _two_node_map()
    current = SemanticMap(name="m")
    current.add_node(SemanticNode(id="a", label="A"))
    current.add_node(SemanticNode(id="c", label="C"))
    current.add_edge(SemanticEdge("a", "c", RelationKind.GENERATES, 0.5))

    report = compare_maps(previous, current)

    assert report.added_nodes == ["c"]
    assert report.removed_nodes == ["b"]
    assert report.added_edges == [("a", "c", "generates")]
    assert report.removed_edges == [("a", "b", "influences")]
    assert report.reweighted_edges == []
    assert report.has_drift()


def test_compare_maps_detects_reweighted_edge():
    previous = _two_node_map(weight=0.5)
    current = _two_node_map(weight=0.9)

    report = compare_maps(previous, current)

    assert report.added_nodes == []
    assert report.removed_nodes == []
    assert report.added_edges == []
    assert report.removed_edges == []
    assert report.reweighted_edges == [("a", "b", "influences", 0.5, 0.9)]


def test_compare_maps_no_drift():
    semantic_map = _two_node_map()
    report = compare_maps(semantic_map, semantic_map)
    assert not report.has_drift()


def test_compare_perspectives_requires_two_maps():
    with pytest.raises(ValueError):
        compare_perspectives({"only": _two_node_map()})


def test_compare_perspectives_shared_and_unique():
    shared = _two_node_map()

    other = SemanticMap(name="other")
    other.add_node(SemanticNode(id="a", label="A"))
    other.add_node(SemanticNode(id="b", label="B"))
    other.add_node(SemanticNode(id="c", label="C"))
    other.add_edge(SemanticEdge("a", "b", RelationKind.INFLUENCES, 0.5))
    other.add_edge(SemanticEdge("b", "c", RelationKind.CONTRADICTS, 0.3))

    comparison = compare_perspectives({"agent1": shared, "agent2": other})

    assert comparison.shared_nodes == ["a", "b"]
    assert comparison.unique_nodes == {"agent1": [], "agent2": ["c"]}
    assert comparison.shared_edges == [("a", "b", "influences")]
    assert comparison.unique_edges == {"agent1": [], "agent2": [("b", "c", "contradicts")]}


def test_default_map_traces_crep_to_agent_coordination():
    path = DEFAULT_MAP.trace("crep", "agent_coordination")
    assert path == ["crep", "governance", "diamond", "claim_system", "agent_coordination"]


def test_default_map_traces_quasicrystals_to_scope():
    path = DEFAULT_MAP.trace("quasicrystals", "scope")
    assert path == ["quasicrystals", "info_geometry", "topology", "semantic_states", "scope"]


def test_default_map_attractors_include_scope_and_genesis_os():
    top_ids = [node_id for node_id, _ in DEFAULT_MAP.attractors(top_n=5)]
    assert "genesis_os" in top_ids
    assert "scope" in top_ids
    assert "unified_mandala" in top_ids


def test_walk_reinforces_edge_weight():
    semantic_map = _two_node_map(weight=0.5)
    trace = semantic_map.walk("agent1", ["a", "b"], gain=0.1)

    assert semantic_map.edges[0].weight == pytest.approx(0.6)
    assert trace == PheromoneTrace(actor="agent1", path=("a", "b"))
    assert semantic_map.trail == [trace]


def test_walk_clamps_weight_at_one():
    semantic_map = _two_node_map(weight=0.95)
    semantic_map.walk("agent1", ["a", "b"], gain=0.5)
    assert semantic_map.edges[0].weight == pytest.approx(1.0)


def test_walk_requires_at_least_two_nodes():
    semantic_map = _two_node_map()
    with pytest.raises(ValueError):
        semantic_map.walk("agent1", ["a"])


def test_walk_requires_gain_in_unit_interval():
    semantic_map = _two_node_map()
    with pytest.raises(ValueError):
        semantic_map.walk("agent1", ["a", "b"], gain=0.0)
    with pytest.raises(ValueError):
        semantic_map.walk("agent1", ["a", "b"], gain=1.5)


def test_walk_requires_connected_path():
    semantic_map = _two_node_map()
    with pytest.raises(ValueError):
        semantic_map.walk("agent1", ["b", "a"])


def test_walk_reinforces_all_matching_edges():
    semantic_map = SemanticMap(name="m")
    semantic_map.add_node(SemanticNode(id="a", label="A"))
    semantic_map.add_node(SemanticNode(id="b", label="B"))
    semantic_map.add_edge(SemanticEdge("a", "b", RelationKind.INFLUENCES, 0.5))
    semantic_map.add_edge(SemanticEdge("a", "b", RelationKind.CONTRADICTS, 0.3))

    semantic_map.walk("agent1", ["a", "b"], gain=0.1)

    assert semantic_map.edges[0].weight == pytest.approx(0.6)
    assert semantic_map.edges[1].weight == pytest.approx(0.4)


def test_evaporate_decays_weight_toward_floor():
    semantic_map = _two_node_map(weight=0.5)
    semantic_map.evaporate(rate=0.8, floor=0.1)
    assert semantic_map.edges[0].weight == pytest.approx(0.4)


def test_evaporate_does_not_drop_below_floor():
    semantic_map = _two_node_map(weight=0.05)
    semantic_map.evaporate(rate=0.5, floor=0.1)
    assert semantic_map.edges[0].weight == pytest.approx(0.1)


def test_evaporate_requires_valid_rate_and_floor():
    semantic_map = _two_node_map()
    with pytest.raises(ValueError):
        semantic_map.evaporate(rate=0.0)
    with pytest.raises(ValueError):
        semantic_map.evaporate(rate=1.5)
    with pytest.raises(ValueError):
        semantic_map.evaporate(floor=-0.1)
    with pytest.raises(ValueError):
        semantic_map.evaporate(floor=1.5)


def test_reinforced_path_resists_evaporation_while_others_fade():
    semantic_map = SemanticMap(name="m")
    for node_id in ("a", "b", "c"):
        semantic_map.add_node(SemanticNode(id=node_id, label=node_id.upper()))
    semantic_map.add_edge(SemanticEdge("a", "b", RelationKind.INFLUENCES, 0.5))
    semantic_map.add_edge(SemanticEdge("a", "c", RelationKind.INFLUENCES, 0.5))

    for _ in range(5):
        semantic_map.walk("agent1", ["a", "b"], gain=0.05)
        semantic_map.evaporate(rate=0.95, floor=0.01)

    walked = next(e for e in semantic_map.edges if e.target == "b")
    unused = next(e for e in semantic_map.edges if e.target == "c")
    assert walked.weight > unused.weight


def test_footprints_counts_traversals_per_actor():
    semantic_map = _two_node_map()
    semantic_map.walk("agent1", ["a", "b"], gain=0.01)
    semantic_map.walk("agent1", ["a", "b"], gain=0.01)
    semantic_map.walk("human", ["a", "b"], gain=0.01)

    assert semantic_map.footprints() == {"agent1": 2, "human": 1}


def test_to_dict_from_dict_round_trips_trail():
    semantic_map = _two_node_map()
    semantic_map.walk("agent1", ["a", "b"], gain=0.1)

    restored = SemanticMap.from_dict(semantic_map.to_dict())

    assert restored.trail == semantic_map.trail
    assert restored.edges[0].weight == pytest.approx(semantic_map.edges[0].weight)
