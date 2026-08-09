from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from .models import (
    CONTEXT_PROFILES,
    FAILURE_PRIORITIES,
    FINAL_STATUSES,
    EvalFailure,
    EvalRun,
    EvalScore,
    EvalTask,
    ExternalResult,
)

HARNESS_DIMENSION_NAMES = (
    "task_success",
    "quality_adherence",
    "runtime_reliability",
    "context_usefulness",
    "verification_strength",
    "cost_efficiency",
    "latency",
    "human_trust",
)


def _allowed_message(label: str, allowed: frozenset[str]) -> str:
    return f"Invalid {label}. Use one of: {', '.join(sorted(allowed))}."


def validate_context_profile(context_profile: str) -> None:
    if context_profile not in CONTEXT_PROFILES:
        raise ValueError(_allowed_message("context_profile", CONTEXT_PROFILES))


def validate_final_status(final_status: str) -> None:
    if final_status not in FINAL_STATUSES:
        raise ValueError(_allowed_message("final_status", FINAL_STATUSES))


def validate_priority(priority: str) -> None:
    if priority not in FAILURE_PRIORITIES:
        raise ValueError(_allowed_message("priority", FAILURE_PRIORITIES))


def validate_eval_task(data: Mapping[str, object]) -> EvalTask:
    return EvalTask.model_validate(data)


def validate_eval_run(data: Mapping[str, object]) -> EvalRun:
    return EvalRun.model_validate(data)


def validate_eval_score(data: Mapping[str, object]) -> EvalScore:
    return EvalScore.model_validate(data)


def validate_eval_failure(data: Mapping[str, object]) -> EvalFailure:
    return EvalFailure.model_validate(data)


def validate_external_result(data: Mapping[str, object]) -> ExternalResult:
    return ExternalResult.model_validate(data)


def _is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, str) for item in cast(list[object], value)
    )


def _as_string_object_mapping(value: object) -> Mapping[str, object] | None:
    if not isinstance(value, Mapping):
        return None
    candidate = cast(Mapping[object, object], value)
    if not all(isinstance(key, str) for key in candidate):
        return None
    return cast(Mapping[str, object], candidate)


def _validate_expected_gates(expected_gates: object) -> None:
    if not isinstance(expected_gates, list):
        raise ValueError("harness fixture expected_gates must be a list")
    for item in cast(list[object], expected_gates):
        item_mapping = _as_string_object_mapping(item)
        if item_mapping is None:
            raise ValueError("harness fixture expected_gates entries must be objects")
        if not item_mapping.get("id") or not item_mapping.get("expected_decision"):
            raise ValueError("harness fixture expected_gates entries need id and expected_decision")


def _validate_runs(runs: object) -> None:
    runs_mapping = _as_string_object_mapping(runs)
    if runs_mapping is None or not runs_mapping:
        raise ValueError("harness fixture runs must be a non-empty object")
    for run_id, run in runs_mapping.items():
        if not run_id:
            raise ValueError("harness fixture run ids must be non-empty strings")
        run_mapping = _as_string_object_mapping(run)
        if run_mapping is None:
            raise ValueError("harness fixture run artifacts must be objects")
        harness = _as_string_object_mapping(run_mapping.get("harness"))
        if harness is None or not harness.get("name"):
            raise ValueError("harness fixture run artifacts need harness.name")


def validate_harness_fixture_components(
    *,
    task_markdown: str,
    expected_context_packets: list[str],
    expected_gates: list[dict[str, str]],
    expected_success_criteria: list[str],
    golden_outcome_markdown: str,
    scoring: object,
    runs: object,
) -> None:
    if not task_markdown.strip():
        raise ValueError("harness fixture task_markdown must not be empty")
    if not golden_outcome_markdown.strip():
        raise ValueError("harness fixture golden_outcome_markdown must not be empty")
    if not _is_string_list(expected_context_packets):
        raise ValueError("harness fixture expected_context_packets must be a string list")
    if not _is_string_list(expected_success_criteria):
        raise ValueError("harness fixture expected_success_criteria must be a string list")
    if _as_string_object_mapping(scoring) is None:
        raise ValueError("harness fixture scoring must be an object")
    _validate_expected_gates(expected_gates)
    _validate_runs(runs)
