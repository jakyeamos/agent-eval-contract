# Security and approval constraints

The public boundary excludes credentials, private paths, environment files, raw
prompts, transcripts, and unpublished evaluation evidence. Fixtures and
examples must use synthetic or public-safe values. The package never executes
record content and must remain provider-neutral.

Validation, normalization, schema export, and tests must not call model
providers, collect credentials, import AIOS, or write to external services.
Release publication, tagging, and trusted-publishing changes require explicit
human approval and the reviewed release checklist. CI may validate a package
artifact but must not publish from ordinary test jobs.

If a guard, dependency audit, or provenance check is unavailable, preserve the
unknown or blocked result and repair the smallest owned surface. Never weaken a
security gate or add a broad exclusion to make it pass.
