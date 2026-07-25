from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]
PACKETS: tuple[str, ...] = (
    "architecture.md",
    "commands.md",
    "conventions.md",
    "security.md",
    "failure-modes.md",
    "examples.md",
    "done.md",
    "deployment.md",
)
QUALITY_COMMANDS: tuple[str, ...] = (
    "uv run ruff check agent_eval_contract scripts tests",
    "uv run ruff format --check agent_eval_contract scripts tests",
    "uv run basedpyright agent_eval_contract scripts tests",
    "uv run pytest -q",
    "uv run --with vulture vulture agent_eval_contract scripts tests --min-confidence 70",
    "uv build --out-dir /tmp/agent-eval-contract-dist",
    "python3 scripts/check_environment_contract.py",
)
REQUIRED_FILES: tuple[str, ...] = (
    "AGENTS.md",
    "README.md",
    "SECURITY.md",
    "pyproject.toml",
    "uv.lock",
    "scripts/pre_cr_coverage.py",
)
REQUIRED_GITIGNORE: tuple[str, ...] = (
    ".env",
    ".env.*",
    ".pre-cr/",
    ".quality-runner/",
    "dist/",
    "build/",
)
SECRET_NAME_PATTERN = re.compile(
    r"(^|/)(?:\.env(?:\..*)?|.*\.(?:pem|key|p12|pfx)|id_rsa|credentials(?:\.[^/]+)?)$",
    re.IGNORECASE,
)
SAFE_SECRET_NAMES = {".env.example", ".env.template"}
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REVIEW_PATTERN = re.compile(r"last_reviewed:\s*(\d{4}-\d{2}-\d{2})")


def _date_only(value: str | date | datetime) -> date | None:
    if isinstance(value, datetime):
        return value.astimezone(UTC).date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def _read_json(path: Path) -> dict[str, object]:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"{path} must contain an object")
    return cast(dict[str, object], parsed)


def _tracked_paths(root: Path) -> list[str] | None:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return [path for path in result.stdout.split("\0") if path]


def _check_context(root: Path, errors: list[str], as_of: date) -> int:
    context_root = root / ".agents" / "context"
    index_path = context_root / "README.md"
    if not index_path.is_file() or index_path.is_symlink():
        errors.append("context index is missing or is a symlink")
        return 0
    text = index_path.read_text(encoding="utf-8")
    reviewed = REVIEW_PATTERN.search(text)
    if reviewed is None:
        errors.append("context index is missing last_reviewed")
    else:
        reviewed_date = _date_only(reviewed.group(1))
        if reviewed_date is None:
            errors.append("context index has an invalid freshness date")
        elif reviewed_date > as_of:
            errors.append("context index freshness date is in the future")
        elif as_of - reviewed_date > timedelta(days=35):
            errors.append(f"context index is stale: {reviewed.group(1)}")
    for match in LINK_PATTERN.finditer(text):
        target_text = match.group(1).split("#", 1)[0].strip()
        if not target_text or "://" in target_text or target_text.startswith("mailto:"):
            continue
        target = (context_root / target_text).resolve()
        if not target.is_file() or not target.is_relative_to(root.resolve()):
            errors.append(f"broken context link: {target_text}")
    present = 0
    for packet in PACKETS:
        packet_path = context_root / packet
        if not packet_path.is_file() or packet_path.is_symlink():
            errors.append(f"missing or symlinked context packet: {packet}")
        else:
            present += 1
    return present


def _check_pyproject(root: Path, errors: list[str]) -> bool:
    try:
        project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        basedpyright = cast(dict[str, object], project.get("tool", {})).get("basedpyright", {})
        strict = cast(dict[str, object], basedpyright).get("typeCheckingMode") == "strict"
        if not strict:
            errors.append("pyproject.toml must keep basedpyright typeCheckingMode=strict")
        return strict
    except (OSError, tomllib.TOMLDecodeError, TypeError):
        errors.append("pyproject.toml is invalid or missing basedpyright configuration")
        return False


def _check_pre_cr(root: Path, errors: list[str]) -> bool:
    try:
        config = _read_json(root / ".pre-cr.json")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(f"invalid .pre-cr.json: {error}")
        return False
    commands = config.get("qualityCommands")
    if commands != list(QUALITY_COMMANDS):
        errors.append(".pre-cr.json qualityCommands drift")
    adapters_value = config.get("qualityAdapters", [])
    if not isinstance(adapters_value, list):
        errors.append(".pre-cr.json qualityAdapters must be a list")
        return False
    environment_adapter = False
    for item in cast(list[object], adapters_value):
        if not isinstance(item, dict):
            continue
        adapter = cast(dict[str, object], item)
        if (
            adapter.get("name") == "environment-contract"
            and adapter.get("command") == "python3 scripts/check_environment_contract.py"
            and adapter.get("required") is True
        ):
            environment_adapter = True
    if not environment_adapter:
        errors.append("required environment-contract quality adapter is missing or drifted")
    return environment_adapter


def _check_gitignore(root: Path, errors: list[str]) -> None:
    try:
        entries = {
            line.strip()
            for line in (root / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
    except OSError as error:
        errors.append(f"unable to read .gitignore: {error}")
        return
    for entry in REQUIRED_GITIGNORE:
        if entry not in entries:
            errors.append(f"missing .gitignore rule: {entry}")


def validate_contract(
    root_input: str | Path = ROOT,
    as_of_input: str | date | datetime | None = None,
    paths: list[str] | None = None,
) -> dict[str, object]:
    root = Path(root_input).expanduser().resolve()
    as_of = _date_only(as_of_input or datetime.now(UTC))
    errors: list[str] = []
    if as_of is None:
        errors.append("invalid --as-of date")
        as_of = date.min
    for required in REQUIRED_FILES:
        required_path = root / required
        if not required_path.is_file() or required_path.is_symlink():
            errors.append(f"missing required surface: {required}")
    context_packets = _check_context(root, errors, as_of)
    strict_type_checking = _check_pyproject(root, errors)
    required_pre_cr_adapter = _check_pre_cr(root, errors)
    _check_gitignore(root, errors)
    tracked = paths if paths is not None else _tracked_paths(root)
    if tracked is None:
        errors.append("git tracked-path inspection unavailable")
    else:
        for file in tracked:
            basename = Path(file).name.lower()
            if basename in SAFE_SECRET_NAMES:
                continue
            if SECRET_NAME_PATTERN.search(file):
                errors.append(f"secret-like tracked path: {file}")
    unique_errors = sorted(set(errors))
    return {
        "schema_version": "environment-contract/v1",
        "as_of": as_of.isoformat(),
        "status": "pass" if not unique_errors else "fail",
        "errors": unique_errors,
        "checks": {
            "context_packets": context_packets,
            "context_packets_required": len(PACKETS),
            "quality_commands": len(QUALITY_COMMANDS),
            "strict_type_checking": strict_type_checking,
            "tracked_secret_paths": sum(
                error.startswith("secret-like tracked path:") for error in unique_errors
            ),
            "required_pre_cr_adapter": required_pre_cr_adapter,
        },
    }


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the repository environment contract.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--as-of", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    options = _parse_args(argv if argv is not None else sys.argv[1:])
    result = validate_contract(options.root, options.as_of)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
