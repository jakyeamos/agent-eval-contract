# Examples

Single-record samples for quick validation and normalization:

- `eval_run.json`, `terminal_bench_result.json`, `swe_bench_result.json`

Copy-paste workflows showing where the contract sits in a pipeline:

- [`ci_pytest_eval/`](ci_pytest_eval/) — emit a validated `EvalRun` from a CI pytest job and gate the build on valid artifacts.
- [`swe_bench_normalization/`](swe_bench_normalization/) — normalize raw SWE-bench output into a portable `NormalizedRun`.
- [`dashboard_ingest/`](dashboard_ingest/) — export JSON Schemas for a dashboard and validate records before uploading them.

Each workflow directory is runnable from its own folder after `pip install agent-eval-contract` (or `uv sync --dev` in this repo). See the module docstrings for how to run each script.
