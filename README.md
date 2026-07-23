# Agent Eval Contract

[![CI](https://github.com/jakyeamos/agent-eval-contract/actions/workflows/ci.yml/badge.svg)](https://github.com/jakyeamos/agent-eval-contract/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/agent-eval-contract.svg)](https://pypi.org/project/agent-eval-contract/)
[![Python versions](https://img.shields.io/pypi/pyversions/agent-eval-contract.svg)](https://pypi.org/project/agent-eval-contract/)
[![License: MIT](https://img.shields.io/pypi/l/agent-eval-contract.svg)](LICENSE)
[![Typed](https://img.shields.io/badge/types-py.typed-blue.svg)](agent_eval_contract/py.typed)

Pydantic contracts and JSON Schemas for portable agent evaluation records.

Use this package when you are experimenting with agents, harnesses, CI checks, or benchmark runners and need a stable record shape for tasks, runs, scores, failures, and normalized external results.

## Release status

This source checkout targets `v0.3.0`. PyPI currently publishes `v0.2.0`; the
existing `v0.3.0` tag has passed the local package and consumer gates, but its
GitHub release and PyPI publication are still pending trusted-publisher
configuration. `pip install agent-eval-contract` therefore resolves the
verified `v0.2.0` registry release until that workflow succeeds.

## What this is

A small contract layer for agent evaluation records:

- validate eval task/run/score/failure records
- export JSON Schemas
- normalize common harness output
- provide fixtures and examples for downstream tools

## What this is not

- not an eval runner
- not an agent framework
- not a benchmark suite
- not a storage layer
- not a dashboard
- not a model-provider client

It gives those tools a shared contract; it does not replace them.

## Should you use this?

Use this if:

- you already run agent evals and need a common record shape
- you want JSON Schema for eval artifacts
- you need lightweight validation in CI
- you want to normalize outputs from multiple harnesses

Do not use this if:

- you need an eval runner
- you need model calls
- you need a hosted dashboard
- you need a benchmark dataset
- you need agent orchestration

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
agent-eval-contract validate --kind run --file examples/eval_run.json --quiet   # exit code only
agent-eval-contract validate --kind run --file examples/eval_run.json --pretty  # indented JSON
agent-eval-contract inspect --file examples/eval_run.json   # report which models the file matches
agent-eval-contract schemas --output-dir /tmp/agent-eval-contract-schemas
agent-eval-contract fixtures --output-dir /tmp/agent-eval-contract-fixtures
agent-eval-contract normalize --harness terminal-bench --file examples/terminal_bench_result.json --task-id task-login-flow-001 --model gpt-5
agent-eval-contract normalize --harness swe-bench --file examples/swe_bench_result.json
agent-eval-contract version   # package and contract versions, for CI/debugging
```

`validate` prints a friendly, field-oriented message on failure and exits non-zero; add `--json-errors` for raw structured errors. The legacy `agent-eval-contract-fixtures` command still writes fixture bundles for one release.

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

### Top-level fields are strict by design

All public models reject unknown top-level fields (`extra="forbid"`). Use `metadata` for harness-specific or project-specific extensions. This is intentional: the record shape is the contract, so a typo or a stray private field fails fast instead of silently traveling between tools.

See [docs/contract.md](docs/contract.md), [docs/field-reference.md](docs/field-reference.md), and [docs/adapters.md](docs/adapters.md) for the model contract and adapter guidance.

## Stability

Package versions follow SemVer for the Python API; the contract version tracks the JSON record/schema shape. See [docs/stability.md](docs/stability.md) for the full policy.

## Security

See [SECURITY.md](SECURITY.md) for how to report vulnerabilities and the package's supply-chain stance.

## Development

```bash
uv run ruff check agent_eval_contract tests
uv run ruff format --check agent_eval_contract tests
uv run basedpyright agent_eval_contract tests
uv run pytest -q
uv build --out-dir /tmp/agent-eval-contract-dist
```
