# Common failure modes and recovery

- Validation rejects an unknown top-level field: move the harness-specific
  value into `metadata`, or make an intentional contract change with snapshots
  and compatibility fixtures.
- A schema snapshot changes unexpectedly: inspect the model diff, decide whether
  the contract version must change, then regenerate snapshots deliberately.
- An adapter cannot map required fields: preserve the source failure in a
  normalized result and document the missing input; do not invent values.
- CLI validation fails: rerun with `--json-errors`, repair the input or model
  contract, and add a focused regression fixture for the failure.
- A quality gate is unavailable or a dependency cache is missing: report the
  measurement gap and restore the locked local environment; do not weaken the
  gate or claim success from a partial run.
- A release smoke test fails: keep the artifact and logs, fix the smallest
  owned surface, and repeat the full ladder before publishing.
