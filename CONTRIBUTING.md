# Contributing

Thanks for your interest in contributing to this GenesisAeon ecosystem
package!

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
   (or `.venv\Scripts\activate` on Windows). Alternatively, use `uv sync --dev`.
3. Install in editable mode with dev dependencies:
   `pip install -e ".[dev]"`.
4. Run the test suite: `pytest`.

## Code style

- Format and lint with `ruff check .`.
- Type-check with `mypy src` (strict mode is enabled).
- Keep functions documented with concise docstrings.

## Diamond Interface

`genesis-scope` implements the GenesisAeon Diamond Interface
(`run_cycle`, `get_crep_state`, `get_utac_state`, `get_phase_events`,
`to_zenodo_record`) on the `GenesisScope` class in `src/genesis_scope/system.py`.
Any change to these methods' signatures or return shapes is a **breaking
change** and requires a MAJOR version bump (see `RELEASE_GUIDE.md`).

## Pull requests

- One logical change per PR.
- Add or update tests for any behavioral change.
- Update `CHANGELOG.md` under an `## [Unreleased]` section.
- Fill out the PR template (`.github/PULL_REQUEST_TEMPLATE.md`).

## Reporting issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` — they help us
triage bug reports vs. feature requests quickly.

## Scientific claims

This is part of a research framework. If your contribution touches any
scientific model, prediction, or benchmark (e.g. `Gamma_collab` targets in
`benchmark.py`), please:
- Cite the source (paper, dataset, or prior GenesisAeon Zenodo record).
- Clearly mark speculative vs. validated claims.
