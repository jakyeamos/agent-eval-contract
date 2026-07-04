from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest
from pydantic import ValidationError

from agent_eval_contract import (
    EvalRun,
    FixtureBundleManifest,
    NormalizedRun,
    export_json_schemas,
    load_release_metadata,
    load_sample,
    normalize_external_result,
    normalize_swe_bench_result,
    normalize_terminal_bench_result,
    render_eval_template,
    run_clean_room_contract_check,
    supported_template_ids,
    validate_all_samples,
    validate_context_profile,
    validate_eval_failure,
    validate_eval_run,
    validate_eval_score,
    validate_eval_task,
    validate_eval_template,
    validate_external_result,
    validate_priority,
    validate_release_metadata,
)
from agent_eval_contract.fixture_runner import write_contract_fixture_bundle
from agent_eval_contract.models import JsonValue

ROOT = Path(__file__).resolve().parents[1]


def test_eval_run_model_rejects_unknown_core_fields() -> None:
    with pytest.raises(ValidationError) as exc_info:
        EvalRun.model_validate(
            {
                "run_id": "run-1",
                "task_id": "task-1",
                "harness": "pytest",
                "model": "gpt-5",
                "final_status": "success",
                "private_field": "nope",
            }
        )

    assert exc_info.value.errors()[0]["type"] == "extra_forbidden"


def test_metadata_accepts_extension_data() -> None:
    run = validate_eval_run(
        {
            "run_id": "run-1",
            "task_id": "task-1",
            "harness": "pytest",
            "model": "gpt-5",
            "final_status": "success",
            "metadata": {"workflow": {"name": "local-agent", "attempt": 2}},
        }
    )

    assert run.metadata["workflow"] == {"name": "local-agent", "attempt": 2}


def test_public_validators_return_typed_models() -> None:
    assert validate_eval_task(load_sample("eval_task")).task_id == "task-login-flow-001"
    assert validate_eval_run(load_sample("eval_run")).final_status == "success"
    assert validate_eval_score(load_sample("eval_score")).overall_score == 0.91
    assert validate_eval_failure(load_sample("eval_failure")).priority == "medium"
    assert (
        validate_external_result(
            {
                "harness": "terminal-bench",
                "passed": True,
                "tests_run": ["pytest -q"],
            }
        ).harness
        == "terminal-bench"
    )


def test_invalid_scores_expose_pydantic_errors() -> None:
    with pytest.raises(ValidationError) as exc_info:
        validate_eval_score(
            {
                "run_id": "run-1",
                "overall_score": 1.5,
            }
        )

    assert exc_info.value.errors()[0]["loc"] == ("overall_score",)


def test_contract_vocabulary_validates() -> None:
    validate_context_profile("repo_only")
    validate_priority("critical")

    with pytest.raises(ValueError, match="Invalid context_profile"):
        validate_context_profile("private_magic")

    with pytest.raises(ValueError, match="Invalid priority"):
        validate_priority("urgent")


def test_external_result_normalization_returns_complete_normalized_run() -> None:
    normalized = normalize_external_result(
        {"success": False, "tests_run": ["pytest"], "duration_ms": 10, "score": 75},
        eval_task_id="task-1",
        harness="terminal-bench",
        model="gpt-5",
    )

    assert isinstance(normalized, NormalizedRun)
    assert normalized.context_profile == "clean_room"
    assert normalized.final_status == "failed"
    assert normalized.checks == ["pytest"]
    assert normalized.score == 0.75
    raw = cast(dict[str, JsonValue], normalized.metadata["raw"])
    assert raw["success"] is False


def test_terminal_bench_adapter_handles_command_and_seconds() -> None:
    normalized = normalize_terminal_bench_result(
        {
            "task_id": "terminal-task-1",
            "status": "passed",
            "command": "pytest -q",
            "duration_seconds": 1.25,
        },
        model="gpt-5",
    )

    assert normalized.task_id == "terminal-task-1"
    assert normalized.harness == "terminal-bench"
    assert normalized.final_status == "success"
    assert normalized.checks == ["pytest -q"]
    assert normalized.duration_ms == 1250
    assert normalized.metadata["source"] == "terminal-bench"


def test_swe_bench_adapter_reads_instance_and_test_lists() -> None:
    normalized = normalize_swe_bench_result(load_json_example("swe_bench_result.json"))

    assert normalized.task_id == "example__repo-123"
    assert normalized.harness == "swe-bench"
    assert normalized.model == "gpt-5"
    assert normalized.final_status == "success"
    assert normalized.duration_ms == 92400
    assert normalized.score == 1.0
    assert normalized.checks == [
        "tests/test_checkout.py::test_preserves_discount",
        "tests/test_checkout.py::test_calculates_total",
    ]


