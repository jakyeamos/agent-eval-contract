from __future__ import annotations

import sys
import trace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "agent_eval_contract"
COVERAGE_PATH = ROOT / ".pre-cr" / "coverage.lcov"


def _package_files() -> set[Path]:
    return {path.resolve() for path in PACKAGE_ROOT.rglob("*.py")}


def _write_lcov(results: trace.CoverageResults) -> None:
    counts = results.counts
    package_files = _package_files()
    COVERAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = ["TN:agent-eval-contract"]
    for source_file in sorted(package_files):
        executable_lines = {
            line_number
            for line_number, line in enumerate(
                source_file.read_text(encoding="utf-8").splitlines(),
                start=1,
            )
            if line.strip() and not line.lstrip().startswith("#")
        }
        if not executable_lines:
            continue
        lines.append(f"SF:{source_file.relative_to(ROOT).as_posix()}")
        for line_number in sorted(executable_lines):
            hit_count = counts.get((str(source_file), line_number), 0)
            lines.append(f"DA:{line_number},{hit_count}")
        lines.append(f"LF:{len(executable_lines)}")
        lines.append(
            f"LH:{sum(1 for line_number in executable_lines if counts.get((str(source_file), line_number), 0) > 0)}"
        )
        lines.append("end_of_record")
    COVERAGE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    tracer = trace.Trace(
        count=True, trace=False, ignoredirs=[sys.base_prefix, sys.base_exec_prefix]
    )
    exit_code = 0
    try:
        tracer.runctx(
            "raise SystemExit(pytest_main(['-q']))",
            {
                "__name__": "__pre_cr_coverage__",
                "pytest_main": __import__("pytest").main,
                "SystemExit": SystemExit,
            },
            {},
        )
    except SystemExit as exc:
        exit_code = int(exc.code or 0)
    _write_lcov(tracer.results())
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
