from __future__ import annotations

from pathlib import Path

import pytest

from agent_eval_contract.schema_export import SCHEMA_MODELS, export_json_schemas

SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots" / "schemas"


@pytest.mark.parametrize("schema_id", sorted(SCHEMA_MODELS))
def test_exported_schema_matches_committed_snapshot(schema_id: str, tmp_path: Path) -> None:
    export_json_schemas(tmp_path)
    generated = (tmp_path / f"{schema_id}.schema.json").read_text(encoding="utf-8")
    committed = (SNAPSHOT_DIR / f"{schema_id}.schema.json").read_text(encoding="utf-8")

    assert generated == committed, (
        f"{schema_id} schema drifted from its committed snapshot. If the change is "
        "intentional, regenerate tests/snapshots/schemas/ (agent-eval-contract schemas "
        "--output-dir tests/snapshots/schemas) and bump contract_version when the change "
        "is schema-breaking."
    )


def test_snapshot_directory_covers_every_public_model() -> None:
    committed = {path.name for path in SNAPSHOT_DIR.glob("*.schema.json")}
    expected = {f"{schema_id}.schema.json" for schema_id in SCHEMA_MODELS}

    assert committed == expected
