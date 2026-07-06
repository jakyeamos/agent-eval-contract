# Release

## Current Version

- Version: `0.2.0`
- Contract version: `0.1`
- Status: public package release
- Source package: `agent_eval_contract`

## Public Promise

`agent-eval-contract` defines, validates, serializes, exports JSON Schema for, and normalizes portable agent evaluation records.

Releases are automated by `.github/workflows/release.yml` on a `v*` tag (build, twine check, fresh-venv CLI smoke, PyPI trusted publishing, GitHub release). See [docs/release-checklist.md](docs/release-checklist.md) for the manual steps around it.

## Release Checks

CI runs the same quality ladder on pull requests and pushes. Run this local block before tagging or publishing:

```bash
uv run ruff check agent_eval_contract tests
uv run ruff format --check agent_eval_contract tests
uv run basedpyright agent_eval_contract tests
uv run pytest -q
uv build --out-dir /tmp/agent-eval-contract-dist
```

Then install the wheel in a temp virtualenv and smoke test:

```bash
python -m venv /tmp/agent-eval-contract-venv
/tmp/agent-eval-contract-venv/bin/pip install /tmp/agent-eval-contract-dist/agent_eval_contract-0.2.0-py3-none-any.whl
/tmp/agent-eval-contract-venv/bin/agent-eval-contract validate --kind run --file examples/eval_run.json
/tmp/agent-eval-contract-venv/bin/agent-eval-contract schemas --output-dir /tmp/agent-eval-contract-schemas
/tmp/agent-eval-contract-venv/bin/agent-eval-contract normalize --harness swe-bench --file examples/swe_bench_result.json
```

## Boundaries

Public core:

- Pydantic record models
- runtime validation helpers
- JSON Schema export
- external harness normalization
- fixture bundle generation
- CLI validation and schema export

Out of scope:

- evaluation execution
- model provider calls
- dashboard storage
- private workflow vocabulary
- agent orchestration
