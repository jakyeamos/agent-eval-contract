"""Normalize a raw SWE-bench result into a portable NormalizedRun.

Run it with `python normalize.py`; it reads swe_bench_result.json, normalizes
it, and prints the NormalizedRun as JSON. Raw fields are preserved under
`metadata.raw` so nothing from the harness is lost.
"""

from __future__ import annotations

import json
from pathlib import Path

from agent_eval_contract import normalize_swe_bench_result

RESULT = json.loads((Path(__file__).parent / "swe_bench_result.json").read_text(encoding="utf-8"))


def main() -> None:
    normalized = normalize_swe_bench_result(RESULT)
    print(json.dumps(normalized.model_dump(mode="json"), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
