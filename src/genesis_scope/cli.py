"""Command-line interface for genesis-scope."""

from __future__ import annotations

import json

import typer

from genesis_scope.benchmark import evaluate
from genesis_scope.cartography import DEFAULT_MAP, SemanticMap, compare_maps
from genesis_scope.drift_model import DriftModel
from genesis_scope.semantic_anchor import SemanticAnchor
from genesis_scope.system import DEFAULT_ANCHORS, GenesisScope

app = typer.Typer(help="genesis-scope — semantic coordination CLI")


@app.command()
def status(n_sessions: int = 38) -> None:
    """Run a collaboration cycle and print the current scope status."""
    scope = GenesisScope()
    result = scope.run_cycle(n_sessions=n_sessions)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def drift(n_steps: int = 10, kappa: float = 0.3, lambda_: float = 0.8) -> None:
    """Simulate semantic drift with and without anchors."""
    no_anchor = DriftModel(kappa=kappa, lambda_=lambda_, anchors=[])
    with_anchors = DriftModel(kappa=kappa, lambda_=lambda_, anchors=list(DEFAULT_ANCHORS))

    typer.echo("Without anchors:")
    for t, d in no_anchor.trajectory((0, n_steps), n_steps=n_steps):
        typer.echo(f"  t={t:6.2f}  D={d:8.4f}")

    typer.echo("With anchors:")
    for t, d in with_anchors.trajectory((0, n_steps), n_steps=n_steps):
        typer.echo(f"  t={t:6.2f}  D={d:8.4f}")


@app.command()
def benchmark(n_sessions: int = 38) -> None:
    """Evaluate genesis-scope against SCOPE_TARGETS."""
    results = evaluate(n_sessions=n_sessions)
    for name, result in results.items():
        marker = "OK" if result["passed"] else "FAIL"
        typer.echo(f"[{marker}] {name}: {result['value']} (target {result['target']})")


@app.command(name="anchor")
def anchor_info() -> None:
    """Print the registered semantic anchors (Sigillin)."""
    for a in DEFAULT_ANCHORS:
        anchor: SemanticAnchor = a
        typer.echo(
            f"{anchor.name}: compression={anchor.compression_ratio():.1f}x "
            f"strength={anchor.strength}"
        )


@app.command(name="map")
def show_map() -> None:
    """Print the semantic cartography (nodes and typed relations)."""
    semantic_map = DEFAULT_MAP
    typer.echo(f"Semantic map: {semantic_map.name}")
    typer.echo("Nodes:")
    for node in semantic_map.nodes.values():
        typer.echo(f"  {node.id:20s} [{node.kind.value:7s}] {node.label}")
    typer.echo("Edges:")
    for edge in semantic_map.edges:
        typer.echo(f"  {edge.source} --{edge.relation.value}--> {edge.target} (w={edge.weight})")


@app.command()
def trace(start: str, end: str) -> None:
    """Trace an explicit path between two nodes in the semantic map."""
    path = DEFAULT_MAP.trace(start, end)
    if path is None:
        typer.echo(f"No path found from '{start}' to '{end}'.")
        raise typer.Exit(code=1)
    typer.echo(" -> ".join(path))


@app.command()
def attractors(top_n: int = 5) -> None:
    """Rank semantic nodes by attractor strength (weighted in-degree)."""
    for node_id, score in DEFAULT_MAP.attractors(top_n=top_n):
        label = DEFAULT_MAP.nodes[node_id].label
        typer.echo(f"{node_id:20s} {label:25s} score={score:.2f}")


@app.command(name="drift-map")
def drift_map(previous: str, current: str) -> None:
    """Compare two semantic map JSON files and report the drift between them."""
    with open(previous) as f:
        prev_map = SemanticMap.from_dict(json.load(f))
    with open(current) as f:
        curr_map = SemanticMap.from_dict(json.load(f))

    report = compare_maps(prev_map, curr_map)
    if not report.has_drift():
        typer.echo("No drift detected.")
        return

    for node_id in report.added_nodes:
        typer.echo(f"+ node {node_id}")
    for node_id in report.removed_nodes:
        typer.echo(f"- node {node_id}")
    for source, target, relation in report.added_edges:
        typer.echo(f"+ edge {source} --{relation}--> {target}")
    for source, target, relation in report.removed_edges:
        typer.echo(f"- edge {source} --{relation}--> {target}")
    for source, target, relation, old_weight, new_weight in report.reweighted_edges:
        typer.echo(f"~ edge {source} --{relation}--> {target}: {old_weight} -> {new_weight}")


if __name__ == "__main__":
    app()
