# Coding and contract conventions

- Use Python 3.12+ with annotations, explicit public types, and strict
  `basedpyright` checking. Do not use `Any` in production code.
- Keep the public vocabulary generic. Put harness-specific extensions in
  `metadata` or a separate adapter package.
- Treat Pydantic models and exported JSON Schema as the record contract.
  Unknown top-level fields must fail fast; schema changes require snapshots and
  frozen compatibility fixtures.
- Keep adapters as plain-data transforms. They must not execute record content,
  call providers, or import private workflow state.
- Keep examples runnable and public-safe. Do not place credentials, raw private
  transcripts, local paths, or unpublished evaluation evidence in fixtures.
- Prefer small focused functions and deterministic sorted output. Match the
  existing Ruff configuration and test the behavior contract, not internals.
