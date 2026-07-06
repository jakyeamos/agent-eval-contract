"""Validate eval records before uploading them to a dashboard.

Reject anything that does not match the contract so the dashboard only ever
ingests well-formed records. Run it with `python validate_before_upload.py`;
it validates an in-memory batch and reports how many records passed.
"""

from __future__ import annotations

from pydantic import ValidationError

from agent_eval_contract import validate_eval_run

BATCH = [
    {
        "run_id": "run-checkout-discount-001",
        "task_id": "task-checkout-discount-001",
        "harness": "pytest",
        "model": "gpt-5",
        "final_status": "success",
    },
    {
        "run_id": "run-checkout-discount-002",
        "task_id": "task-checkout-discount-001",
        "harness": "pytest",
        "model": "gpt-5",
        "final_status": "not-a-real-status",
    },
]


def main() -> None:
    accepted = 0
    for index, record in enumerate(BATCH):
        try:
            validate_eval_run(record)
        except ValidationError as error:
            print(f"record {index}: rejected ({error.error_count()} field error(s))")
            continue
        accepted += 1
        print(f"record {index}: ok")
    print(f"{accepted}/{len(BATCH)} records ready to upload")


if __name__ == "__main__":
    main()
