# Release

## Current Release Candidate

- Version: `0.3.0`
- Contract version: `0.1`
- Status: public package candidate; not published to PyPI
- Source package: `agent_eval_contract`

## Public Promise

`agent-eval-contract` defines, validates, serializes, exports JSON Schema for, and normalizes portable agent evaluation records.

Releases are automated by `.github/workflows/release.yml` on a `v*` tag (build, twine check, fresh-venv CLI smoke, PyPI trusted publishing, GitHub release). See [docs/release-checklist.md](docs/release-checklist.md) for the manual steps around it.

## Publication State

As of 2026-07-17, PyPI reports `0.2.0` as the latest published version. The
repository has a `v0.3.0` source tag, but this cleanup is a post-tag change, so
the tag must be intentionally finalized after this work is merged. Publication
is not performed in this task.

Do not run `gh workflow run release.yml --ref v0.3.0` until the final release
tag points at the merged release commit. After the tag decision, the tagged
workflow performs the build, metadata checks, trusted PyPI publication, and
GitHub release; then install the published version from PyPI and rerun the CLI
smoke checks below.

## Release Checks

CI runs the same quality ladder on pull requests and pushes. Run this local block before tagging or publishing:

```bash
uv run ruff check agent_eval_contract tests scripts
uv run ruff format --check agent_eval_contract tests scripts
uv run basedpyright agent_eval_contract tests scripts
uv run pytest -q
uv run python scripts/check_release_metadata.py
uv build --out-dir /tmp/agent-eval-contract-dist
uv run --with twine twine check /tmp/agent-eval-contract-dist/*
```

Then install the wheel in a temp virtualenv and smoke test:

```bash
python -m venv /tmp/agent-eval-contract-venv
/tmp/agent-eval-contract-venv/bin/pip install /tmp/agent-eval-contract-dist/agent_eval_contract-0.3.0-py3-none-any.whl
/tmp/agent-eval-contract-venv/bin/agent-eval-contract --help
/tmp/agent-eval-contract-venv/bin/agent-eval-contract --version
/tmp/agent-eval-contract-venv/bin/agent-eval-contract version
/tmp/agent-eval-contract-venv/bin/agent-eval-contract validate --kind run --file examples/eval_run.json
/tmp/agent-eval-contract-venv/bin/agent-eval-contract inspect --file examples/eval_run.json
/tmp/agent-eval-contract-venv/bin/agent-eval-contract normalize --harness terminal-bench --file examples/terminal_bench_result.json --task-id task-login-flow-001 --model gpt-5
/tmp/agent-eval-contract-venv/bin/agent-eval-contract schemas --output-dir /tmp/agent-eval-contract-schemas
/tmp/agent-eval-contract-venv/bin/agent-eval-contract fixtures --output-dir /tmp/agent-eval-contract-fixtures
/tmp/agent-eval-contract-venv/bin/agent-eval-contract normalize --harness swe-bench --file examples/swe_bench_result.json
/tmp/agent-eval-contract-venv/bin/agent-eval-contract-fixtures --output-dir /tmp/agent-eval-contract-fixtures-compat
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
