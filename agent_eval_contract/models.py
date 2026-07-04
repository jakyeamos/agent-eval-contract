from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator

ContextProfile = Literal[
    "repo_only",
    "provided_context",
    "clean_room",
    "tool_augmented",
    "full_workspace",
]
EvalTaskSource = Literal[
    "manual",
    "ci",
    "benchmark",
    "production_trace",
    "synthetic",
]
EvalRunMode = Literal[
    "interactive",
    "autonomous",
    "shadow",
    "replay",
    "benchmark",
]
FinalStatus = Literal["success", "partial", "failed", "abandoned", "error"]
FailurePriority = Literal["low", "medium", "high", "critical"]
ExternalHarness = Literal["terminal-bench", "swe-bench"]

CONTEXT_PROFILES: frozenset[str] = frozenset(
    {"repo_only", "provided_context", "clean_room", "tool_augmented", "full_workspace"}
)
EVAL_TASK_SOURCES: frozenset[str] = frozenset(
    {"manual", "ci", "benchmark", "production_trace", "synthetic"}
)
EVAL_RUN_MODES: frozenset[str] = frozenset(
    {"interactive", "autonomous", "shadow", "replay", "benchmark"}
)
FINAL_STATUSES: frozenset[str] = frozenset({"success", "partial", "failed", "abandoned", "error"})
FAILURE_PRIORITIES: frozenset[str] = frozenset({"low", "medium", "high", "critical"})
EXTERNAL_HARNESSES: frozenset[str] = frozenset({"terminal-bench", "swe-bench"})

Score = Annotated[float, Field(ge=0.0, le=1.0)]
NonNegativeInt = Annotated[int, Field(ge=0)]
NonNegativeFloat = Annotated[float, Field(ge=0.0)]


def utc_now() -> datetime:
    return datetime.now(UTC)


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class EvalTask(ContractModel):
    task_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    source: EvalTaskSource = "manual"
    context_profile: ContextProfile = "repo_only"
    acceptance_criteria: list[str] = Field(default_factory=list)
    repo: str | None = None
    start_revision: str | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class EvalRun(ContractModel):
    run_id: str = Field(min_length=1)
    task_id: str = Field(min_length=1)
    harness: str = Field(min_length=1)
    model: str = Field(min_length=1)
    mode: EvalRunMode = "interactive"
    context_profile: ContextProfile = "repo_only"
    final_status: FinalStatus
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: NonNegativeInt | None = None
    total_tokens: NonNegativeInt | None = None
    estimated_cost_usd: NonNegativeFloat | None = None
    tool_calls: NonNegativeInt = 0
    failed_steps: NonNegativeInt = 0
    files_changed: NonNegativeInt = 0
    checks: list[str] = Field(default_factory=list)
    output_summary: str | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class EvalScore(ContractModel):
    run_id: str = Field(min_length=1)
    overall_score: Score
    metrics: dict[str, Score] = Field(default_factory=dict)
    passed: bool | None = None
    reviewer_notes: str | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class EvalFailure(ContractModel):
    failure_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    failure_types: list[str] = Field(min_length=1)
    summary: str = Field(min_length=1)
    suspected_cause: str | None = None
    affected_components: list[str] = Field(default_factory=list)
    recommended_fixes: list[str] = Field(default_factory=list)
    priority: FailurePriority = "medium"
    regression_task_id: str | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class ExternalResult(ContractModel):
    harness: str = Field(min_length=1)
    task_id: str | None = None
    model: str | None = None
    passed: bool | None = None
    success: bool | None = None
    score: Score | None = None
    tests_run: list[str] = Field(default_factory=list)
    duration_ms: NonNegativeInt | None = None
    raw: dict[str, JsonValue] = Field(default_factory=dict)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class NormalizedRun(ContractModel):
    task_id: str = Field(min_length=1)
    harness: str = Field(min_length=1)
    model: str = Field(min_length=1)
    mode: EvalRunMode = "benchmark"
    context_profile: ContextProfile = "clean_room"
    final_status: FinalStatus
    checks: list[str] = Field(default_factory=list)
    duration_ms: NonNegativeInt | None = None
    score: Score | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class FixtureBundleManifest(ContractModel):
    package: str = "agent-eval-contract"
    version: str = Field(min_length=1)
    contract_version: str = Field(min_length=1)
    generated_at: datetime = Field(default_factory=utc_now)
    samples: list[str] = Field(default_factory=list)
    templates: list[str] = Field(default_factory=list)
    schemas: list[str] = Field(default_factory=list)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @field_validator("package")
    @classmethod
    def package_name_matches(_cls, value: str) -> str:
        if value != "agent-eval-contract":
            raise ValueError("package must be agent-eval-contract")
        return value
