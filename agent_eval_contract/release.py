from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RELEASE_METADATA_PATH = Path(__file__).resolve().parent / "release_metadata.json"
REQUIRED_RELEASE_METADATA_KEYS = (
    "package_name",
    "version",
    "contract_version",
    "status",
    "python_requires",
    "public_promise",
    "public_surfaces",
    "out_of_scope",
    "public_modules",
    "release_blockers",
)


def load_release_metadata(path: Path = RELEASE_METADATA_PATH) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError("Agent eval release metadata must be a JSON object.")
    validate_release_metadata(loaded)
    return loaded


def validate_release_metadata(metadata: dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_RELEASE_METADATA_KEYS if key not in metadata]
    if missing:
        raise ValueError(f"Agent eval release metadata is missing keys: {', '.join(missing)}")
    if metadata["package_name"] != "agent-eval-contract":
        raise ValueError("Agent eval release metadata package_name must be agent-eval-contract.")
    if metadata["status"] not in {"public_package_candidate", "published"}:
        raise ValueError("Agent eval release metadata status is invalid.")
    if not isinstance(metadata["public_promise"], str) or not metadata["public_promise"].strip():
        raise ValueError("Agent eval release metadata public_promise must be a non-empty string.")
    for key in ("public_surfaces", "out_of_scope", "public_modules"):
        value = metadata[key]
        if (
            not isinstance(value, list)
            or not value
            or not all(isinstance(item, str) for item in value)
        ):
            raise ValueError(f"Agent eval release metadata field '{key}' must be a string list.")
    blockers = metadata["release_blockers"]
    if not isinstance(blockers, list) or not all(isinstance(item, str) for item in blockers):
        raise ValueError(
            "Agent eval release metadata field 'release_blockers' must be a string list."
        )
