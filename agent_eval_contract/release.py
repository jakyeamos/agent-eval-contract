from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RELEASE_METADATA_PATH = Path(__file__).resolve().parent / "release_metadata.json"
REQUIRED_RELEASE_METADATA_KEYS = (
    "package_name",
    "version",
    "status",
    "python_requires",
    "portable_surfaces",
    "aios_owned_surfaces",
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
    if metadata["status"] not in {"in_repo_package_candidate", "repo_extracted"}:
        raise ValueError("Agent eval release metadata status is invalid.")
    for key in (
        "portable_surfaces",
        "aios_owned_surfaces",
        "public_modules",
        "release_blockers",
    ):
        value = metadata[key]
        if (
            not isinstance(value, list)
            or not value
            or not all(isinstance(item, str) for item in value)
        ):
            raise ValueError(f"Agent eval release metadata field '{key}' must be a string list.")
