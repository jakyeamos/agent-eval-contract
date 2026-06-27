from __future__ import annotations

from pathlib import Path

TEMPLATE_SECTIONS: dict[str, tuple[str, ...]] = {
    "major-task-eval": (
        "Task Summary",
        "Original Acceptance Criteria",
        "Context Profile",
        "AIOS Condition",
        "Checks Run",
        "Check Results",
        "Failure Taxonomy Labels",
        "Final Confidence Level",
    ),
    "failure-record": (
        "Identifiers",
        "Condition",
        "Context Profile",
        "Failure Types",
        "Summary",
        "Priority",
        "Standards or Project Truth Update Needed",
    ),
    "shadow-branch-comparison": (
        "Branches",
        "Task Description",
        "Acceptance Criteria",
        "Context Profile",
        "AIOS Condition",
        "Test Results",
        "Shadow Branch Delta",
        "Recommendation",
    ),
    "backfill-hotspot": (
        "Hotspot",
        "Evidence",
        "Risk",
        "Suggested Fix",
        "Priority",
        "Blocking Status",
        "Related Failure Taxonomy Label",
    ),
    "portable-context-packet": (
        "Packet ID",
        "Scope",
        "Task Summary",
        "Included Repo Files/Docs",
        "Excluded Content",
        "Privacy/Secret Review",
        "Expiration/Staleness Notes",
    ),
}


def supported_template_ids() -> tuple[str, ...]:
    return tuple(sorted(TEMPLATE_SECTIONS))


def render_eval_template(template_id: str) -> str:
    required_sections = TEMPLATE_SECTIONS.get(template_id)
    if required_sections is None:
        allowed = ", ".join(supported_template_ids())
        raise ValueError(f"Unknown eval template id '{template_id}'. Use one of: {allowed}.")
    title = template_id.replace("-", " ").title()
    sections = "\n\n".join(f"## {section}\n\nTODO" for section in required_sections)
    return f"# {title}\n\n{sections}\n"


def validate_eval_template(template_id: str, markdown: str) -> None:
    required_sections = TEMPLATE_SECTIONS.get(template_id)
    if required_sections is None:
        allowed = ", ".join(supported_template_ids())
        raise ValueError(f"Unknown eval template id '{template_id}'. Use one of: {allowed}.")
    if not markdown.strip():
        raise ValueError(f"Eval template '{template_id}' must not be empty.")
    missing = [
        section
        for section in required_sections
        if f"## {section}" not in markdown and f"# {section}" not in markdown
    ]
    if missing:
        raise ValueError(
            f"Eval template '{template_id}' is missing required sections: {', '.join(missing)}"
        )


def validate_eval_template_file(path: Path, *, template_id: str | None = None) -> str:
    resolved = path.expanduser().resolve()
    actual_id = template_id or resolved.stem
    validate_eval_template(actual_id, resolved.read_text(encoding="utf-8"))
    return actual_id


def validate_template_directory(template_root: Path) -> list[str]:
    resolved = template_root.expanduser().resolve()
    validated: list[str] = []
    for template_id in supported_template_ids():
        validate_eval_template_file(resolved / f"{template_id}.md", template_id=template_id)
        validated.append(template_id)
    return validated
