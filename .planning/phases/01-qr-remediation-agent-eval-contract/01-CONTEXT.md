# Phase 1: QR remediation: agent-eval-contract - Context

**Gathered:** 2026-07-04
**Status:** Ready for planning
**Source:** PRD Express Path (/Users/jakyeamos/.local/state/quality-runner/fleet/per-repo-summaries-20260704/agent-eval-contract.md)

<domain>
## Phase Boundary

Plan the remediation work for agent-eval-contract from Quality Runner run qr-low-risk-post-branch-fix-20260704-agent-eval-contract.
This phase is planning-only until execute-phase runs. Quality Runner remains advisory-only: it identifies findings, remediation clusters, and verification suggestions, but all source changes happen in /Users/jakyeamos/projects/agent-eval-contract.

Findings: 1
Severity: `warning` 1
Categories: `capability` 1
Fleet phase candidate: Phase 1 - Quick Closers
Requirement: QR-AGENT-EVAL-CONTRACT

</domain>

<decisions>
## Implementation Decisions

### D-01 - QR summary is the planning source
- Use /Users/jakyeamos/.local/state/quality-runner/fleet/per-repo-summaries-20260704/agent-eval-contract.md and the artifacts under /Users/jakyeamos/projects/agent-eval-contract/.quality-runner/runs/qr-low-risk-post-branch-fix-20260704-agent-eval-contract as the source of truth for this remediation phase.

### D-02 - Cluster-oriented remediation
- Plan and execute coherent remediation batches by QR cluster, not one isolated edit per finding row.

### D-03 - Behavior preservation
- Prefer behavior-preserving refactors, hardening, and simplification. Do not change product behavior unless a QR hardening cluster explicitly requires safer behavior.

### D-04 - Existing project conventions first
- Read the target files and local manifests before editing. Follow existing package-manager, formatter, test, and architecture conventions. Use pnpm for JavaScript package scripts.

### D-05 - Evidence-backed closure
- A cluster is done only when focused repo verification passes and a post-remediation QR run shows the fingerprints cleared or are dispositioned with evidence.

### Claude's Discretion
- Choose exact helper extraction boundaries, naming, and task order when the QR document identifies the finding but not the implementation shape.
- If a cluster turns out to require product, API, or design decisions, stop that cluster and capture the question instead of guessing.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Quality Runner Inputs
- `/Users/jakyeamos/.local/state/quality-runner/fleet/per-repo-summaries-20260704/agent-eval-contract.md` - Per-repo QR summary used as this phase PRD.
- `/Users/jakyeamos/projects/agent-eval-contract/.quality-runner/runs/qr-low-risk-post-branch-fix-20260704-agent-eval-contract/quality-audit.json` - Quality audit report.
- `/Users/jakyeamos/projects/agent-eval-contract/.quality-runner/runs/qr-low-risk-post-branch-fix-20260704-agent-eval-contract/remediation-plan.json` - QR remediation plan.
- `/Users/jakyeamos/projects/agent-eval-contract/.quality-runner/runs/qr-low-risk-post-branch-fix-20260704-agent-eval-contract/code-quality-scan.json` - Code-quality scan fingerprints.
- `/Users/jakyeamos/projects/agent-eval-contract/.quality-runner/runs/qr-low-risk-post-branch-fix-20260704-agent-eval-contract/resolution-ledger.md` - Resolution ledger for closure evidence.
- `/Users/jakyeamos/projects/agent-eval-contract/.quality-runner/runs/qr-low-risk-post-branch-fix-20260704-agent-eval-contract/agent-handoff.md` - QR agent handoff.

</canonical_refs>

<specifics>
## Top Findings

- `missing-runtime-smoke` warning capability: Required quality capability is missing: runtime_smoke. Fix: Add a Python smoke gate that exercises installed console scripts. Evidence: Capability map lists runtime_smoke as missing.; Missing command capability evidence: no quality command found for runtime_smoke.

## Remediation Clusters

No active remediation clusters; preserve the zero-finding baseline and verify QR stays clean.

</specifics>

<deferred>
## Deferred Ideas

- Broad rewrites outside the QR clusters.
- Running Quality Runner as an executor or letting QR mutate source code.
- Remediating repos outside agent-eval-contract; each repo gets its own GSD phase.

</deferred>

---

*Phase: 1*
*Context gathered: 2026-07-04 via QR per-repo PRD*
