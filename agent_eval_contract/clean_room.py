from __future__ import annotations

from pathlib import Path
from typing import Any

from .samples import validate_all_samples
from .templates import validate_template_directory


def run_clean_room_contract_check(
    *,
    template_root: Path,
    sample_root: Path | None = None,
) -> dict[str, Any]:
    templates = validate_template_directory(template_root)
    samples = (
        validate_all_samples()
        if sample_root is None
        else validate_all_samples(sample_root=sample_root)
    )
    return {
        "ok": True,
        "template_count": len(templates),
        "sample_count": len(samples),
        "templates": templates,
        "samples": samples,
    }
