from __future__ import annotations

import argparse
import json
import sys
from importlib import metadata
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from .external import normalize_external_result
from .fixture_runner import write_contract_fixture_bundle
from .models import (
    EvalFailure,
    EvalRun,
    EvalScore,
    EvalTask,
    ExternalResult,
    NormalizedRun,
)
from .release import load_release_metadata
from .schema_export import export_json_schemas
from .validators import (
    validate_eval_failure,
    validate_eval_run,
    validate_eval_score,
    validate_eval_task,
)

_VALIDATORS = {
    "task": validate_eval_task,
    "run": validate_eval_run,
    "score": validate_eval_score,
    "failure": validate_eval_failure,
}

_INSPECT_MODELS: dict[str, type[BaseModel]] = {
    "task": EvalTask,
    "run": EvalRun,
    "score": EvalScore,
    "failure": EvalFailure,
    "external_result": ExternalResult,
    "normalized_run": NormalizedRun,
}


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.expanduser().resolve().read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return loaded


def _print_json(value: BaseModel | dict[str, Any] | list[str]) -> None:
    payload = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
    print(json.dumps(payload, indent=2, sort_keys=True))


def _emit(value: BaseModel | dict[str, Any], *, quiet: bool, pretty: bool) -> None:
    if quiet:
        return
    payload = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
    indent = 2 if pretty else None
    print(json.dumps(payload, indent=indent, sort_keys=True))


def _format_validation_error(record_label: str, error: ValidationError) -> str:
    blocks = [f"Invalid {record_label} record"]
    for err in error.errors():
        location = ".".join(str(part) for part in err["loc"]) or "(root)"
        block = f"\nField: {location}\nError: {err['msg']}"
        if "input" in err:
            block += f"\nValue: {json.dumps(err['input'], default=str)}"
        blocks.append(block)
    return "\n".join(blocks)


def _run_fixtures(args: argparse.Namespace) -> int:
    _print_json(write_contract_fixture_bundle(Path(args.output_dir)))
    return 0


def _run_schemas(args: argparse.Namespace) -> int:
    _print_json({"schemas": export_json_schemas(Path(args.output_dir))})
    return 0


def _run_validate(args: argparse.Namespace) -> int:
    data = _load_json(Path(args.file))
    try:
        record = _VALIDATORS[args.kind](data)
    except ValidationError as error:
        if args.json_errors:
            print(json.dumps(error.errors(), indent=2, default=str), file=sys.stderr)
        else:
            print(_format_validation_error(f"eval_{args.kind}", error), file=sys.stderr)
        return 1
    _emit(record, quiet=args.quiet, pretty=args.pretty)
    return 0


def _run_inspect(args: argparse.Namespace) -> int:
    data = _load_json(Path(args.file))
    matches: list[str] = []
    record: BaseModel | None = None
    for kind, model in _INSPECT_MODELS.items():
        try:
            parsed = model.model_validate(data)
        except ValidationError:
            continue
        matches.append(kind)
        record = parsed
    result: dict[str, Any] = {"file": str(Path(args.file)), "matches": matches}
    if len(matches) == 1 and record is not None:
        result["record"] = record.model_dump(mode="json")
    _emit(result, quiet=args.quiet, pretty=args.pretty)
    return 0 if matches else 1


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


def _run_version(_args: argparse.Namespace) -> int:
    release_metadata = load_release_metadata()
    try:
        package_version = metadata.version("agent-eval-contract")
    except metadata.PackageNotFoundError:
        package_version = str(release_metadata["version"])
    print(f"package: {package_version}")
    print(f"contract: {release_metadata['contract_version']}")
    return 0


def _add_output_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--quiet", action="store_true", help="Print nothing on success; rely on the exit code."
    )
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output.")


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
    validate.add_argument(
        "--json-errors",
        action="store_true",
        help="Emit raw JSON validation errors instead of the friendly format.",
    )
    _add_output_flags(validate)
    validate.set_defaults(func=_run_validate)

    inspect = subparsers.add_parser(
        "inspect", help="Report which contract models a JSON record matches."
    )
    inspect.add_argument("--file", required=True, help="JSON file to inspect.")
    _add_output_flags(inspect)
    inspect.set_defaults(func=_run_inspect)

    normalize = subparsers.add_parser("normalize", help="Normalize external harness output.")
    normalize.add_argument("--harness", choices=("terminal-bench", "swe-bench"), required=True)
    normalize.add_argument("--file", required=True, help="External result JSON file to normalize.")
    normalize.add_argument("--task-id", help="Task id to use when the external result omits one.")
    normalize.add_argument("--model", help="Model name to use when the external result omits one.")
    normalize.set_defaults(func=_run_normalize)

    version = subparsers.add_parser("version", help="Print package and contract versions.")
    version.set_defaults(func=_run_version)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
