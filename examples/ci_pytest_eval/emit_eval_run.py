"""Emit a validated EvalRun for a CI pytest job.

In a real CI job you would run pytest, capture its outcome, and fill the
fields below from that outcome. Here the outcome is hard-coded so the example
is deterministic. Run it with `python emit_eval_run.py`; it prints a validated
EvalRun record as JSON on stdout.
"""

from __future__ import annotations

import json
from pathlib import Path

from agent_eval_contract import validate_eval_run

TASK = json.loads((Path(__file__).parent / "eval_task.json").read_text(encoding="utf-8"))


def build_eval_run() -> dict[str, object]:
    # Stand-in for a real pytest outcome captured in CI.
    tests_passed = True
    return {
        "run_id": "run-checkout-discount-001",
        "task_id": TASK["task_id"],
        "harness": "pytest",
        "model": "gpt-5",
        "mode": "autonomous",
        "context_profile": TASK["context_profile"],
        "final_status": "success" if tests_passed else "failed",
        "checks": ["pytest tests/test_checkout.py -q"],
        "output_summary": "Restored discount in the checkout total and added a regression test.",
        "metadata": {"ci": {"provider": "github-actions", "run_attempt": 1}},
    }


def main() -> None:
    run = validate_eval_run(build_eval_run())
    print(json.dumps(run.model_dump(mode="json"), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
