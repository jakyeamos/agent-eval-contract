# Release

## Current Version

- Version: `0.1.0`
- Status: local repo extracted
- Source package: `agent_eval_contract`

## Release Checks

Run before tagging:

```bash
uv run ruff check agent_eval_contract tests
uv run ruff format --check agent_eval_contract tests
uv run basedpyright agent_eval_contract tests
uv run pytest -q
uv run python -m agent_eval_contract.fixture_runner --output-dir /tmp/agent-eval-contract-fixtures
```

## Boundary

Portable:

- schemas and vocabulary
- fixture validators
- template validators/renderers
- bundled samples
- external result normalization
- clean-room fixture bundle generation
- release metadata

AIOS-owned:

- SQLite eval storage
- peer traces
- shadow worktrees
- second-brain lift
- operator projections
- AIOS CLI and workflow orchestration
