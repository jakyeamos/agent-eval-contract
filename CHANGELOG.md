# Changelog

## Unreleased

### Added

- CLI: `version` (package and contract versions) and `inspect` (report which models a record matches) subcommands.
- CLI: `validate` gains `--quiet`, `--pretty`, and `--json-errors`, plus a friendly field-oriented error message on failure.
- Committed JSON Schema snapshots and a test that fails on unexpected schema drift.
- Frozen v0.2.0 fixtures and a contract guardrail that fails if a required field changes without a `contract_version` bump.
- Real-world example workflows under `examples/` (CI pytest eval, SWE-bench normalization, dashboard ingest).
- Docs: `docs/stability.md`, `docs/writing-adapters.md`, `docs/release-checklist.md`, a non-Python (ajv) validation example, README "what this is / is not", "should you use this", and package-health badges.
- `SECURITY.md` and a release workflow that publishes to PyPI via trusted publishing.
- CI now also tests on Python 3.14.

### Fixed

- Removed an invalid `harness` argument from the `normalize_terminal_bench_result` example in the adapter docs.

## 0.2.0 - 2026-07-04

- Reworked the package into a public Pydantic contract library for agent evaluation records.
- Added typed models, runtime validators, JSON Schema export, CLI subcommands, public examples, and fixture bundles.
- Removed private workflow vocabulary from the public core.

## 0.1.0 - 2026-06-27

- Initial internal package extraction.
