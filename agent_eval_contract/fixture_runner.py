from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .clean_room import run_clean_room_contract_check
from .models import FixtureBundleManifest
from .release import load_release_metadata
from .samples import SAMPLE_FILES, SAMPLE_ROOT, load_sample
from .schema_export import export_json_schemas
from .templates import render_eval_template, supported_template_ids


def write_contract_fixture_bundle(
    output_dir: Path,
    *,
    sample_root: Path = SAMPLE_ROOT,
) -> dict[str, Any]:
    resolved = output_dir.expanduser().resolve()
    samples_dir = resolved / "samples"
    templates_dir = resolved / "templates"
    schemas_dir = resolved / "schemas"
    samples_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)
    schemas_dir.mkdir(parents=True, exist_ok=True)

    sample_ids: list[str] = []
    for sample_id, filename in sorted(SAMPLE_FILES.items()):
        sample = load_sample(sample_id, sample_root=sample_root)
        (samples_dir / filename).write_text(
            json.dumps(sample, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        sample_ids.append(sample_id)

    template_ids: list[str] = []
    for template_id in supported_template_ids():
        (templates_dir / f"{template_id}.md").write_text(
            render_eval_template(template_id),
            encoding="utf-8",
        )
        template_ids.append(template_id)

    check = run_clean_room_contract_check(template_root=templates_dir, sample_root=samples_dir)
    metadata = load_release_metadata()
    schema_files = export_json_schemas(schemas_dir)
    manifest = FixtureBundleManifest(
        version=str(metadata["version"]),
        contract_version=str(metadata["contract_version"]),
        samples=sample_ids,
        templates=template_ids,
        schemas=schema_files,
        metadata={
            "clean_room_check": check,
            "public_surfaces": metadata["public_surfaces"],
            "out_of_scope": metadata["out_of_scope"],
        },
    ).model_dump(mode="json")
    (resolved / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Produce an agent-eval-contract fixture bundle with samples, templates, and JSON Schemas."
    )
    parser.add_argument(
        "--output-dir", required=True, help="Directory to write fixture artifacts into."
    )
    args = parser.parse_args(argv)
    manifest = write_contract_fixture_bundle(Path(args.output_dir))
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
