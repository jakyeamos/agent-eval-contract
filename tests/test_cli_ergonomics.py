from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_eval_contract.cli import main

ROOT = Path(__file__).resolve().parents[1]
EVAL_RUN = ROOT / "examples" / "eval_run.json"


def test_version_reports_package_and_contract(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["version"]) == 0
    out = capsys.readouterr().out
    assert out.splitlines()[0].startswith("package: ")
    assert any(line.startswith("contract: ") for line in out.splitlines())


def test_inspect_infers_kind(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["inspect", "--file", str(EVAL_RUN)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["matches"] == ["run"]
    assert result["record"]["run_id"] == "run-login-flow-001"


def test_inspect_reports_no_match_with_nonzero_exit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    unknown = tmp_path / "unknown.json"
    unknown.write_text(json.dumps({"totally": "unrelated"}), encoding="utf-8")

    assert main(["inspect", "--file", str(unknown)]) == 1
    assert json.loads(capsys.readouterr().out)["matches"] == []


def test_validate_quiet_suppresses_success_output(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", "--kind", "run", "--file", str(EVAL_RUN), "--quiet"]) == 0
    assert capsys.readouterr().out == ""


def test_validate_pretty_indents_output(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", "--kind", "run", "--file", str(EVAL_RUN), "--pretty"]) == 0
    assert "\n  " in capsys.readouterr().out


def test_validate_friendly_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    bad = tmp_path / "bad_run.json"
    bad.write_text(
        json.dumps(
            {
                "run_id": "run-1",
                "task_id": "task-1",
                "harness": "pytest",
                "model": "gpt-5",
                "final_status": "pass",
            }
        ),
        encoding="utf-8",
    )

    assert main(["validate", "--kind", "run", "--file", str(bad)]) == 1
    err = capsys.readouterr().err
    assert "Invalid eval_run record" in err
    assert "Field: final_status" in err
    assert 'Value: "pass"' in err


def test_validate_json_errors_flag(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    bad = tmp_path / "bad_run.json"
    bad.write_text(json.dumps({"run_id": "run-1"}), encoding="utf-8")

    assert main(["validate", "--kind", "run", "--file", str(bad), "--json-errors"]) == 1
    errors = json.loads(capsys.readouterr().err)
    assert isinstance(errors, list)
    assert all("loc" in item for item in errors)
