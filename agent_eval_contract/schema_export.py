from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

from .models import (
    EvalFailure,
    EvalRun,
    EvalScore,
    EvalTask,
    ExternalResult,
    FixtureBundleManifest,
    NormalizedRun,
)

type ModelType = type[BaseModel]

SCHEMA_MODELS: dict[str, ModelType] = {
    "eval_failure": EvalFailure,
    "eval_run": EvalRun,
    "eval_score": EvalScore,
    "eval_task": EvalTask,
    "external_result": ExternalResult,
    "fixture_bundle_manifest": FixtureBundleManifest,
    "normalized_run": NormalizedRun,
}


def export_json_schemas(output_dir: Path) -> list[str]:
    resolved = output_dir.expanduser().resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    exported: list[str] = []
    for schema_id, model in sorted(SCHEMA_MODELS.items()):
        path = resolved / f"{schema_id}.schema.json"
        path.write_text(
            json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        exported.append(path.name)
    return exported
