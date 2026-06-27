from __future__ import annotations

from typing import Literal, TypedDict

CONTEXT_PROFILES = frozenset(
    {
        "jakye_second_brain_full",
        "jakye_second_brain_limited",
        "jakye_repo_only",
        "peer_repo_only",
        "peer_portable_context_packet",
        "external_clean_room",
    }
)
EVAL_TASK_SOURCES = frozenset(
    {
        "real_workflow",
        "peer_trace",
        "controlled_benchmark",
        "external_benchmark",
        "second_brain_gold_set",
    }
)
EVAL_RUN_MODES = frozenset({"trace", "shadow", "second_brain_eval", "controlled", "external"})
FINAL_STATUSES = frozenset({"success", "partial", "failed", "abandoned"})
SHADOW_RECOMMENDATIONS = frozenset(
    {
        "trace_only",
        "possible_shadow_candidate",
        "good_shadow_candidate",
        "excellent_shadow_candidate",
    }
)
AUTOMATION_STATES = frozenset(
    {
        "DISCOVERED",
        "TRIAGED",
        "TRACE_ONLY",
        "CANDIDATE",
        "READY_FOR_SHADOW",
        "SHADOW_RUNNING",
        "SHADOW_COMPLETE",
        "PROMOTED",
        "REJECTED",
        "BLOCKED_CONTEXT",
        "BLOCKED_PRIVACY",
        "BLOCKED_ACCEPTANCE",
        "BLOCKED_TOOLING",
        "BLOCKED_HUMAN_REVIEW",
    }
)
FAILURE_PRIORITIES = frozenset({"low", "medium", "high", "critical"})
SCORE_FIELDS = (
    "task_success",
    "quality_adherence",
    "workflow_speed",
    "cost_efficiency",
    "context_effectiveness",
    "second_brain_effectiveness",
    "context_portability",
    "autonomy",
    "user_trust",
)

ContextProfile = Literal[
    "jakye_second_brain_full",
    "jakye_second_brain_limited",
    "jakye_repo_only",
    "peer_repo_only",
    "peer_portable_context_packet",
    "external_clean_room",
]
EvalTaskSource = Literal[
    "real_workflow",
    "peer_trace",
    "controlled_benchmark",
    "external_benchmark",
    "second_brain_gold_set",
]
EvalRunMode = Literal[
    "trace",
    "shadow",
    "second_brain_eval",
    "controlled",
    "external",
]
FinalStatus = Literal["success", "partial", "failed", "abandoned"]
ShadowRecommendation = Literal[
    "trace_only",
    "possible_shadow_candidate",
    "good_shadow_candidate",
    "excellent_shadow_candidate",
]
AutomationState = Literal[
    "DISCOVERED",
    "TRIAGED",
    "TRACE_ONLY",
    "CANDIDATE",
    "READY_FOR_SHADOW",
    "SHADOW_RUNNING",
    "SHADOW_COMPLETE",
    "PROMOTED",
    "REJECTED",
    "BLOCKED_CONTEXT",
    "BLOCKED_PRIVACY",
    "BLOCKED_ACCEPTANCE",
    "BLOCKED_TOOLING",
    "BLOCKED_HUMAN_REVIEW",
]
FailurePriority = Literal["low", "medium", "high", "critical"]


class EvalTask(TypedDict):
    task_id: str
    repo_id: str
    source: EvalTaskSource
    start_sha: str
    context_profile: ContextProfile
    task_type: str
    prompt_summary: str
    acceptance_criteria: list[str]
    success_criteria_files: list[str]
    created_at: str


class EvalRun(TypedDict):
    run_id: str
    task_id: str
    condition: str
    mode: EvalRunMode
    harness: str
    model: str
    context_profile: ContextProfile
    branch_name: str | None
    duration_ms: int
    total_tokens: int | None
    estimated_cost_usd: float | None
    tool_calls: int
    failed_commands: int
    files_changed: int
    tests_run: list[str]
    final_status: FinalStatus


class ShadowCandidate(TypedDict):
    candidate_id: str
    task_id: str
    peer_session_id: str | None
    score: float
    recommendation: ShadowRecommendation
    reasons: list[str]
    blockers: list[str]
    automation_state: AutomationState


class EvalScore(TypedDict):
    run_id: str
    task_success: float
    quality_adherence: float
    workflow_speed: float | None
    cost_efficiency: float | None
    context_effectiveness: float | None
    second_brain_effectiveness: float | None
    context_portability: float | None
    autonomy: float
    user_trust: float
    overall_score: float
    reviewer_notes: str | None


class EvalFailure(TypedDict):
    failure_id: str
    run_id: str
    failure_types: list[str]
    summary: str
    suspected_cause: str
    affected_components: list[str]
    recommended_fixes: list[str]
    priority: FailurePriority
    regression_task_created: bool
    backfill_item_created: bool
    standards_update_needed: bool
