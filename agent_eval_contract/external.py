from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import ExternalHarness, FinalStatus, JsonValue, NormalizedRun


def _as_mapping(value: object) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    raise TypeError("external result must be a mapping")


def _string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    return []


def _json_metadata(data: Mapping[str, Any]) -> dict[str, JsonValue]:
    return {
        str(key): value
        for key, value in data.items()
        if isinstance(key, str) and _is_json_value(value)
    }


def _is_json_value(value: object) -> bool:
    if value is None or isinstance(value, str | int | float | bool):
        return True
    if isinstance(value, list):
        return all(_is_json_value(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and _is_json_value(item) for key, item in value.items())
    return False


def _passed_status(data: Mapping[str, Any]) -> FinalStatus:
    passed_value = data.get("passed", data.get("success"))
    if passed_value is None:
        return "partial"
    return "success" if bool(passed_value) else "failed"


def _score(data: Mapping[str, Any]) -> float | None:
    value = data.get("score")
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if 0.0 <= numeric <= 1.0:
        return numeric
    if 0.0 <= numeric <= 100.0:
        return numeric / 100.0
    return None


def to_swe_bench_format(eval_task: Mapping[str, Any]) -> dict[str, Any]:
    task = _as_mapping(eval_task)
    return {
        "repo": task.get("repo"),
        "instance_id": task.get("task_id"),
        "problem_statement": task.get("description"),
        "base_commit": task.get("start_revision"),
        "FAIL_TO_PASS": task.get("fail_to_pass", []),
        "PASS_TO_PASS": task.get("pass_to_pass", []),
    }


def to_terminal_bench_format(eval_task: Mapping[str, Any]) -> dict[str, Any]:
    task = _as_mapping(eval_task)
    return {
        "task_id": task.get("task_id"),
        "command": task.get("command", "pytest"),
        "expected_exit_code": int(task.get("expected_exit_code", 0)),
        "setup_commands": task.get("setup_commands", []),
        "timeout_seconds": int(task.get("timeout_seconds", 600)),
    }


def normalize_external_result(
    external_result: Mapping[str, Any],
    *,
    eval_task_id: str | None = None,
    harness: ExternalHarness | str,
    model: str | None = None,
) -> NormalizedRun:
    data = _as_mapping(external_result)
    task_id = eval_task_id or data.get("task_id") or data.get("instance_id")
    if not task_id:
        raise ValueError("eval_task_id is required when the external result has no task_id")
    resolved_model = model or data.get("model") or "unknown"
    checks = data.get("tests_run", data.get("checks", []))
    return NormalizedRun(
        task_id=str(task_id),
        harness=str(harness),
        model=str(resolved_model),
        final_status=_passed_status(data),
        checks=_string_list(checks),
        duration_ms=data.get("duration_ms"),
        score=_score(data),
        metadata={
            "source": "external_result",
            "raw": _json_metadata(data),
        },
    )
