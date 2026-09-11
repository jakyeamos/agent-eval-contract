# Accepted purpose reconciliation

On 2026-09-11 the user explicitly accepted the documented purpose through the fleet bootstrap review: a provider-neutral record/schema validation and normalization package that does not run evaluations or models; Quality Runner remediation is maintenance only. This is a faithful summary reported by the coordinating task, not a verbatim transcript.

The prior root at source e0ee78d4fe7d72f8c5f6bc429a80bb1a4e574487 incorrectly promoted the maintenance project in `.planning/PROJECT.md` to product identity. Its exact revision 1 bytes and maturity values remain in `history/contract-revision-1.json`. The former evaluation-execution targets are superseded, not silently completed.

README and `.agents/context/architecture.md` own the public purpose. `docs/contract.md` owns record semantics; `docs/stability.md` is the direct compatibility owner linked by README. Its explicit policy permits additive backward-compatible enum members without a contract-version bump, while breaking record meaning/shape requires a bump. The contradictory blanket enum-bump sentence in `docs/writing-adapters.md` was corrected to the direct stability owner's exact rule after coordinator review. This reconciles documentation; it does not change API or version policy.

Preserved: strict top-level records; metadata/separate adapters for harness detail; frozen compatibility fixtures and schema snapshots; package/contract version distinction; no model calls, eval execution, storage, orchestration, benchmark datasets or hosted dashboard; no registry/publication claim from local checks. No release tag or package publication is authorized here.

The required environment-contract check rejected the July 25 context-index review date. The index and all eight routed packets were reread on September 11; only the index review date was refreshed, with gate thresholds and source rules unchanged.

This bootstrap associates existing documented responsibilities with exact source paths. Narrow local fixture assertions remain separate from full interoperability, downstream consumer adoption, published-package parity and real evaluation correctness. Maturity records foundations conservatively; source associations and tests do not establish external operational use.
