# Agent Eval Contract

Pydantic contracts and JSON Schemas for portable agent evaluation records.

Use this package when you are experimenting with agents, harnesses, CI checks, or benchmark runners and need a stable record shape for tasks, runs, scores, failures, and normalized external results. It does not run evaluations, call model providers, store dashboards, or orchestrate agents. It gives those tools a shared contract.

## Install

```bash
pip install agent-eval-contract
```

For local development from this repo:

```bash
uv sync --dev
```

## Validate A Record

```python
from agent_eval_contract import validate_eval_run

run = validate_eval_run(
    {
        "run_id": "run-login-flow-001",
        "task_id": "task-login-flow-001",
        "harness": "pytest",
        "model": "gpt-5",
        "mode": "autonomous",
        "context_profile": "repo_only",
        "final_status": "success",
        "checks": ["pytest tests/test_auth_redirect.py -q"],
    }
)

print(run.model_dump(mode="json"))
```

Validation returns typed Pydantic model instances. Invalid records raise `pydantic.ValidationError` with structured field errors.

## CLI

```bash
agent-eval-contract validate --kind run --file examples/eval_run.json
agent-eval-contract schemas --output-dir /tmp/agent-eval-contract-schemas
agent-eval-contract fixtures --output-dir /tmp/agent-eval-contract-fixtures
agent-eval-contract normalize --harness terminal-bench --file examples/terminal_bench_result.json --task-id task-login-flow-001 --model gpt-5
```

The legacy `agent-eval-contract-fixtures` command still writes fixture bundles for one release.

## What It Provides

- Pydantic models for eval tasks, runs, scores, failures, external results, normalized runs, and fixture manifests
- runtime validators that return typed model instances
- JSON Schema export for all public models
- bundled sample records and markdown templates
- Terminal-Bench and SWE-bench oriented normalization helpers
- a small CLI for validation, schema export, fixture generation, and normalization

## Contract Vocabulary

The public core uses generic vocabulary only. Project-specific concepts should live in `metadata` or a separate adapter package.

- `context_profile`: `repo_only`, `provided_context`, `clean_room`, `tool_augmented`, `full_workspace`
- `source`: `manual`, `ci`, `benchmark`, `production_trace`, `synthetic`
- `mode`: `interactive`, `autonomous`, `shadow`, `replay`, `benchmark`
- `final_status`: `success`, `partial`, `failed`, `abandoned`, `error`

See [docs/contract.md](docs/contract.md) and [docs/adapters.md](docs/adapters.md) for the model contract and adapter guidance.

## Development

```bash
uv run ruff check agent_eval_contract tests
uv run ruff format --check agent_eval_contract tests
uv run basedpyright agent_eval_contract tests
uv run pytest -q
uv build --out-dir /tmp/agent-eval-contract-dist
```
