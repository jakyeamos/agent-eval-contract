from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .schemas import CONTEXT_PROFILES, FAILURE_PRIORITIES, FINAL_STATUSES

HARNESS_DIMENSION_NAMES = (
    "context_precision",
    "context_recall",
    "gate_accuracy",
    "success_criteria_recall",
    "trace_completeness",
    "false_completion_caught",
    "recovery_evidence_present",
    "writeback_usefulness_present",
)


def _allowed_message(label: str, allowed: frozenset[str]) -> str:
    return f"Invalid {label}. Use one of: {', '.join(sorted(allowed))}."


def validate_context_profile(context_profile: str) -> None:
    if context_profile not in CONTEXT_PROFILES:
        raise ValueError(
            _allowed_message("context_profile", CONTEXT_PROFILES)
            + " Choose the profile that matches the context actually available to the run."
        )


def validate_final_status(final_status: str) -> None:
    if final_status not in FINAL_STATUSES:
        raise ValueError(_allowed_message("final_status", FINAL_STATUSES))


def validate_priority(priority: str) -> None:
    if priority not in FAILURE_PRIORITIES:
        raise ValueError(_allowed_message("priority", FAILURE_PRIORITIES))


def _is_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _validate_expected_gates(expected_gates: Any) -> None:
    if not isinstance(expected_gates, list):
        raise ValueError("harness fixture expected_gates must be a list")
    for item in expected_gates:
        if not isinstance(item, Mapping):
            raise ValueError("harness fixture expected_gates entries must be objects")
        if not item.get("id") or not item.get("expected_decision"):
            raise ValueError("harness fixture expected_gates entries need id and expected_decision")


def _validate_runs(runs: Any) -> None:
    if not isinstance(runs, Mapping) or not runs:
        raise ValueError("harness fixture runs must be a non-empty object")
    for run_id, run in runs.items():
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("harness fixture run ids must be non-empty strings")
        if not isinstance(run, Mapping):
            raise ValueError("harness fixture run artifacts must be objects")
        harness = run.get("harness")
        if not isinstance(harness, Mapping) or not harness.get("name"):
            raise ValueError("harness fixture run artifacts need harness.name")


def validate_harness_fixture_components(
    *,
    task_markdown: str,
    expected_context_packets: list[str],
    expected_gates: list[dict[str, str]],
    expected_success_criteria: list[str],
    golden_outcome_markdown: str,
    scoring: Mapping[str, Any],
    runs: Mapping[str, Mapping[str, Any]],
) -> None:
    if not task_markdown.strip():
        raise ValueError("harness fixture task_markdown must not be empty")
    if not golden_outcome_markdown.strip():
        raise ValueError("harness fixture golden_outcome_markdown must not be empty")
    if not _is_string_list(expected_context_packets):
        raise ValueError("harness fixture expected_context_packets must be a string list")
    if not _is_string_list(expected_success_criteria):
        raise ValueError("harness fixture expected_success_criteria must be a string list")
    if not isinstance(scoring, Mapping):
        raise ValueError("harness fixture scoring must be an object")
    _validate_expected_gates(expected_gates)
    _validate_runs(runs)
