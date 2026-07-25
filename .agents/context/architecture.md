# Architecture and boundaries

Agent Eval Contract is a small, public, provider-neutral Python package. It
defines portable evaluation records and the validation, schema, fixture, CLI,
and normalization surfaces that consume or produce those records.

The repository is organized as:

- `agent_eval_contract/`: public Pydantic models, validators, schemas, CLI,
  fixtures, and generic external-result normalization;
- `docs/`, `README.md`, `SECURITY.md`, and `RELEASE.md`: public contract,
  security, stability, and release policy;
- `examples/`: runnable, public-safe usage patterns;
- `tests/`: contract snapshots, compatibility fixtures, behavior tests, and
  CLI tests;
- `.github/workflows/`: CI and reviewed trusted-publishing release automation.

The data flow is:

`external record -> adapter/normalization -> typed contract -> validation or JSON Schema`

The public core does not run evaluations, call model providers, orchestrate
agents, store history, host dashboards, or import AIOS. Harness-specific fields
belong in `metadata` or a separate adapter package.
