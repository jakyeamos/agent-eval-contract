from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .external import normalize_external_result
from .validators import (
    validate_eval_failure,
    validate_eval_run,
    validate_eval_score,
    validate_eval_task,
)

SAMPLE_ROOT = Path(__file__).resolve().parent / "samples"
SAMPLE_FILES = {
    "eval_task": "eval_task.json",
    "eval_run": "eval_run.json",
    "eval_score": "eval_score.json",
    "eval_failure": "eval_failure.json",
    "external_result_normalization": "external_result_normalization.json",
}


def load_sample(sample_id: str, *, sample_root: Path = SAMPLE_ROOT) -> dict[str, Any]:
    filename = SAMPLE_FILES.get(sample_id)
    if filename is None:
        allowed = ", ".join(sorted(SAMPLE_FILES))
        raise ValueError(f"Unknown agent eval sample '{sample_id}'. Use one of: {allowed}.")
    loaded = json.loads((sample_root / filename).read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Agent eval sample '{sample_id}' must be a JSON object.")
    return loaded


def validate_sample(sample_id: str, sample: dict[str, Any]) -> None:
    if sample_id == "eval_task":
        validate_eval_task(sample)
        return
    if sample_id == "eval_run":
        validate_eval_run(sample)
        return
    if sample_id == "eval_score":
        validate_eval_score(sample)
        return
    if sample_id == "eval_failure":
        validate_eval_failure(sample)
        return
    if sample_id == "external_result_normalization":
        _validate_external_result_normalization(sample)
        return
    allowed = ", ".join(sorted(SAMPLE_FILES))
    raise ValueError(f"Unknown agent eval sample '{sample_id}'. Use one of: {allowed}.")


def validate_all_samples(*, sample_root: Path = SAMPLE_ROOT) -> list[str]:
    validated: list[str] = []
    for sample_id in sorted(SAMPLE_FILES):
        validate_sample(sample_id, load_sample(sample_id, sample_root=sample_root))
        validated.append(sample_id)
    return validated


def _validate_external_result_normalization(sample: dict[str, Any]) -> None:
    external_result = sample.get("external_result")
    request = sample.get("request")
    expected = sample.get("expected_normalized")
    if (
        not isinstance(external_result, dict)
        or not isinstance(request, dict)
        or not isinstance(expected, dict)
    ):
        raise ValueError("Agent eval external normalization sample fields must be objects.")
    normalized = normalize_external_result(
        external_result,
        eval_task_id=str(request["eval_task_id"]),
        harness=str(request["harness"]),
        model=str(request["model"]),
    )
    if normalized.model_dump(mode="json") != expected:
        raise ValueError("Agent eval external normalization sample expected output does not match.")
