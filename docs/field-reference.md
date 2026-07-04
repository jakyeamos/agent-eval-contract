# Field Reference

This reference defines the public meaning of each core record. Unknown top-level fields are rejected. Put harness-specific or project-specific values under `metadata`.

## EvalTask

| Field | Required | Meaning |
| --- | --- | --- |
| `task_id` | yes | Stable id for the work item being evaluated. |
| `title` | yes | Short human-readable task name. |
| `description` | yes | Prompt, issue, benchmark statement, or task summary. |
| `source` | no | Origin of the task: `manual`, `ci`, `benchmark`, `production_trace`, or `synthetic`. |
| `context_profile` | no | Context available to the run: `repo_only`, `provided_context`, `clean_room`, `tool_augmented`, or `full_workspace`. |
| `acceptance_criteria` | no | Observable success criteria. |
| `repo` | no | Repository or project id. |
| `start_revision` | no | Commit, tag, snapshot id, or benchmark base revision. |
| `tags` | no | Search/filter labels. |
| `created_at` | no | ISO timestamp. Defaults to validation time. |
| `metadata` | no | JSON object for extensions. |

## EvalRun

| Field | Required | Meaning |
| --- | --- | --- |
| `run_id` | yes | Stable id for one attempt. |
| `task_id` | yes | `EvalTask.task_id` this run attempts. |
| `harness` | yes | Harness or runner name, such as `pytest`, `terminal-bench`, or `swe-bench`. |
| `model` | yes | Model, agent, or system under evaluation. |
| `mode` | no | Run style: `interactive`, `autonomous`, `shadow`, `replay`, or `benchmark`. |
| `context_profile` | no | Context available during the run. |
| `final_status` | yes | `success`, `partial`, `failed`, `abandoned`, or `error`. |
| `started_at` / `completed_at` | no | ISO timestamps when known. |
| `duration_ms` | no | Non-negative wall-clock duration. |
| `total_tokens` | no | Non-negative total token count. |
| `estimated_cost_usd` | no | Non-negative estimated cost. |
| `tool_calls` | no | Non-negative count of tool calls. |
| `failed_steps` | no | Non-negative count of failed commands, checks, or steps. |
| `files_changed` | no | Non-negative count of changed files. |
| `checks` | no | Commands, tests, assertions, or harness checks executed. |
| `output_summary` | no | Human-readable result summary. |
| `metadata` | no | JSON object for extensions. |

## EvalScore

| Field | Required | Meaning |
| --- | --- | --- |
| `run_id` | yes | Run being scored. |
| `overall_score` | yes | Number from `0.0` to `1.0`. |
| `metrics` | no | Named metric scores, each from `0.0` to `1.0`. |
| `passed` | no | Boolean pass/fail when the score has a binary verdict. |
| `reviewer_notes` | no | Human or automated scoring notes. |
| `metadata` | no | JSON object for extensions. |

## EvalFailure

| Field | Required | Meaning |
| --- | --- | --- |
| `failure_id` | yes | Stable id for a failure record. |
| `run_id` | yes | Run where the failure appeared. |
| `failure_types` | yes | One or more taxonomy labels. |
| `summary` | yes | Short failure description. |
| `suspected_cause` | no | Best current cause hypothesis. |
| `affected_components` | no | Files, modules, tools, or workflows involved. |
| `recommended_fixes` | no | Follow-up actions. |
| `priority` | no | `low`, `medium`, `high`, or `critical`. |
| `regression_task_id` | no | Follow-up task id when one exists. |
| `metadata` | no | JSON object for extensions. |

## NormalizedRun

`NormalizedRun` is the adapter output for external harnesses. It is intentionally compact: task id, harness, model, status, checks, optional duration, optional score, and raw source metadata.

The normalizers preserve JSON-compatible input under `metadata.raw` and identify the adapter under `metadata.source`.
