---
id: agent-eval-contract.repo-context
title: Agent Eval Contract Repository Context
tier: project
status: active
last_reviewed: 2026-07-22
applies_when:
  - repo_context
tags:
  - agent-evaluation
  - contracts
  - python
---

# Agent Eval Contract context index

Load this index before non-trivial work, then route to the smallest relevant
source. Do not dump the repository or generated schema snapshots into context.

| Task evidence | Read |
| --- | --- |
| Public record shape or validation | `docs/contract.md`, `docs/field-reference.md`, `agent_eval_contract/models.py`, `validators.py` |
| Adapter or normalization work | `docs/adapters.md`, `docs/writing-adapters.md`, `agent_eval_contract/external.py` |
| Compatibility or versioning | `docs/stability.md`, `tests/test_backward_compatibility.py`, `tests/snapshots/` |
| Release or publication | `docs/release-checklist.md`, `RELEASE.md`, `SECURITY.md`, `.github/workflows/release.yml` |
| Quality checks | `README.md`, `pyproject.toml`, `scripts/pre_cr_coverage.py` |

The public core must remain provider-neutral and AIOS-independent. Examples and
fixtures are public-safe contract evidence, not a place for real transcripts,
credentials, paths, or private task data.
