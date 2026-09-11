---
id: agent-eval-contract.repo-context
title: Agent Eval Contract Repository Context
tier: project
status: active
last_reviewed: 2026-09-11
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
| Architecture and boundaries | [architecture](architecture.md) |
| Commands and quality gates | [commands](commands.md) |
| Python and contract conventions | [conventions](conventions.md) |
| Security and approval constraints | [security](security.md) |
| Failure diagnosis and recovery | [failure modes](failure-modes.md) |
| Canonical implementation examples | [examples](examples.md) |
| Definition of done | [done](done.md) |
| Release, deployment, and rollback | [deployment](deployment.md) |
| Public record shape or validation | [contract docs](../../docs/contract.md), [field reference](../../docs/field-reference.md), `agent_eval_contract/models.py`, `agent_eval_contract/validators.py` |
| Adapter or normalization work | [adapter docs](../../docs/adapters.md), [adapter writing guide](../../docs/writing-adapters.md), `agent_eval_contract/external.py` |
| Compatibility or versioning | [stability](../../docs/stability.md), `tests/test_backward_compatibility.py`, `tests/snapshots/` |
| Release or publication | [release checklist](../../docs/release-checklist.md), [release policy](../../RELEASE.md), [security](../../SECURITY.md), `.github/workflows/release.yml` |

The public core must remain provider-neutral and AIOS-independent. Examples and
fixtures are public-safe contract evidence, not a place for real transcripts,
credentials, paths, or private task data.
