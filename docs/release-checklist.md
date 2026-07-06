# Release Checklist

Cutting a release is mostly automated by [`.github/workflows/release.yml`](../.github/workflows/release.yml),
which runs on a `v*` tag. This checklist covers the manual steps around it.

## Prepare

- [ ] Update `version` in `pyproject.toml`
- [ ] Update `version` (and `contract_version` if the record shape changed) in `agent_eval_contract/release_metadata.json`
- [ ] Move the `CHANGELOG.md` "Unreleased" section under the new version with a date
- [ ] If the contract shape changed, bump `contract_version`, refresh `tests/snapshots/` (schemas and `required_fields_*.json`), and add a frozen fixture set under `tests/fixtures/`

## Verify locally

- [ ] `uv run ruff check agent_eval_contract tests`
- [ ] `uv run ruff format --check agent_eval_contract tests`
- [ ] `uv run basedpyright agent_eval_contract tests`
- [ ] `uv run pytest -q` (includes schema snapshot and backward-compatibility tests)
- [ ] `uv build --out-dir /tmp/agent-eval-contract-dist`
- [ ] `uv run --with twine twine check /tmp/agent-eval-contract-dist/*`
- [ ] Install the wheel in a fresh venv and run the CLI smoke tests (`validate`, `schemas`, `normalize`, `version`)

## Release

- [ ] Commit the version bump and changelog
- [ ] Tag the release (`git tag vX.Y.Z && git push --tags`)
- [ ] Confirm the Release workflow published to PyPI via trusted publishing
- [ ] Confirm the GitHub release was created with notes
- [ ] Install `agent-eval-contract==X.Y.Z` from PyPI in a fresh venv and smoke test
