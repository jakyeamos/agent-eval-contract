# ruff: noqa: E402

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_eval_contract import (
    CONTEXT_PROFILES,
    HARNESS_DIMENSION_NAMES,
    load_release_metadata,
    load_sample,
    normalize_external_result,
    render_eval_template,
    run_clean_room_contract_check,
    supported_template_ids,
    validate_all_samples,
    validate_context_profile,
    validate_eval_template,
    validate_harness_fixture_components,
    validate_priority,
    validate_release_metadata,
)
from agent_eval_contract.fixture_runner import write_contract_fixture_bundle


def test_import_does_not_import_aios_services() -> None:
    for module_name in list(sys.modules):
        if module_name == "agent_eval_contract" or module_name.startswith("agent_eval_contract."):
            del sys.modules[module_name]
        if module_name == "services" or module_name.startswith("services."):
            del sys.modules[module_name]

    imported = importlib.import_module("agent_eval_contract")

    assert "external_clean_room" in imported.CONTEXT_PROFILES
    assert "services" not in sys.modules
    assert not any(module_name.startswith("services.") for module_name in sys.modules)


def test_contract_vocabulary_validates() -> None:
    validate_context_profile("peer_portable_context_packet")
    validate_priority("critical")

    with pytest.raises(ValueError, match="Invalid context_profile"):
        validate_context_profile("private_magic")

    with pytest.raises(ValueError, match="Invalid priority"):
        validate_priority("urgent")


def test_harness_fixture_contract_rejects_malformed_fixture() -> None:
    with pytest.raises(ValueError, match="expected_gates entries need id and expected_decision"):
        validate_harness_fixture_components(
            task_markdown="# Task",
            expected_context_packets=["global.testing"],
            expected_gates=[{"id": "approval"}],
            expected_success_criteria=["test-quality"],
            golden_outcome_markdown="# Outcome",
            scoring={},
            runs={"aios_shadow": {"harness": {"name": "AIOS"}}},
        )


def test_external_result_normalization_matches_contract() -> None:
    normalized = normalize_external_result(
        {"success": False, "tests_run": ["pytest"], "duration_ms": 10},
        eval_task_id="task-1",
        harness="terminal-bench",
        model="gpt-5",
    )

    assert normalized["context_profile"] == "external_clean_room"
    assert normalized["final_status"] == "failed"
    assert normalized["tests_run"] == ["pytest"]
    assert set(CONTEXT_PROFILES) >= {"external_clean_room", "peer_repo_only"}
    assert "false_completion_caught" in HARNESS_DIMENSION_NAMES


def test_eval_template_renderer_produces_valid_portable_templates() -> None:
    for template_id in supported_template_ids():
        validate_eval_template(template_id, render_eval_template(template_id))


def test_bundled_samples_and_release_metadata_validate() -> None:
    assert "eval_task" in validate_all_samples()
    assert load_sample("eval_run")["context_profile"] == "peer_repo_only"

    metadata = load_release_metadata()
    validate_release_metadata(metadata)

    assert metadata["package_name"] == "agent-eval-contract"
    assert "clean-room fixture production" in metadata["portable_surfaces"]
    assert "SQLite eval storage" in metadata["aios_owned_surfaces"]


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
    assert result["sample_count"] == 6


def test_fixture_bundle_writer_produces_non_aios_artifacts(tmp_path: Path) -> None:
    result = write_contract_fixture_bundle(tmp_path)

    assert result["clean_room_check"]["ok"] is True
    assert (tmp_path / "manifest.json").exists()
    assert (tmp_path / "samples" / "eval_task.json").exists()
    assert (tmp_path / "templates" / "major-task-eval.md").exists()
    assert json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))["package"] == (
        "agent-eval-contract"
    )


def test_fixture_runner_cli_works_outside_repo_cwd(tmp_path: Path) -> None:
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
    assert manifest["clean_room_check"]["ok"] is True
    assert manifest["clean_room_check"]["sample_count"] == 6
    assert (output_dir / "manifest.json").exists()
