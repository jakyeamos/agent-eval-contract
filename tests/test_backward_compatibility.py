from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_eval_contract import (
    NormalizedRun,
    load_release_metadata,
    validate_eval_failure,
    validate_eval_run,
    validate_eval_score,
    validate_eval_task,
)
from agent_eval_contract.schema_export import SCHEMA_MODELS

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "v0_2_0"
SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"

# The contract version that the frozen v0.2.0 fixtures and the required-field
# snapshot describe. Bump this (and add new frozen fixtures/snapshots) only when
# contract_version changes in a coordinated, deliberate release.
EXPECTED_CONTRACT_VERSION = "0.1"


def _load_fixture(name: str) -> dict[str, Any]:
    loaded = json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_v020_eval_task_fixture_still_valid() -> None:
    task = validate_eval_task(_load_fixture("eval_task.json"))
    assert task.task_id == "task-login-flow-001"


def test_v020_eval_run_fixture_still_valid() -> None:
    run = validate_eval_run(_load_fixture("eval_run.json"))
    assert run.final_status == "success"


def test_v020_eval_score_fixture_still_valid() -> None:
    score = validate_eval_score(_load_fixture("eval_score.json"))
    assert score.overall_score == 0.91


def test_v020_eval_failure_fixture_still_valid() -> None:
    failure = validate_eval_failure(_load_fixture("eval_failure.json"))
    assert failure.priority == "medium"


def test_v020_normalized_run_fixture_still_valid() -> None:
    normalized = NormalizedRun.model_validate(_load_fixture("normalized_run.json"))
    assert normalized.harness == "terminal-bench"


def test_schema_contract_version_matches_release_metadata() -> None:
    metadata = load_release_metadata()
    assert metadata["contract_version"] == EXPECTED_CONTRACT_VERSION


def test_no_required_field_added_without_contract_bump() -> None:
    metadata = load_release_metadata()
    if metadata["contract_version"] != EXPECTED_CONTRACT_VERSION:
        # A deliberate contract bump: this guard no longer applies to the old
        # frozen required-field set. Refresh the snapshot alongside the bump.
        return

    frozen = json.loads(
        (SNAPSHOT_DIR / "required_fields_v0_1.json").read_text(encoding="utf-8")
    )
    current = {
        schema_id: sorted(model.model_json_schema().get("required", []))
        for schema_id, model in SCHEMA_MODELS.items()
    }

    assert current == frozen, (
        "Required fields changed while contract_version is still "
        f"{EXPECTED_CONTRACT_VERSION}. Adding or removing a required field is a "
        "schema-breaking change: bump contract_version and refresh "
        "tests/snapshots/required_fields_v0_1.json in the same release."
    )