def test_eval_template_renderer_produces_valid_public_templates() -> None:
    for template_id in supported_template_ids():
        rendered = render_eval_template(template_id)
        if template_id in {"major-task-eval", "shadow-branch-comparison"}:
            assert "Harness Condition" in rendered
        validate_eval_template(template_id, rendered)


def test_bundled_samples_and_release_metadata_validate() -> None:
    assert validate_all_samples() == [
        "eval_failure",
        "eval_run",
        "eval_score",
        "eval_task",
        "external_result_normalization",
    ]

    metadata = load_release_metadata()
    validate_release_metadata(metadata)

    assert metadata["package_name"] == "agent-eval-contract"
    assert "Pydantic evaluation record models" in metadata["public_surfaces"]
    assert metadata["release_blockers"] == []


def test_schema_export_writes_public_model_schemas(tmp_path: Path) -> None:
    exported = export_json_schemas(tmp_path)

    assert "eval_run.schema.json" in exported
    assert "normalized_run.schema.json" in exported
    schema = json.loads((tmp_path / "eval_run.schema.json").read_text(encoding="utf-8"))
    assert schema["title"] == "EvalRun"
    assert schema["additionalProperties"] is False


def test_clean_room_runner_uses_generated_templates(tmp_path: Path) -> None:
    template_root = tmp_path / "templates"
    template_root.mkdir()
    for template_id in supported_template_ids():
        (template_root / f"{template_id}.md").write_text(
            render_eval_template(template_id),
            encoding="utf-8",
        )

    result = run_clean_room_contract_check(template_root=template_root)

    assert result["ok"] is True
    assert result["template_count"] == 5
    assert result["sample_count"] == 5


def test_fixture_bundle_writer_produces_public_artifacts(tmp_path: Path) -> None:
    result = write_contract_fixture_bundle(tmp_path)

    manifest = FixtureBundleManifest.model_validate(result)
    assert manifest.package == "agent-eval-contract"
    assert (tmp_path / "manifest.json").exists()
    assert (tmp_path / "samples" / "eval_task.json").exists()
    assert (tmp_path / "templates" / "major-task-eval.md").exists()
    assert (tmp_path / "schemas" / "eval_run.schema.json").exists()
    assert result["metadata"]["public_surfaces"]


def test_main_cli_subcommands_work(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    fixture_dir = tmp_path / "bundle"
    schema_dir = tmp_path / "schemas"

    fixtures = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_eval_contract.cli",
            "fixtures",
            "--output-dir",
            str(fixture_dir),
        ],
        cwd=tmp_path,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(fixtures.stdout)["package"] == "agent-eval-contract"

    schemas = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_eval_contract.cli",
            "schemas",
            "--output-dir",
            str(schema_dir),
        ],
        cwd=tmp_path,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "eval_run.schema.json" in json.loads(schemas.stdout)["schemas"]

    validated = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_eval_contract.cli",
            "validate",
            "--kind",
            "run",
            "--file",
            str(ROOT / "examples" / "eval_run.json"),
        ],
        cwd=tmp_path,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(validated.stdout)["run_id"] == "run-login-flow-001"

    normalized = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_eval_contract.cli",
            "normalize",
            "--harness",
            "terminal-bench",
            "--file",
            str(ROOT / "examples" / "terminal_bench_result.json"),
            "--task-id",
            "task-login-flow-001",
            "--model",
            "gpt-5",
        ],
        cwd=tmp_path,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(normalized.stdout)["final_status"] == "success"

    swe_normalized = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_eval_contract.cli",
            "normalize",
            "--harness",
            "swe-bench",
            "--file",
            str(ROOT / "examples" / "swe_bench_result.json"),
        ],
        cwd=tmp_path,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(swe_normalized.stdout)["task_id"] == "example__repo-123"


def test_deprecated_fixture_runner_cli_still_works(tmp_path: Path) -> None:
    output_dir = tmp_path / "bundle"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "agent_eval_contract.fixture_runner",
            "--output-dir",
            str(output_dir),
        ],
        cwd=tmp_path,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    manifest = json.loads(completed.stdout)
    assert manifest["samples"] == [
        "eval_failure",
        "eval_run",
        "eval_score",
        "eval_task",
        "external_result_normalization",
    ]
    assert (output_dir / "schemas" / "normalized_run.schema.json").exists()


def load_json_example(name: str) -> dict[str, JsonValue]:
    loaded = json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded
