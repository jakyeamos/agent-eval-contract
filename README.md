# Agent Eval Contract

Portable Python contract helpers for agent evaluation records.

The package is intentionally dependency-free. It provides:

- context profile, status, priority, and score vocabulary
- eval task/run/score/failure TypedDict schemas
- harness fixture validation
- eval template validation and template rendering
- bundled sample record validation
- external benchmark result normalization
- clean-room fixture bundle generation
- release metadata separating portable contract surfaces from AIOS-owned runtime/storage

AIOS uses this package as a shared contract while keeping SQLite eval storage, peer traces, shadow worktrees, second-brain lift, operator projections, and workflow integration in AIOS.

## Development

```bash
uv run ruff check agent_eval_contract tests
uv run ruff format --check agent_eval_contract tests
uv run basedpyright agent_eval_contract tests
uv run pytest -q
uv run python -m agent_eval_contract.fixture_runner --output-dir /tmp/agent-eval-contract-fixtures
```
