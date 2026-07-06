# Writing Adapters

An adapter turns one harness's raw output into a public contract record. The
long-term value of this package is as the stable core beneath adapter packages,
so adapters should be small, well-tested, and keep private vocabulary out of the
public core.

## The pattern

An adapter is a function from raw harness output to a `NormalizedRun`:

```python
from agent_eval_contract import NormalizedRun


def normalize_my_harness_result(raw: dict) -> NormalizedRun:
    return NormalizedRun(
        task_id=str(raw["task_id"]),
        harness="my-harness",
        model=str(raw.get("model", "unknown")),
        final_status="success" if raw.get("passed") else "failed",
        checks=[str(check) for check in raw.get("checks", [])],
        duration_ms=raw.get("duration_ms"),
        score=raw.get("score"),
        metadata={"source": "my-harness", "raw": raw},
    )
```

Constructing the model validates it, so a malformed record raises
`pydantic.ValidationError` at the boundary instead of downstream.

## Required output fields

A `NormalizedRun` must set `task_id`, `harness`, `model`, and `final_status`.
`checks`, `duration_ms`, and `score` are optional but recommended when the
harness provides them. `mode` defaults to `benchmark` and `context_profile` to
`clean_room`; override them only when the harness clearly implies otherwise.

## Where to put raw data

Preserve the original harness payload under `metadata.raw` and identify the
adapter under `metadata.source`. Nothing from the harness should be dropped —
downstream tools can always fall back to the raw record.

Only JSON-compatible values (`str`, `int`, `float`, `bool`, `None`, and lists or
string-keyed dicts of those) belong in metadata. Convert timestamps and enums to
strings and drop non-serializable objects before storing them.

## Enum values vs metadata

Add a value to a public enum (for example, a new `final_status`) only when it is
harness-independent and belongs in the shared contract; that is a contract
change and bumps `contract_version` (see [stability.md](stability.md)). For
anything harness-specific or project-specific, use `metadata` instead of
widening the core vocabulary.

## Testing an adapter

Cover at least:

- a passing result maps to `final_status="success"`
- a failing result maps to `final_status="failed"`
- `metadata.raw` round-trips the input
- a missing `task_id` raises rather than producing an incomplete record

```python
def test_my_harness_adapter_marks_success() -> None:
    normalized = normalize_my_harness_result(
        {"task_id": "t-1", "passed": True, "checks": ["pytest -q"]}
    )
    assert normalized.final_status == "success"
    assert normalized.metadata["source"] == "my-harness"
```

## Publishing

Project-specific vocabularies should be published as separate adapter packages
that depend on `agent-eval-contract`, not merged into the public core. The core
stays generic so records can move between independent harnesses.
