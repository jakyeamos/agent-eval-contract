# Release Checklist

Cutting a release is mostly automated by [`.github/workflows/release.yml`](../.github/workflows/release.yml),
which runs on a `v*` tag. This checklist covers the manual steps around it.

## Current candidate state

The repository's current candidate is `0.3.0`, while PyPI's latest published
version is `0.2.0` (verified 2026-07-17). Keep release metadata marked as
`public_package_candidate` with explicit blockers until the tagged workflow and
registry smoke test have completed. Do not publish the existing `v0.3.0` tag
from a post-tag cleanup commit without first deciding which final tag should
contain the merged work.

## Prepare

- [ ] Update `version` in `pyproject.toml`
- [ ] Update `version` (and `contract_version` if the record shape changed) in `agent_eval_contract/release_metadata.json`
- [ ] Move the `CHANGELOG.md` "Unreleased" section under the new version with a date
- [ ] If the contract shape changed, bump `contract_version`, refresh `tests/snapshots/` (schemas and `required_fields_*.json`), and add a frozen fixture set under `tests/fixtures/`

## Verify locally

- [ ] `uv run ruff check agent_eval_contract tests scripts`
- [ ] `uv run ruff format --check agent_eval_contract tests scripts`
- [ ] `uv run basedpyright agent_eval_contract tests scripts`
- [ ] `uv run pytest -q` (includes schema snapshot and backward-compatibility tests)
- [ ] `uv run python scripts/check_release_metadata.py`
- [ ] `uv run python scripts/check_release_metadata.py --tag vX.Y.Z` (after the final tag points at the release commit)
- [ ] `uv build --out-dir /tmp/agent-eval-contract-dist`
- [ ] `uv run --with twine twine check /tmp/agent-eval-contract-dist/*`
- [ ] Install the wheel in a fresh venv and run the CLI smoke tests (`--help`, `--version`, `version`, `validate`, `inspect`, `normalize`, `schemas`, `fixtures`, and `agent-eval-contract-fixtures`)

## Release

- [ ] Commit the version bump and changelog
- [ ] Merge the final release commit before tagging it
- [ ] Trigger the tagged workflow (`gh workflow run release.yml --ref vX.Y.Z`) or push the final `vX.Y.Z` tag
- [ ] Confirm the Release workflow published to PyPI via trusted publishing
- [ ] Confirm the GitHub release was created with notes
- [ ] Install `agent-eval-contract==X.Y.Z` from PyPI in a fresh venv and smoke test
- [ ] Update release metadata to `published` and clear `release_blockers` in the follow-up truth update
