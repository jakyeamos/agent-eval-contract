# Adapters

Adapters translate harness-specific output into public contract records. They should keep raw harness details in `metadata.raw` and produce a complete `NormalizedRun`.

## Terminal-Bench

```python
from agent_eval_contract import normalize_terminal_bench_result

normalized = normalize_terminal_bench_result(
    {
        "passed": True,
        "tests_run": ["pytest -q"],
        "duration_ms": 120000,
        "score": 0.9,
    },
    eval_task_id="task-1",
    model="gpt-5",
)
```

The CLI equivalent:

```bash
agent-eval-contract normalize --harness terminal-bench --file examples/terminal_bench_result.json --task-id task-login-flow-001 --model gpt-5
```

## SWE-bench

Use `to_swe_bench_format()` when you need to map an `EvalTask`-shaped object into the common SWE-bench fields:

```python
from agent_eval_contract import to_swe_bench_format

swe_task = to_swe_bench_format(
    {
        "task_id": "repo__issue-123",
        "repo": "example/repo",
        "description": "Fix issue 123.",
        "start_revision": "abc1234",
    }
)
```

Normalize SWE-bench style result output:

```bash
agent-eval-contract normalize --harness swe-bench --file examples/swe_bench_result.json
```

The SWE-bench adapter reads `instance_id`, `resolved`, `model_name_or_path`, `FAIL_TO_PASS`, `PASS_TO_PASS`, `duration_seconds`, and `score` when present. Unknown JSON-compatible fields are preserved under `metadata.raw`.

## Validating in other languages

JSON Schema export is a first-class use case, not only a Python helper. Export
the schemas and validate records with any JSON Schema tool. For example, with
[`ajv-cli`](https://github.com/ajv-validator/ajv-cli):

```bash
agent-eval-contract schemas --output-dir schemas
npx ajv validate -c ajv-formats -s schemas/eval_run.schema.json -d eval_run.json
```

The `-c ajv-formats` plugin is needed so `date-time` fields (such as
`started_at`) validate.

## Writing your own adapter

See [writing-adapters.md](writing-adapters.md) for the adapter pattern, required
output fields, where to put raw data, when to add enum values vs use metadata,
and how to test an adapter.

## Extension Packages

Project-specific vocabularies should be published as separate adapters or stored in `metadata`. The public core intentionally avoids private workflow terms so records can move between independent harnesses.
