from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .external import normalize_external_result
from .schemas import (
    AUTOMATION_STATES,
    EVAL_RUN_MODES,
    EVAL_TASK_SOURCES,
    SCORE_FIELDS,
    SHADOW_RECOMMENDATIONS,
)
from .validators import validate_context_profile, validate_final_status, validate_priority

SAMPLE_ROOT = Path(__file__).resolve().parent / "samples"
SAMPLE_FILES = {
    "eval_task": "eval_task.json",
    "eval_run": "eval_run.json",
    "eval_score": "eval_score.json",
    "eval_failure": "eval_failure.json",
    "shadow_candidate": "shadow_candidate.json",
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
    validators = {
        "eval_task": _validate_eval_task,
        "eval_run": _validate_eval_run,
        "eval_score": _validate_eval_score,
        "eval_failure": _validate_eval_failure,
        "shadow_candidate": _validate_shadow_candidate,
        "external_result_normalization": _validate_external_result_normalization,
    }
    validator = validators.get(sample_id)
    if validator is None:
        allowed = ", ".join(sorted(validators))
        raise ValueError(f"Unknown agent eval sample '{sample_id}'. Use one of: {allowed}.")
    validator(sample)


def validate_all_samples(*, sample_root: Path = SAMPLE_ROOT) -> list[str]:
    validated: list[str] = []
    for sample_id in sorted(SAMPLE_FILES):
        validate_sample(sample_id, load_sample(sample_id, sample_root=sample_root))
        validated.append(sample_id)
    return validated


def _require_keys(sample_id: str, sample: dict[str, Any], keys: tuple[str, ...]) -> None:
    missing = [key for key in keys if key not in sample]
    if missing:
        raise ValueError(f"Agent eval sample '{sample_id}' is missing keys: {', '.join(missing)}")


def _require_string_list(sample_id: str, sample: dict[str, Any], key: str) -> None:
    value = sample.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Agent eval sample '{sample_id}' field '{key}' must be a string list.")


def _require_number(sample_id: str, sample: dict[str, Any], key: str) -> None:
    if not isinstance(sample.get(key), int | float):
        raise ValueError(f"Agent eval sample '{sample_id}' field '{key}' must be numeric.")


def _validate_eval_task(sample: dict[str, Any]) -> None:
    sample_id = "eval_task"
    _require_keys(
        sample_id,
        sample,
        (
            "task_id",
            "repo_id",
            "source",
            "start_sha",
            "context_profile",
            "task_type",
            "prompt_summary",
            "acceptance_criteria",
            "success_criteria_files",
            "created_at",
        ),
    )
    if sample["source"] not in EVAL_TASK_SOURCES:
        raise ValueError("Agent eval sample 'eval_task' has invalid source.")
    validate_context_profile(str(sample["context_profile"]))
    _require_string_list(sample_id, sample, "acceptance_criteria")
    _require_string_list(sample_id, sample, "success_criteria_files")


def _validate_eval_run(sample: dict[str, Any]) -> None:
    sample_id = "eval_run"
    _require_keys(
        sample_id,
        sample,
        (
            "run_id",
            "task_id",
            "condition",
            "mode",
            "harness",
            "model",
            "context_profile",
            "tests_run",
            "final_status",
        ),
    )
    if sample["mode"] not in EVAL_RUN_MODES:
        raise ValueError("Agent eval sample 'eval_run' has invalid mode.")
    validate_context_profile(str(sample["context_profile"]))
    validate_final_status(str(sample["final_status"]))
    _require_string_list(sample_id, sample, "tests_run")


def _validate_eval_score(sample: dict[str, Any]) -> None:
    sample_id = "eval_score"
    _require_keys(sample_id, sample, ("run_id", "overall_score", "reviewer_notes"))
    _require_number(sample_id, sample, "overall_score")
    for score_field in SCORE_FIELDS:
        if score_field in sample and sample[score_field] is not None:
            _require_number(sample_id, sample, score_field)


def _validate_eval_failure(sample: dict[str, Any]) -> None:
    sample_id = "eval_failure"
    _require_keys(
        sample_id,
        sample,
        (
            "failure_id",
            "run_id",
            "failure_types",
            "summary",
            "suspected_cause",
            "affected_components",
            "recommended_fixes",
            "priority",
            "regression_task_created",
            "backfill_item_created",
            "standards_update_needed",
        ),
    )
    validate_priority(str(sample["priority"]))
    _require_string_list(sample_id, sample, "failure_types")
    _require_string_list(sample_id, sample, "affected_components")
    _require_string_list(sample_id, sample, "recommended_fixes")


def _validate_shadow_candidate(sample: dict[str, Any]) -> None:
    sample_id = "shadow_candidate"
    _require_keys(
        sample_id,
        sample,
        (
            "candidate_id",
            "task_id",
            "score",
            "recommendation",
            "reasons",
            "blockers",
            "automation_state",
        ),
    )
    _require_number(sample_id, sample, "score")
    if sample["recommendation"] not in SHADOW_RECOMMENDATIONS:
        raise ValueError("Agent eval sample 'shadow_candidate' has invalid recommendation.")
    if sample["automation_state"] not in AUTOMATION_STATES:
        raise ValueError("Agent eval sample 'shadow_candidate' has invalid automation_state.")
    _require_string_list(sample_id, sample, "reasons")
    _require_string_list(sample_id, sample, "blockers")


def _validate_external_result_normalization(sample: dict[str, Any]) -> None:
    sample_id = "external_result_normalization"
    _require_keys(sample_id, sample, ("external_result", "request", "expected_normalized"))
    external_result = sample["external_result"]
    request = sample["request"]
    expected = sample["expected_normalized"]
    if (
        not isinstance(external_result, dict)
        or not isinstance(request, dict)
        or not isinstance(expected, dict)
    ):
        raise ValueError("Agent eval external normalization sample fields must be objects.")
    _require_keys(sample_id, request, ("eval_task_id", "harness", "model"))
    normalized = normalize_external_result(
        external_result,
        eval_task_id=str(request["eval_task_id"]),
        harness=str(request["harness"]),
        model=str(request["model"]),
    )
    if normalized != expected:
        raise ValueError("Agent eval external normalization sample expected output does not match.")
    _validate_eval_run(
        {
            "run_id": "external-sample-run",
            "task_id": expected.get("task_id"),
            "condition": expected.get("condition"),
            "mode": expected.get("mode"),
            "harness": expected.get("harness"),
            "model": expected.get("model"),
            "context_profile": expected.get("context_profile"),
            "tests_run": expected.get("tests_run", []),
            "final_status": expected.get("final_status"),
        }
    )
