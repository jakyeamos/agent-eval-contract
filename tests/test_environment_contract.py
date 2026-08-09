from __future__ import annotations

import importlib.util
import json
from datetime import date
from pathlib import Path
from types import ModuleType


def _load_contract_module() -> ModuleType:
    path = Path(__file__).parents[1] / "scripts" / "check_environment_contract.py"
    spec = importlib.util.spec_from_file_location("environment_contract", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load environment contract checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTRACT = _load_contract_module()


def _minimal_contract(root: Path) -> None:
    for required in CONTRACT.REQUIRED_FILES:
        path = root / required
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n" if path.suffix == ".json" else "# surface\n", encoding="utf-8")
    context = root / ".agents" / "context"
    context.mkdir(parents=True, exist_ok=True)
    packets = "\n".join(f"- [{packet}]({packet})" for packet in CONTRACT.PACKETS)
    (context / "README.md").write_text(
        "last_reviewed: 2026-07-25\n\n" + packets + "\n", encoding="utf-8"
    )
    for packet in CONTRACT.PACKETS:
        (context / packet).write_text(f"# {packet}\n", encoding="utf-8")
    (root / "pyproject.toml").write_text(
        '[tool.basedpyright]\ntypeCheckingMode = "strict"\n', encoding="utf-8"
    )
    pre_cr = {
        "qualityCommands": list(CONTRACT.QUALITY_COMMANDS),
        "qualityAdapters": [
            {
                "name": "environment-contract",
                "command": "python3 scripts/check_environment_contract.py",
                "required": True,
            }
        ],
    }
    (root / ".pre-cr.json").write_text(json.dumps(pre_cr), encoding="utf-8")
    (root / ".gitignore").write_text("\n".join(CONTRACT.REQUIRED_GITIGNORE), encoding="utf-8")


def test_environment_contract_accepts_complete_private_surface(tmp_path: Path) -> None:
    _minimal_contract(tmp_path)
    result = CONTRACT.validate_contract(tmp_path, date(2026, 7, 25), paths=[])
    assert result["status"] == "pass"


def test_environment_contract_rejects_missing_packet(tmp_path: Path) -> None:
    _minimal_contract(tmp_path)
    (tmp_path / ".agents" / "context" / "examples.md").unlink()
    result = CONTRACT.validate_contract(tmp_path, date(2026, 7, 25), paths=[])
    assert result["status"] == "fail"
    assert "missing or symlinked context packet: examples.md" in result["errors"]


def test_environment_contract_rejects_stale_context(tmp_path: Path) -> None:
    _minimal_contract(tmp_path)
    index = tmp_path / ".agents" / "context" / "README.md"
    index.write_text(
        index.read_text(encoding="utf-8").replace("2026-07-25", "2026-01-01"), encoding="utf-8"
    )
    result = CONTRACT.validate_contract(tmp_path, date(2026, 7, 25), paths=[])
    assert result["status"] == "fail"
    assert "context index is stale: 2026-01-01" in result["errors"]
