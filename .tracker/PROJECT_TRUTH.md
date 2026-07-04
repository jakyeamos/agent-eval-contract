---
schemaVersion: 1
projectName: Agent Eval Contract
summary: Public Pydantic contract package for portable agent evaluation records, validators, JSON Schema export, fixture bundles, and external harness normalization.
healthScore: 92
statusLabel: healthy
nextStep: Monitor early install/use feedback and decide whether to add a dedicated AIOS adapter package separately.
blockers: []
lastUpdated: 2026-07-04
tags: [agent-eval, contract, eval, pydantic, python]
areas: [engineering]
goals: []
repoType: library
sourceOfTruth: mixed
primaryLanguage: Python
activeBranch: main
lastCommitDate: 2026-07-04
quality:
  lint: pass
  types: pass
  tests: pass
  deadCode: pass
  structure: pass
canonicalCommands:
  install: uv sync --dev
  dev: unknown
  lint: uv run ruff check agent_eval_contract tests
  typecheck: uv run basedpyright agent_eval_contract tests
  test: uv run pytest -q
  deadcode: uv run --with vulture vulture agent_eval_contract tests --min-confidence 70
agentExpectationsVersion: 1
---

## Current State

Agent Eval Contract is now published on PyPI at version 0.2.0. It defines Pydantic models for eval tasks, runs, scores, failures, external results, normalized runs, and fixture bundle manifests. It includes runtime validators, JSON Schema export, bundled samples/templates, Terminal-Bench and SWE-bench normalization helpers, package metadata, docs, examples, and CI.

The old internal extraction framing has been removed from the public core. Project-specific workflow vocabulary should live in `metadata` or a separate adapter package.

## What Exists

- `agent_eval_contract/models.py` for public Pydantic models and vocabulary.
- `agent_eval_contract/validators.py` for runtime validation helpers returning typed model instances.
- `agent_eval_contract/schema_export.py` for JSON Schema export.
- `agent_eval_contract/external.py` for generic, Terminal-Bench, and SWE-bench normalization.
- `agent_eval_contract/cli.py` for `fixtures`, `schemas`, `validate`, and `normalize` commands.
- `agent_eval_contract/fixture_runner.py` for fixture bundle generation and the deprecated compatibility entrypoint.
- `docs/contract.md`, `docs/field-reference.md`, and `docs/adapters.md` for public package docs.
- `.github/workflows/ci.yml` for lint, format, typecheck, tests, dead-code scan, build, and installed CLI smoke.

## What Does Not Exist Yet

- No long-term AIOS-specific adapter package exists in this repo.

## Next Step

Monitor early install/use feedback and keep AIOS-specific vocabulary in a separate adapter package rather than the public core.

## Quality Ladder Notes

Checks run on 2026-07-04 after the 0.2.0 version bump:

| Step | Status | Evidence |
| --- | --- | --- |
| Lint | Pass | `uv run ruff check agent_eval_contract tests` passed. |
| Format | Pass | `uv run ruff format --check agent_eval_contract tests` passed. |
| Type check | Pass | `uv run basedpyright agent_eval_contract tests` passed with 0 errors and 0 warnings. |
| Tests | Pass | `uv run pytest -q` passed with 15 tests. |
| Dead code | Pass | `uv run --with vulture vulture agent_eval_contract tests --min-confidence 70` reported no findings. |
| Pre-CR | Pass | `uv run --with pytest python scripts/pre_cr_coverage.py` passed. |
| Build | Pass | `uv build --out-dir /tmp/agent-eval-contract-dist` built `agent_eval_contract-0.2.0` wheel and sdist. |
| Installed smoke | Pass | Installed the `0.2.0` wheel in a fresh venv, validated records, exported schemas, and normalized Terminal-Bench and SWE-bench examples. |
| Publish | Pass | `uv publish` uploaded the `0.2.0` wheel and sdist to PyPI. |
| Registry smoke | Pass | Installed `agent-eval-contract==0.2.0` from PyPI in a fresh venv, validated records, exported schemas, and normalized Terminal-Bench and SWE-bench examples. |

## Agent Notes

Do not publish the public package as `0.1.0`: the existing `v0.1.0` tag points to the older extraction commit. Version `0.2.0` is the intended public release version.
