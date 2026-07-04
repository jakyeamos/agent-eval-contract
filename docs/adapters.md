# Adapters

Adapters translate harness-specific output into public contract records. They should keep raw harness details in `metadata.raw` and produce a complete `NormalizedRun`.

## Terminal-Bench

```python
from agent_eval_contract import normalize_external_result

normalized = normalize_external_result(
    {
        "passed": True,
        "tests_run": ["pytest -q"],
        "duration_ms": 120000,
        "score": 0.9,
    },
    eval_task_id="task-1",
    harness="terminal-bench",
    model="gpt-5",
)
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

## Extension Packages

Project-specific vocabularies should be published as separate adapters or stored in `metadata`. The public core intentionally avoids private workflow terms so records can move between independent harnesses.
