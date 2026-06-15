"""Semantic cartography — the navigable map of the GenesisAeon concept space.

genesis-scope's role is the translation layer between the ecosystem's
domains (physics, biology, governance, runtime, agents, entropy,
mathematics) and a navigable semantic topography: explicit nodes,
typed relations between them, traceable paths, attractor concepts, and
drift between snapshots of the map.

This module does not try to explain the latent space exhaustively. It
makes traces through it visible:

    CREP -> Governance -> Diamond -> Claim-System -> Agentenkoordination
    Quasikristalle -> Informationsgeometrie -> Topologie -> Semantische
        Zustaende -> Scope

and lets those traces be compared, ranked and diffed over time. A
pheromone trail (`walk`, `evaporate`) lets the map respond to its own
usage: paths that are actually walked by humans or agents get
stronger, paths that fall out of use fade — turning the static
topography into a living one.

Usage and quality are tracked as two separate dimensions. An edge's
`weight` is its pheromone trail — how often the route is walked,
regardless of outcome. Its `quality` is a reliability score that only
moves when a walk is explicitly marked as successful or not. This
keeps the busiest path from automatically becoming "the best path":
a route can be frequent and unreliable, or rare and excellent, and
`attractors(by=...)` can rank by either dimension.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

DEFAULT_PHEROMONE_GAIN = 0.05
DEFAULT_EVAPORATION_RATE = 0.95
MIN_EDGE_WEIGHT = 0.01


class NodeKind(StrEnum):
    """The kind of thing a semantic node represents."""

    CONCEPT = "concept"
    STATE = "state"
    AGENT = "agent"
    METRIC = "metric"
    MODEL = "model"


class RelationKind(StrEnum):
    """The kind of relation a semantic edge represents."""

    INFLUENCES = "influences"
    GENERATES = "generates"
    STABILIZES = "stabilizes"
    CONTRADICTS = "contradicts"
    EXTENDS = "extends"
    ABSTRACTS = "abstracts"


@dataclass(frozen=True)
class SemanticNode:
    """A node in the semantic map: a concept, state, agent, metric or model."""

    id: str
    label: str
    kind: NodeKind = NodeKind.CONCEPT


@dataclass(frozen=True)
class SemanticEdge:
    """A typed, weighted, directed relation between two semantic nodes.

    `weight` is the usage (pheromone) weight: how often this route is
    walked. `quality` is a separate reliability score: how often walks
    along this route were marked successful. The two are independent —
    a heavily used edge is not necessarily a high-quality one.
    """

    source: str
    target: str
    relation: RelationKind
    weight: float = 1.0
    quality: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError("weight must be in [0, 1]")
        if not 0.0 <= self.quality <= 1.0:
            raise ValueError("quality must be in [0, 1]")

    def key(self) -> tuple[str, str, str]:
        """Returns the (source, target, relation) identity of this edge."""
        return (self.source, self.target, self.relation.value)


@dataclass(frozen=True)
class PheromoneTrace:
    """A single traversal recorded against a map — a footprint left by an actor.

    `actor` identifies who walked the path (a human, an agent, a model
    name); `path` is the sequence of node ids visited, in order.
    """

    actor: str
    path: tuple[str, ...]


@dataclass
class SemanticMap:
    """A directed, typed graph of concepts, states, agents, metrics and models.

    This is the navigable topography genesis-scope projects domain
    knowledge onto: nodes are the landmarks, edges are the (typed,
    weighted) routes between them.
    """

    name: str = "default"
    nodes: dict[str, SemanticNode] = field(default_factory=dict)
    edges: list[SemanticEdge] = field(default_factory=list)
    trail: list[PheromoneTrace] = field(default_factory=list)

    def add_node(self, node: SemanticNode) -> None:
        """Registers a node, keyed by its id."""
        self.nodes[node.id] = node

    def add_edge(self, edge: SemanticEdge) -> None:
        """Registers an edge. Both endpoints must already be registered nodes."""
        if edge.source not in self.nodes:
            raise ValueError(f"unknown source node: {edge.source}")
        if edge.target not in self.nodes:
            raise ValueError(f"unknown target node: {edge.target}")
        self.edges.append(edge)

    def outgoing(self, node_id: str) -> list[SemanticEdge]:
        """Returns all edges starting at `node_id`."""
        return [edge for edge in self.edges if edge.source == node_id]

    def incoming(self, node_id: str) -> list[SemanticEdge]:
        """Returns all edges ending at `node_id`."""
        return [edge for edge in self.edges if edge.target == node_id]

    def trace(self, start: str, end: str) -> list[str] | None:
        """Returns an explicit path of node ids from `start` to `end`.

        Finds the shortest directed path (by number of edges, BFS) and
        returns it as a list of node ids, e.g. ["crep", "governance",
        "diamond"]. Returns None if no path exists.
        """
        if start not in self.nodes:
            raise ValueError(f"unknown node id: {start}")
        if end not in self.nodes:
            raise ValueError(f"unknown node id: {end}")
        if start == end:
            return [start]

        visited = {start}
        queue: deque[list[str]] = deque([[start]])
        while queue:
            path = queue.popleft()
            for edge in self.outgoing(path[-1]):
                if edge.target == end:
                    return [*path, end]
                if edge.target not in visited:
                    visited.add(edge.target)
                    queue.append([*path, edge.target])
        return None

    def attractors(self, top_n: int = 5, by: str = "weight") -> list[tuple[str, float]]:
        """Ranks nodes by attractor strength (weighted in-degree).

        Attractor strength of a node is the sum of either the usage
        `weight` or the `quality` of all edges pointing at it — how
        strongly other concepts are pulled toward it. `by` selects
        which dimension to rank on: "weight" (the default) surfaces
        the most-used attractors, "quality" surfaces the most reliable
        ones. These can disagree: a frequently walked node need not be
        a high-quality one. Returns the top `top_n` (node_id, score)
        pairs, sorted descending by score, then ascending by node id.
        """
        if top_n < 1:
            raise ValueError("top_n must be >= 1")
        if by not in ("weight", "quality"):
            raise ValueError("by must be 'weight' or 'quality'")
        scores: dict[str, float] = dict.fromkeys(self.nodes, 0.0)
        for edge in self.edges:
            scores[edge.target] += edge.weight if by == "weight" else edge.quality
        ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        return ranked[:top_n]

    def walk(
        self,
        actor: str,
        path: list[str],
        gain: float = DEFAULT_PHEROMONE_GAIN,
        success: bool | None = True,
    ) -> PheromoneTrace:
        """Lays a pheromone trail along `path`, walked by `actor`.

        Every directed edge connecting consecutive nodes in `path` has
        `gain` added to its usage `weight` (clamped to 1.0) — the more
        often a route is actually used, the stronger it stands out in
        the map. This happens regardless of `success`: usage tracks how
        often a path is walked, not how well it went.

        `success` separately moves each edge's `quality` toward 1.0
        (on success) or 0.0 (on failure) by `gain`, clamped to [0, 1].
        Pass `success=None` to record usage without affecting quality —
        e.g. when an outcome wasn't observed. This keeps "frequently
        used" and "good" as independent dimensions: a path can be
        frequent and unreliable, or rare and excellent.

        The traversal itself is appended to `self.trail`, so usage
        history (who walked where) can be inspected later.

        Raises ValueError if `path` has fewer than two nodes, or if any
        consecutive pair is not connected by an existing edge.
        """
        if len(path) < 2:
            raise ValueError("path must contain at least two nodes")
        if not 0.0 < gain <= 1.0:
            raise ValueError("gain must be in (0, 1]")

        for source, target in zip(path, path[1:], strict=False):
            matches = [
                i
                for i, edge in enumerate(self.edges)
                if edge.source == source and edge.target == target
            ]
            if not matches:
                raise ValueError(f"no edge from '{source}' to '{target}'")
            for i in matches:
                edge = self.edges[i]
                new_weight = min(1.0, edge.weight + gain)
                if success is None:
                    new_quality = edge.quality
                elif success:
                    new_quality = min(1.0, edge.quality + gain)
                else:
                    new_quality = max(0.0, edge.quality - gain)
                self.edges[i] = SemanticEdge(
                    edge.source, edge.target, edge.relation, new_weight, new_quality
                )

        trace = PheromoneTrace(actor=actor, path=tuple(path))
        self.trail.append(trace)
        return trace

    def evaporate(
        self, rate: float = DEFAULT_EVAPORATION_RATE, floor: float = MIN_EDGE_WEIGHT
    ) -> None:
        """Evaporates pheromones: decays every edge weight toward `floor`.

        Each edge's weight is multiplied by `rate` (e.g. 0.95 retains
        95% per step) but never drops below `floor`. Edges repeatedly
        reinforced by `walk()` stay strong despite evaporation; edges
        that fall out of use fade toward the floor — rare paths
        gradually become faint without ever fully disappearing.
        """
        if not 0.0 < rate <= 1.0:
            raise ValueError("rate must be in (0, 1]")
        if not 0.0 <= floor <= 1.0:
            raise ValueError("floor must be in [0, 1]")

        for i, edge in enumerate(self.edges):
            new_weight = max(floor, edge.weight * rate)
            self.edges[i] = SemanticEdge(
                edge.source, edge.target, edge.relation, new_weight, edge.quality
            )

    def footprints(self) -> dict[str, int]:
        """Returns how many traversals each actor has recorded in `self.trail`."""
        counts: dict[str, int] = {}
        for trace in self.trail:
            counts[trace.actor] = counts.get(trace.actor, 0) + 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        """Serializes this map to a JSON-compatible dict."""
        return {
            "name": self.name,
            "nodes": [
                {"id": node.id, "label": node.label, "kind": node.kind.value}
                for node in self.nodes.values()
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "relation": edge.relation.value,
                    "weight": edge.weight,
                    "quality": edge.quality,
                }
                for edge in self.edges
            ],
            "trail": [
                {"actor": trace.actor, "path": list(trace.path)} for trace in self.trail
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SemanticMap:
        """Deserializes a map from a dict produced by `to_dict`."""
        semantic_map = cls(name=data.get("name", "default"))
        for node in data.get("nodes", []):
            semantic_map.add_node(
                SemanticNode(id=node["id"], label=node["label"], kind=NodeKind(node["kind"]))
            )
        for edge in data.get("edges", []):
            semantic_map.add_edge(
                SemanticEdge(
                    source=edge["source"],
                    target=edge["target"],
                    relation=RelationKind(edge["relation"]),
                    weight=edge.get("weight", 1.0),
                    quality=edge.get("quality", 1.0),
                )
            )
        for trace in data.get("trail", []):
            semantic_map.trail.append(
                PheromoneTrace(actor=trace["actor"], path=tuple(trace["path"]))
            )
        return semantic_map


@dataclass(frozen=True)
class DriftReport:
    """The semantic drift between two snapshots of a `SemanticMap`.

    Captures where the map's meaning has shifted: nodes and edges
    added or removed, edges whose usage `weight` changed
    (`reweighted_edges`), and edges whose `quality` changed
    (`requalified_edges`). The two are reported separately: a path can
    become more used without becoming better, or more reliable without
    becoming busier.
    """

    added_nodes: list[str]
    removed_nodes: list[str]
    added_edges: list[tuple[str, str, str]]
    removed_edges: list[tuple[str, str, str]]
    reweighted_edges: list[tuple[str, str, str, float, float]]
    requalified_edges: list[tuple[str, str, str, float, float]]

    def has_drift(self) -> bool:
        """Returns True if anything changed between the two snapshots."""
        return bool(
            self.added_nodes
            or self.removed_nodes
            or self.added_edges
            or self.removed_edges
            or self.reweighted_edges
            or self.requalified_edges
        )


def compare_maps(previous: SemanticMap, current: SemanticMap) -> DriftReport:
    """Compares two snapshots of a semantic map and reports the drift.

    `previous` is the earlier snapshot, `current` the later one.
    """
    prev_ids = set(previous.nodes)
    curr_ids = set(current.nodes)
    added_nodes = sorted(curr_ids - prev_ids)
    removed_nodes = sorted(prev_ids - curr_ids)

    prev_edges = {edge.key(): edge.weight for edge in previous.edges}
    curr_edges = {edge.key(): edge.weight for edge in current.edges}
    prev_quality = {edge.key(): edge.quality for edge in previous.edges}
    curr_quality = {edge.key(): edge.quality for edge in current.edges}

    added_edges = sorted(key for key in curr_edges if key not in prev_edges)
    removed_edges = sorted(key for key in prev_edges if key not in curr_edges)
    reweighted_edges = sorted(
        (*key, prev_edges[key], curr_edges[key])
        for key in prev_edges
        if key in curr_edges and prev_edges[key] != curr_edges[key]
    )
    requalified_edges = sorted(
        (*key, prev_quality[key], curr_quality[key])
        for key in prev_quality
        if key in curr_quality and prev_quality[key] != curr_quality[key]
    )

    return DriftReport(
        added_nodes=added_nodes,
        removed_nodes=removed_nodes,
        added_edges=added_edges,
        removed_edges=removed_edges,
        reweighted_edges=reweighted_edges,
        requalified_edges=requalified_edges,
    )


@dataclass(frozen=True)
class PerspectiveComparison:
    """The result of comparing multiple agents' maps of the same space.

    `shared_*` are the nodes/edges every perspective agrees on.
    `unique_*` are, per perspective name, the nodes/edges only that
    perspective sees.
    """

    shared_nodes: list[str]
    unique_nodes: dict[str, list[str]]
    shared_edges: list[tuple[str, str, str]]
    unique_edges: dict[str, list[tuple[str, str, str]]]


def compare_perspectives(maps: dict[str, SemanticMap]) -> PerspectiveComparison:
    """Compares multiple named semantic maps of the same concept space.

    Each entry in `maps` is one perspective (e.g. one agent's or one
    model's cartography of the same domain). Returns the nodes and
    edges shared by all perspectives, and those unique to each one.
    """
    if len(maps) < 2:
        raise ValueError("compare_perspectives requires at least two maps")

    node_sets = {name: set(m.nodes) for name, m in maps.items()}
    shared_nodes = sorted(set.intersection(*node_sets.values()))
    unique_nodes = {
        name: sorted(ids - set().union(*(s for other, s in node_sets.items() if other != name)))
        for name, ids in node_sets.items()
    }

    edge_sets = {name: {edge.key() for edge in m.edges} for name, m in maps.items()}
    shared_edges = sorted(set.intersection(*edge_sets.values()))
    unique_edges = {
        name: sorted(
            keys - set().union(*(s for other, s in edge_sets.items() if other != name))
        )
        for name, keys in edge_sets.items()
    }

    return PerspectiveComparison(
        shared_nodes=shared_nodes,
        unique_nodes=unique_nodes,
        shared_edges=shared_edges,
        unique_edges=unique_edges,
    )


def _build_default_map() -> SemanticMap:
    """Builds the seed cartography of the GenesisAeon ecosystem.

    Encodes two example traces through the concept space:

        CREP -> Governance -> Diamond -> Claim-System -> Agentenkoordination
        Quasikristalle -> Informationsgeometrie -> Topologie ->
            Semantische Zustaende -> Scope

    plus the cross-links that make Scope, GenesisOS, Diamond and the
    Unified Mandala attractors in the map.
    """
    semantic_map = SemanticMap(name="genesisaeon")

    for node in (
        SemanticNode(id="crep", label="CREP", kind=NodeKind.METRIC),
        SemanticNode(id="governance", label="Governance", kind=NodeKind.CONCEPT),
        SemanticNode(id="diamond", label="Diamond", kind=NodeKind.MODEL),
        SemanticNode(id="claim_system", label="Claim-System", kind=NodeKind.CONCEPT),
        SemanticNode(id="agent_coordination", label="Agentenkoordination", kind=NodeKind.AGENT),
        SemanticNode(id="quasicrystals", label="Quasikristalle", kind=NodeKind.CONCEPT),
        SemanticNode(id="info_geometry", label="Informationsgeometrie", kind=NodeKind.CONCEPT),
        SemanticNode(id="topology", label="Topologie", kind=NodeKind.CONCEPT),
        SemanticNode(id="semantic_states", label="Semantische Zustaende", kind=NodeKind.STATE),
        SemanticNode(id="scope", label="Scope", kind=NodeKind.MODEL),
        SemanticNode(id="genesis_os", label="GenesisOS", kind=NodeKind.MODEL),
        SemanticNode(id="unified_mandala", label="Unified Mandala", kind=NodeKind.CONCEPT),
    ):
        semantic_map.add_node(node)

    for edge in (
        SemanticEdge("crep", "governance", RelationKind.INFLUENCES, 0.9),
        SemanticEdge("governance", "diamond", RelationKind.GENERATES, 0.85),
        SemanticEdge("diamond", "claim_system", RelationKind.GENERATES, 0.8),
        SemanticEdge("claim_system", "agent_coordination", RelationKind.STABILIZES, 0.75),
        SemanticEdge("agent_coordination", "crep", RelationKind.INFLUENCES, 0.6),
        SemanticEdge("quasicrystals", "info_geometry", RelationKind.ABSTRACTS, 0.8),
        SemanticEdge("info_geometry", "topology", RelationKind.ABSTRACTS, 0.8),
        SemanticEdge("topology", "semantic_states", RelationKind.GENERATES, 0.85),
        SemanticEdge("semantic_states", "scope", RelationKind.EXTENDS, 0.9),
        SemanticEdge("crep", "scope", RelationKind.INFLUENCES, 0.6),
        SemanticEdge("agent_coordination", "genesis_os", RelationKind.INFLUENCES, 0.8),
        SemanticEdge("scope", "genesis_os", RelationKind.STABILIZES, 0.85),
        SemanticEdge("diamond", "unified_mandala", RelationKind.EXTENDS, 0.7),
        SemanticEdge("scope", "unified_mandala", RelationKind.EXTENDS, 0.7),
    ):
        semantic_map.add_edge(edge)

    return semantic_map


DEFAULT_MAP: SemanticMap = _build_default_map()
