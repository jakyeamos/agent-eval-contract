# Stability

This package exposes two version numbers, and they mean different things.

- **Package version** (`pyproject.toml` / `pip show agent-eval-contract`) follows [SemVer](https://semver.org/) for Python API compatibility: imports, function signatures, and CLI behavior.
- **Contract version** (`contract_version` in release metadata and fixture manifests) tracks the JSON record/schema shape that records and JSON Schemas conform to.

A package release can change without changing the contract (for example, a new CLI flag), and the contract can only change through a deliberate `contract_version` bump.

## Before 1.0

While the package is pre-1.0:

- fields may be added
- enum values may be added
- required fields will not be removed without a deprecation release
- existing field meanings will not change silently
- schema-breaking changes will bump `contract_version`

## What counts as a schema-breaking change

A change bumps `contract_version` when it would cause a previously valid record to be rejected, or change what a field means:

- adding a required field
- removing a required field
- renaming a field
- narrowing an allowed type or range
- changing the meaning of an existing field

Additive, backward-compatible changes (new optional fields, new enum members, new models) do not require a `contract_version` bump but are noted in the changelog.

## How this is enforced

The test suite pins the contract:

- committed JSON Schema snapshots (`tests/snapshots/schemas/`) fail if any exported schema changes unexpectedly
- frozen backward-compatibility fixtures prove that records written against an earlier contract version still validate
- a required-field guard fails if a required field is added or removed while `contract_version` is unchanged

If a diff is intentional, the snapshots and the `contract_version` are updated in the same change.
