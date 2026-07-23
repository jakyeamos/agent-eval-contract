# Agent operating contract

Read this router and `.agents/context/README.md` before repository work.

- Treat this repository as a public, provider-neutral contract library. It
  validates and normalizes records; it does not call models, run evals, store
  history, or import AIOS.
- Use the documented `uv` quality path. Keep public vocabulary generic and put
  harness-specific fields in `metadata` or a separate adapter package.
- Preserve schema snapshots, backward-compatibility fixtures, release metadata,
  and examples unless the contract change explicitly updates their policy.
- Keep credentials, raw prompts, private transcripts, and unpublished eval
  evidence out of committed fixtures and schemas.
- Do not publish, tag, or change PyPI/GitHub release state without explicit
  approval. Roll back by selecting a prior published version; do not rewrite
  release history.
- A change is done when contract tests, lint, format, type, dead-code, and the
  relevant build/release checks pass and the public documentation matches the
  exported schema.
