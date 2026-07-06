# Security Policy

## Supported versions

The latest released version on PyPI receives security fixes. Because the package
is pre-1.0, fixes ship in a new minor or patch release rather than as backports.

## Reporting a vulnerability

Please report vulnerabilities privately. Do not open a public issue for a
security problem.

- Open a [private security advisory](https://github.com/jakyeamos/agent-eval-contract/security/advisories/new) on GitHub, or
- email the maintainer at jakye.amos@gmail.com

Include a description, affected version, and reproduction steps. You will get an
acknowledgement, and a fix or mitigation timeline once the report is triaged.

## Design notes relevant to security

- **No dynamic code execution in validation paths.** Validation and
  normalization use Pydantic models and plain data transforms; the package never
  `eval`s, `exec`s, imports, or otherwise executes record content.
- **Strict records.** Public models reject unknown top-level fields, so
  malformed or unexpected input fails fast instead of propagating.
- **Minimal dependencies.** The only runtime dependency is Pydantic (`>=2,<3`).

## Supply chain

- GitHub Actions come from trusted publishers (`actions/`, `astral-sh/`,
  `pypa/`, `softprops/`) pinned to reviewed major versions.
- Releases are published to PyPI via [trusted publishing](https://docs.pypi.org/trusted-publishers/)
  (OIDC), so no long-lived PyPI token is stored in the repository.
- The package ships a `py.typed` marker and no compiled extensions.
