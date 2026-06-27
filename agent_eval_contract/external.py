from __future__ import annotations

from typing import Any


def to_swe_bench_format(eval_task_dict: dict[str, Any]) -> dict[str, Any]:
    return {
        "repo": eval_task_dict.get("repo_id"),
        "instance_id": eval_task_dict.get("id") or eval_task_dict.get("task_id"),
        "problem_statement": eval_task_dict.get("prompt_summary"),
        "base_commit": eval_task_dict.get("start_sha"),
        "FAIL_TO_PASS": eval_task_dict.get("fail_to_pass", []),
        "PASS_TO_PASS": eval_task_dict.get("pass_to_pass", []),
    }


def to_terminal_bench_format(eval_task_dict: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": eval_task_dict.get("id") or eval_task_dict.get("task_id"),
        "command": eval_task_dict.get("command", "pytest"),
        "expected_exit_code": int(eval_task_dict.get("expected_exit_code", 0)),
        "setup_commands": eval_task_dict.get("setup_commands", []),
        "timeout_seconds": int(eval_task_dict.get("timeout_seconds", 600)),
    }


def normalize_external_result(
    external_result: dict[str, Any],
    *,
    eval_task_id: str,
    harness: str,
    model: str,
) -> dict[str, Any]:
    passed = bool(external_result.get("passed", external_result.get("success", False)))
    return {
        "task_id": eval_task_id,
        "condition": "external_harness",
        "mode": "external",
        "harness": harness,
        "model": model,
        "context_profile": "external_clean_room",
        "final_status": "success" if passed else "failed",
        "tests_run": external_result.get("tests_run", []),
        "duration_ms": external_result.get("duration_ms"),
    }
