from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .external import normalize_external_result
from .fixture_runner import write_contract_fixture_bundle
from .schema_export import export_json_schemas
from .validators import (
    validate_eval_failure,
    validate_eval_run,
    validate_eval_score,
    validate_eval_task,
)


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.expanduser().resolve().read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return loaded


def _print_json(value: BaseModel | dict[str, Any] | list[str]) -> None:
    payload = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
    print(json.dumps(payload, indent=2, sort_keys=True))


def _run_fixtures(args: argparse.Namespace) -> int:
    _print_json(write_contract_fixture_bundle(Path(args.output_dir)))
    return 0


def _run_schemas(args: argparse.Namespace) -> int:
    _print_json({"schemas": export_json_schemas(Path(args.output_dir))})
    return 0


def _run_validate(args: argparse.Namespace) -> int:
    data = _load_json(Path(args.file))
    validators = {
        "task": validate_eval_task,
        "run": validate_eval_run,
        "score": validate_eval_score,
        "failure": validate_eval_failure,
    }
    _print_json(validators[args.kind](data))
    return 0


def _run_normalize(args: argparse.Namespace) -> int:
    data = _load_json(Path(args.file))
    normalized = normalize_external_result(
        data,
        eval_task_id=args.task_id,
        harness=args.harness,
        model=args.model,
    )
    _print_json(normalized)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-eval-contract",
        description="Validate, normalize, and export portable agent evaluation contracts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    fixtures = subparsers.add_parser(
        "fixtures", help="Write sample records, templates, and schemas."
    )
    fixtures.add_argument(
        "--output-dir", required=True, help="Directory to write fixture artifacts into."
    )
    fixtures.set_defaults(func=_run_fixtures)

    schemas = subparsers.add_parser(
        "schemas", help="Export JSON Schemas for public contract models."
    )
    schemas.add_argument(
        "--output-dir", required=True, help="Directory to write schema files into."
    )
    schemas.set_defaults(func=_run_schemas)

    validate = subparsers.add_parser(
        "validate", help="Validate a JSON record against a contract model."
    )
    validate.add_argument("--kind", choices=("task", "run", "score", "failure"), required=True)
    validate.add_argument("--file", required=True, help="JSON file to validate.")
    validate.set_defaults(func=_run_validate)

    normalize = subparsers.add_parser("normalize", help="Normalize external harness output.")
    normalize.add_argument("--harness", choices=("terminal-bench", "swe-bench"), required=True)
    normalize.add_argument("--file", required=True, help="External result JSON file to normalize.")
    normalize.add_argument("--task-id", help="Task id to use when the external result omits one.")
    normalize.add_argument("--model", help="Model name to use when the external result omits one.")
    normalize.set_defaults(func=_run_normalize)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
