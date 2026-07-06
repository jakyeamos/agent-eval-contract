#!/usr/bin/env bash
# Validate the eval artifacts a CI job produces: the task record and the run
# record emitted from the pytest outcome. Exits non-zero if either is invalid.
set -euo pipefail

cd "$(dirname "$0")"

agent-eval-contract validate --kind task --file eval_task.json --quiet

run_file="$(mktemp)"
trap 'rm -f "$run_file"' EXIT

python emit_eval_run.py >"$run_file"
agent-eval-contract validate --kind run --file "$run_file" --quiet

echo "eval artifacts valid"
