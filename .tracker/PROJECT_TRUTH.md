---
schemaVersion: 1
projectName: Agent Eval Contract
summary: Portable dependency-free Python contracts for agent eval schemas, validators, templates, samples, external result normalization, and clean-room fixture generation are extracted from AIOS and release-checkable.
healthScore: 78
statusLabel: needs_attention
nextStep: Resolve the BasedPyright pytest import warning, then tag v0.1.0 and update AIOS dependency policy after tag consumption is verified.
blockers:
  - Tagged dependency consumption from AIOS is not recorded yet.
  - A second non-AIOS consumer has not been proven yet.
lastUpdated: 2026-06-27
tags: [aios, contract, eval, python]
areas: [engineering]
goals: []
repoType: library
sourceOfTruth: mixed
primaryLanguage: Python
activeBranch: main
lastCommitDate: 2026-06-27
quality:
  lint: pass
  types: warning
  tests: pass
  deadCode: unknown
  structure: warning
canonicalCommands:
  install: uv sync
  dev: unknown
  lint: uv run ruff check agent_eval_contract tests
  typecheck: uv run basedpyright agent_eval_contract tests
  test: uv run pytest -q
  deadcode: unknown
agentExpectationsVersion: 1
---

## Current State

Agent Eval Contract is an extracted AIOS contract package. It owns portable eval vocabulary, TypedDict schemas, validators, templates, bundled samples, external benchmark normalization, clean-room fixture generation, and release metadata. AIOS still owns SQLite eval storage, peer traces, shadow worktrees, second-brain lift, operator projections, and workflow integration.

The package is dependency-free at runtime and has a `0.1.0` release surface. The README and release governance are now public-ready enough for a small contract package, but the release blockers in the fixture-runner metadata are still real.

## What Exists

- `agent_eval_contract/schemas.py` for context profile, status, priority, score, task, run, score, and failure record contracts.
- `agent_eval_contract/validators.py` for runtime contract validation.
- `agent_eval_contract/templates.py` for template validation and rendering.
- `agent_eval_contract/samples.py` for bundled sample records.
- `agent_eval_contract/external.py` for external benchmark result normalization.
- `agent_eval_contract/clean_room.py` and `agent_eval_contract/fixture_runner.py` for clean-room fixture bundle generation.
- `release_metadata.json` and `RELEASE.md` documenting the AIOS boundary.
- Tests covering the contract package.

## What Does Not Exist Yet

- No tagged GitHub release is recorded in this truth snapshot.
- No second non-AIOS consumer is proven.
- No AIOS dependency-policy update after a tag is recorded here.
- No dead-code scanner is configured.

## Next Step

Fix or explicitly document the BasedPyright `pytest` import warning in the test environment, then tag v0.1.0 and verify AIOS consumes the tagged package rather than relying only on a local path.

## Quality Ladder Notes

Checks run on 2026-06-27:

| Step | Status | Evidence |
| --- | --- | --- |
| Lint | Pass | `uv run ruff check agent_eval_contract tests` passed. |
| Format | Pass | `uv run ruff format --check agent_eval_contract tests` reported 10 files already formatted. |
| Type check | Warning | `uv run basedpyright agent_eval_contract tests` exited 0 with one `pytest` import warning. |
| Tests | Pass | `uv run pytest -q` passed with 9 tests. |
| Fixture generation | Pass | `uv run python -m agent_eval_contract.fixture_runner --output-dir /tmp/agent-eval-contract-fixtures` succeeded with clean-room `ok: true`. |
| Structure | Warning | `pre-cr run --workspace .` exited 1 because changed-line readiness did not produce a coverage result in the clean worktree. |
| Dead code | Unknown | No Vulture or equivalent dead-code command is configured. |

## Agent Notes

Keep this repo as a portable contract package. Do not move AIOS persistence, workflow routing, or second-brain behavior into it. Breaking schema, validation, export, or package-shape changes should be treated as major releases.
