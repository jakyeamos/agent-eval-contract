---
schemaVersion: 1
projectName: Agent Eval Contract
summary: Public Pydantic contract package for portable agent evaluation records, validators, JSON Schema export, fixture bundles, external harness normalization, and a lockfile-backed Quality Runner dependency-audit gate.
healthScore: 94
statusLabel: healthy
nextStep: Review the Quality Runner dependency-audit result and resolve the remaining runner vulture-cache mismatch before merging this gate branch.
blockers: []
lastUpdated: 2026-07-22
tags: [agent-eval, contract, eval, pydantic, python]
areas: [engineering]
goals: []
repoType: library
sourceOfTruth: mixed
primaryLanguage: Python
activeBranch: codex/quality-runner-dependency-gate-agent-eval
lastCommitDate: 2026-07-13
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

- The repository environment contract now has a minimal root agent router and
  `.agents/context/README.md` index for contract, adapter, compatibility,
  release, security, and quality routing.
- The 2026-07-13 Quality Runner `0.5.0` dogfood run recorded 6 dangerous-sink
  candidates and 12 total findings with no source-file changes. Commit
  `0195c28` adds a lockfile-exported `pip-audit` gate; explicit verification
  passed it with `No known vulnerabilities found`. The overall verification
  remains blocked only by QR's vulture scan traversing its generated uv cache.

Agent Eval Contract is now published on PyPI at version 0.2.0. It defines Pydantic models for eval tasks, runs, scores, failures, external results, normalized runs, and fixture bundle manifests. It includes runtime validators, JSON Schema export, bundled samples/templates, Terminal-Bench and SWE-bench normalization helpers, package metadata, docs, examples, and CI.

The old internal extraction framing has been removed from the public core. Project-specific workflow vocabulary should live in `metadata` or a separate adapter package.

## What Exists

- `agent_eval_contract/models.py` for public Pydantic models and vocabulary.
- `agent_eval_contract/validators.py` for runtime validation helpers returning typed model instances.
- `agent_eval_contract/schema_export.py` for JSON Schema export.
- `agent_eval_contract/external.py` for generic, Terminal-Bench, and SWE-bench normalization.
- `agent_eval_contract/cli.py` for `fixtures`, `schemas`, `validate`, `inspect`, `normalize`, and `version` commands (validate supports `--quiet`/`--pretty`/`--json-errors` with friendly errors).
- `agent_eval_contract/fixture_runner.py` for fixture bundle generation and the deprecated compatibility entrypoint.
- `docs/contract.md`, `docs/field-reference.md`, `docs/adapters.md`, `docs/stability.md`, `docs/writing-adapters.md`, and `docs/release-checklist.md` for public package docs.
- `SECURITY.md` for the security/supply-chain policy.
- `examples/` with single-record samples plus three runnable workflows (`ci_pytest_eval/`, `swe_bench_normalization/`, `dashboard_ingest/`).
- `tests/snapshots/` (committed schema snapshots + frozen contract-0.1 required fields) and `tests/fixtures/v0_2_0/` (frozen backward-compat fixtures).
- `.github/workflows/ci.yml` (Python 3.12/3.13/3.14) and `.github/workflows/release.yml` (tag-triggered build, twine check, PyPI trusted publishing, GitHub release).

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

## Release-Readiness Work (2026-07-05)

Implemented a 17-item external review on branch `dev` for a 0.3.0-quality release: fixed the adapter docs/API mismatch, sharpened the README promise, added a stability policy, schema snapshot tests, backward-compat fixtures + contract guardrails, Python 3.14 CI, expanded CLI (`version`/`inspect`/`--quiet`/`--pretty`/friendly errors), real-world example workflows, adapter-authoring guide, non-Python (ajv) validation docs, `SECURITY.md`, and a trusted-publishing release workflow. Version is intentionally still `0.2.0`; the actual bump/tag/publish is left as a deliberate release step (see nextStep).

Full ladder on 2026-07-05: ruff lint pass, ruff format pass, basedpyright 0/0/0, pytest 37 passed, vulture clean, `uv build` + `twine check` both pass.

## Agent Notes

Do not publish the public package as `0.1.0`: the existing `v0.1.0` tag points to the older extraction commit. Version `0.2.0` is the intended public release version.

The device commit gate shells out to the `pre-cr` CLI, which was broken (`@pre-cr/core@0.1.0` requires `typescript` but declares no such dependency). Repaired by symlinking the store's typescript package into `@pre-cr/core`'s node_modules; if it regresses after a pnpm prune/reinstall, re-create that symlink.

## QR Remediation Planning

- 2026-07-04: Added GSD Phase 1 for QR remediation from qr-low-risk-post-branch-fix-20260704-agent-eval-contract; 1 plan(s) created from agent-eval-contract.md. Execution has not started.
