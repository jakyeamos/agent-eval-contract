# Planning State

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-07-04)

**Core value:** Keep agent-eval-contract healthy with behavior-preserving,
evidence-backed release and CLI changes.
**Current focus:** Agent Eval Contract command-surface and release-candidate cleanup

## Milestone

**Name:** Command Surface Cleanup
**Status:** Complete in isolated worktree; awaiting merge and final tag decision
**Started:** 2026-07-17

## Active Phase

- **Phase:** CLI compatibility and release truth
- **Slug:** `agent-eval-contract-command-surface-cleanup`
- **Status:** Complete
- **Plan:** Implement, verify, and commit the focused cleanup in an isolated worktree.

## Completed Scope

- Added ergonomic root `--help`/`--version` behavior while preserving `version` and `agent-eval-contract-fixtures`.
- Added focused CLI and release-metadata compatibility tests.
- Marked 0.3.0 as an unpublished public-package candidate because PyPI latest is 0.2.0.
- Added package/tag metadata checks and expanded CI/release packaged smoke coverage.
- Passed the 40-test/type/format/lint/dead-code/build/artifact/smoke ladder.

## Workflow Notes

- Work was performed only in `/Users/jakyeamos/Documents/Codex/2026-07-17/agent-eval-contract/worktree`.
- The user's existing checkout, main branch, tags, registries, and release workflow were not mutated.
- Publication remains intentionally blocked until a final tag points at the merged cleanup commit.

## Accumulated Context

- 2026-07-17: PyPI metadata verified at 0.2.0; repository source candidate is 0.3.0 and existing `v0.3.0` predates this cleanup.
- 2026-07-17: Fresh wheel smoke covered `--help`, `--version`, `version`, `validate`, `inspect`, both normalizers, `schemas`, `fixtures`, and the compatibility executable.

## Next Command

```bash
gh workflow run release.yml --ref <final-tag>
```

Run only after merging and intentionally finalizing the release tag; then
verify the published version from PyPI and update candidate metadata.
