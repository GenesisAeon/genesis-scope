"""Command-line interface for genesis-scope."""

from __future__ import annotations

import json

import typer

from genesis_scope.benchmark import evaluate
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


if __name__ == "__main__":
    app()
