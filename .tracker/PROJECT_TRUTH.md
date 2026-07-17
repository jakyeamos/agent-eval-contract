---
schemaVersion: 1
projectName: Agent Eval Contract
summary: Agent Eval Contract has a 0.3.0 public-package candidate with canonical CLI root version/help compatibility and explicit publication blockers.
healthScore: 96
statusLabel: healthy
nextStep: Merge the isolated cleanup commit, finalize a release tag from the merged commit, run gh workflow run release.yml --ref <final-tag>, then verify the published package from PyPI.
blockers:
  - PyPI latest is 0.2.0; the 0.3.0 candidate is not published.
  - Existing v0.3.0 points at the pre-cleanup commit; a final tag decision is required before publication.
lastUpdated: 2026-07-17
tags: [agent-eval, contract, eval, pydantic, python]
areas: [engineering]
goals: []
repoType: library
sourceOfTruth: mixed
primaryLanguage: Python
activeBranch: codex/agent-eval-contract-command-surface-cleanup-20260717
lastCommitDate: 2026-07-17
quality:
  lint: pass
  format: pass
  types: pass
  tests: pass
  deadCode: pass
  build: pass
  artifactMetadata: pass
  packagedSmoke: pass
  publication: pending
canonicalCommands:
  install: uv sync --dev
  lint: uv run ruff check agent_eval_contract tests scripts
  format: uv run ruff format --check agent_eval_contract tests scripts
  typecheck: uv run basedpyright agent_eval_contract tests scripts
  test: uv run pytest -q
  deadcode: uv run --with vulture vulture agent_eval_contract tests scripts --min-confidence 70
  releaseCheck: uv run python scripts/check_release_metadata.py
  build: uv build --out-dir /tmp/agent-eval-contract-dist
  artifactCheck: uv run --with twine twine check /tmp/agent-eval-contract-dist/*
  packagedSmoke: fresh venv agent-eval-contract --help/--version/version/validate/inspect/normalize/schemas/fixtures plus agent-eval-contract-fixtures
agentExpectationsVersion: 1
---

## Current State

The repository contains the 0.3.0 source candidate for the public
`agent-eval-contract` package. PyPI still publishes 0.2.0, so release metadata
is `public_package_candidate` with explicit blockers and no publication was
performed. The canonical `agent-eval-contract` executable now supports root
`--help` and `--version` alongside the existing `version` subcommand; the
`agent-eval-contract-fixtures` compatibility executable remains available.

The isolated cleanup worktree passed the 40-test suite, Ruff lint and format,
basedpyright, vulture, source release metadata checks, wheel/sdist twine
checks, and fresh-venv packaged CLI smoke checks.

## What Exists

- `agent_eval_contract/models.py`, `validators.py`, `schema_export.py`, and `external.py` provide the public contract models and helpers.
- `agent_eval_contract/cli.py` provides `fixtures`, `schemas`, `validate`, `inspect`, `normalize`, `version`, root `--help`, and root `--version`.
- `agent_eval_contract/fixture_runner.py` provides the fixture compatibility entrypoint.
- `scripts/check_release_metadata.py` keeps package version, release metadata, and final tag names aligned.
- `docs/release-checklist.md` and `RELEASE.md` document candidate state, checks, tagging, publication, and registry smoke.
- `.github/workflows/ci.yml` and `.github/workflows/release.yml` run the metadata gate and packaged CLI smoke surfaces.

## What Does Not Exist Yet

- The 0.3.0 package is not published to PyPI.
- The final release tag has not been selected from the merged cleanup commit.
- No long-term AIOS-specific adapter package exists in this repo.

## Next Step

Merge the isolated commit, decide the final tag, tag the merged release commit,
run the documented workflow command, and verify the installed registry package.

## Quality Ladder Notes

Checks run on 2026-07-17 in the isolated worktree:

| Step | Status | Evidence |
| --- | --- | --- |
| Ruff lint | Pass | `uv run ruff check agent_eval_contract tests scripts` |
| Ruff format | Pass | `uv run ruff format --check agent_eval_contract tests scripts` |
| Type check | Pass | `uv run basedpyright agent_eval_contract tests scripts` reported 0 errors, 0 warnings, 0 notes. |
| Tests | Pass | `uv run pytest -q` passed 40 tests. |
| Dead code | Pass | vulture at minimum confidence 70 reported no findings. |
| Release metadata | Pass | Project version, bundled metadata, and `v0.3.0` tag name agree. |
| Build | Pass | Built 0.3.0 wheel and sdist. |
| Artifact metadata | Pass | twine check passed for both artifacts. |
| Packaged smoke | Pass | Fresh venv covered canonical and compatibility executables plus all documented first-run commands. |
| Publication | Hold | PyPI latest is 0.2.0; no publish command was run. |

## Release Readiness Work (2026-07-17)

Implemented the command-surface cleanup, added focused root help/version
compatibility tests, made candidate/published release metadata states
incompatible with contradictory blockers, added a version/tag metadata gate,
expanded CI/release smoke coverage, and updated README/release documentation
to distinguish the 0.3.0 candidate from the published 0.2.0 package.

The existing `v0.3.0` tag predates this cleanup. Do not run
`gh workflow run release.yml --ref v0.3.0` until the final release tag points
at the merged cleanup commit.

## Agent Notes

Do not publish the public package from the existing pre-cleanup tag. After the
final tag decision and successful registry smoke, update release metadata to
`published` with an empty blocker list in a follow-up truth update.

The device commit gate shells out to the `pre-cr` CLI, which previously needed
a local typescript-store symlink repair; preserve that workaround if the hook
regresses after dependency pruning.

## QR Remediation Planning

The older GSD QR remediation plan remains separate from this command-surface
cleanup; no unrelated QR phase execution was started here.
