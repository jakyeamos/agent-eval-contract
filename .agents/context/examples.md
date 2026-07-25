# Canonical implementation examples

- `examples/ci_pytest_eval/` is the reference for emitting and validating a
  CI-produced evaluation record before downstream use.
- `examples/swe_bench_normalization/` is the reference for a plain-data
  external-result adapter and normalized output.
- `examples/dashboard_ingest/` is the reference for validating records and
  exporting schemas before an external consumer receives them.
- `agent_eval_contract/validators.py` and `agent_eval_contract/external.py`
  show the boundary between typed validation and provider-neutral transforms.
- `tests/test_backward_compatibility.py` and `tests/test_schema_snapshots.py`
  are the canonical examples for preserving public contract stability.

Every example must remain runnable with the documented commands and must use
only synthetic or public-safe data.
