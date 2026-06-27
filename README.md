# Agent Eval Contract

<p align="center"><strong>Portable Python contracts for agent evaluation records, fixtures, templates, and release metadata.</strong></p>

<p align="center">
  <img alt="Status: extracted contract package" src="https://img.shields.io/badge/status-extracted%20contract%20package-0f766e">
  <img alt="Runtime: Python 3.12" src="https://img.shields.io/badge/runtime-Python%203.12-3776ab">
  <img alt="Dependencies: none" src="https://img.shields.io/badge/dependencies-none-111827">
  <img alt="Source: AIOS split-out" src="https://img.shields.io/badge/source-AIOS%20split--out-7c3aed">
</p>

Agent Eval Contract is a small dependency-free Python package for sharing agent-evaluation record shapes outside AIOS. It defines the portable vocabulary, schemas, validators, templates, sample records, external benchmark normalization, and fixture bundle tooling needed by eval harnesses without importing AIOS runtime or storage code.

AIOS remains the owner of SQLite persistence, peer traces, shadow worktrees, operator projections, second-brain lift, CLI orchestration, and workflow integration. This package owns only the reusable contract surface.

## What It Provides

| Surface | Purpose |
| --- | --- |
| Vocabulary | Shared context profile, status, priority, and score values. |
| TypedDict schemas | Portable eval task, run, score, and failure record shapes. |
| Validators | Runtime checks for eval records, templates, samples, and fixture bundles. |
| Templates | Template validation and rendering helpers for agent-facing eval prompts. |
| Samples | Bundled sample records for consumer smoke tests. |
| External normalization | Helpers for converting external benchmark results into the contract shape. |
| Clean-room fixtures | Fixture bundle generation for testing consumers without AIOS state. |
| Release metadata | Machine-readable boundary notes that separate portable and AIOS-owned surfaces. |

## Package Layout

| Path | Purpose |
| --- | --- |
| `agent_eval_contract/schemas.py` | Portable schema and vocabulary definitions. |
| `agent_eval_contract/validators.py` | Validation helpers for records and contract payloads. |
| `agent_eval_contract/templates.py` | Template validation and rendering. |
| `agent_eval_contract/samples.py` | Bundled sample record access. |
| `agent_eval_contract/external.py` | External benchmark normalization. |
| `agent_eval_contract/clean_room.py` | Clean-room fixture bundle helpers. |
| `agent_eval_contract/fixture_runner.py` | CLI entrypoint for writing fixture bundles. |
| `RELEASE.md` | Release checks and AIOS boundary contract. |
| `CHANGELOG.md` | Version history. |

## Install

From a local checkout:

```bash
git clone https://github.com/jakyeamos/agent-eval-contract.git
cd agent-eval-contract
uv sync
```

For editable local development:

```bash
uv pip install -e .
```

## CLI

Generate a clean-room fixture bundle:

```bash
uv run agent-eval-contract-fixtures --output-dir /tmp/agent-eval-contract-fixtures
```

Equivalent module form:

```bash
uv run python -m agent_eval_contract.fixture_runner --output-dir /tmp/agent-eval-contract-fixtures
```

## Development Checks

```bash
uv run ruff check agent_eval_contract tests
uv run ruff format --check agent_eval_contract tests
uv run basedpyright agent_eval_contract tests
uv run pytest -q
uv run python -m agent_eval_contract.fixture_runner --output-dir /tmp/agent-eval-contract-fixtures
```

## Integration Boundary

Portable in this package:

- schemas and vocabulary;
- fixture validators;
- template validators and renderers;
- bundled samples;
- external result normalization;
- clean-room fixture bundle generation;
- release metadata.

AIOS-owned outside this package:

- SQLite eval storage;
- peer traces;
- shadow worktrees;
- second-brain lift;
- operator projections;
- AIOS CLI and workflow orchestration.

## Release Checklist

Before tagging a release:

1. Update `pyproject.toml` version.
2. Update `CHANGELOG.md`.
3. Run the full development checks above.
4. Generate a fixture bundle and inspect it.
5. Commit the release changes.
6. Tag with `vX.Y.Z`.
7. Push `main` and the tag.
8. Update AIOS dependency policy after the tag is available.

## Design Rules

- Keep this package dependency-free unless a contract need is strong enough to justify coupling.
- Prefer additive schema changes for minor releases.
- Treat breaking schema, validator, export, or package-shape changes as major releases.
- Do not move AIOS runtime assumptions into this contract package.
