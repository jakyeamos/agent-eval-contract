from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

from agent_eval_contract.release import load_release_metadata

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PATH = ROOT / "pyproject.toml"
RELEASE_METADATA_PATH = ROOT / "agent_eval_contract" / "release_metadata.json"


def load_project_version(path: Path = PROJECT_PATH) -> str:
    project = tomllib.loads(path.read_text(encoding="utf-8"))
    version = project.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("pyproject.toml is missing project.version")
    return version


def check_release_metadata(tag: str | None = None) -> dict[str, Any]:
    project_version = load_project_version()
    metadata = load_release_metadata(RELEASE_METADATA_PATH)
    metadata_version = metadata["version"]
    if metadata_version != project_version:
        raise ValueError(
            f"pyproject.toml version {project_version} does not match release metadata version "
            f"{metadata_version}"
        )
    if tag is not None and tag.removeprefix("v") != project_version:
        raise ValueError(f"release tag {tag} does not match project version {project_version}")
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check package release metadata consistency.")
    parser.add_argument("--tag", help="Release tag to compare with project.version.")
    args = parser.parse_args(argv)
    try:
        metadata = check_release_metadata(args.tag)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"release metadata check failed: {error}", file=sys.stderr)
        return 1
    print(
        "release metadata ok: "
        f"package=agent-eval-contract version={metadata['version']} status={metadata['status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
