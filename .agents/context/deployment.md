# Packaging, deployment, and rollback

This repository publishes a Python package; it does not deploy a service. The
release workflow builds the wheel and sdist, runs `twine check`, performs a
fresh-environment CLI smoke test, and uses PyPI trusted publishing from a
reviewed `v*` tag. Do not publish or tag as part of ordinary tests.

Before a release, update the package version, release metadata, changelog,
contract version, snapshots, and frozen fixtures as applicable. Run the full
quality ladder and inspect the built artifact in a fresh virtual environment.

Rollback is a normal `git revert` before publication or selection of the prior
published package version after publication. Never rewrite release history,
delete compatibility fixtures, or treat a failed release check as a reason to
lower the gate.
