# Canonical commands and quality gates

Run from the repository root with the locked `uv` environment:

```sh
uv sync --dev
uv run ruff check agent_eval_contract scripts tests
uv run ruff format --check agent_eval_contract scripts tests
uv run basedpyright agent_eval_contract scripts tests
uv run pytest -q
uv run --with vulture vulture agent_eval_contract scripts tests --min-confidence 70
uv build --out-dir /tmp/agent-eval-contract-dist
python3 scripts/check_environment_contract.py
```

The same commands are declared in `.pre-cr.json` and CI. The environment
contract check is a local, deterministic guard for routed context, strict type
checking, quality-command declarations, approval boundaries, and secret-like
tracked paths.

Quality commands must be bounded and offline-capable. They must not publish,
deploy, tag, push, call a model provider, collect credentials, or mutate a
release. Release smoke tests use a disposable virtual environment and an
explicitly reviewed package artifact.
