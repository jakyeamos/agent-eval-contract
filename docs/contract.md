# Contract

`agent-eval-contract` defines portable records for agent evaluation systems. The records are intentionally small enough to write by hand and strict enough to exchange between harnesses, CI jobs, notebooks, and dashboards.

## Records

- `EvalTask`: the work item being evaluated, including prompt summary, source, context profile, and acceptance criteria.
- `EvalRun`: one attempt against a task by a model, agent, harness, or workflow.
- `EvalScore`: human or automated scoring for a run.
- `EvalFailure`: structured failure analysis tied to a run.
- `ExternalResult`: a normalized input wrapper for raw external harness output.
- `NormalizedRun`: a compact, complete run summary produced from an external harness result.
- `FixtureBundleManifest`: the manifest written by the fixture bundle generator.

All public models reject unknown top-level fields. Put project-specific or harness-specific values under `metadata`.

## Validation

Validation functions return Pydantic model instances:

```python
from agent_eval_contract import validate_eval_task

task = validate_eval_task(
    {
        "task_id": "task-1",
        "title": "Fix failing checkout test",
        "description": "Repair a regression in checkout total calculation.",
    }
)
```

Invalid data raises `pydantic.ValidationError`.

## JSON Schema

Export schemas for non-Python consumers:

```bash
agent-eval-contract schemas --output-dir schemas
```

Each schema is generated from the same Pydantic model used by the Python runtime validators.
