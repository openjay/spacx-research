# Contributing to SPACX

Thank you for improving SPACX. This project is **research and education tooling** — not investment advice.

## Before you start

- Read [docs/COMPLIANCE.md](docs/COMPLIANCE.md), [docs/CFA_RESEARCH_POLICY.md](docs/CFA_RESEARCH_POLICY.md), and [docs/LISTING_STATUS.md](docs/LISTING_STATUS.md).
- Use **proposed / expected listing symbol SPCX** until Form 424B4 and first trading are confirmed.
- Do not commit secrets, API keys, or personal account credentials.

## Development

1. Fork or branch from `main`.
2. Keep changes scoped to one workstream or plugin area when possible.
3. Match existing Markdown and YAML conventions in the target directory.
4. For metric or evidence changes, update `plugin/metrics/registry.yaml` and cite SEC primary sources (Grade A).

## Pull requests

- Describe **what** changed and **why** (evidence gap, audit fix, scaffold feature).
- Link related audit items or issues when applicable.
- Confirm research-only disclaimer remains intact; no buy/sell/hold solicitations.
- Note if compliance level or distribution gates are affected.

## Evidence and citations

- Numeric claims from filings require accession ID, section, and cached HTML path when adding new tables.
- See [docs/DATA_PROVENANCE.md](docs/DATA_PROVENANCE.md) for SEC cache redistribution rules.

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

Report vulnerabilities per [SECURITY.md](SECURITY.md) — do not open public issues for sensitive reports.

## License

By contributing, you agree that your contributions are licensed under the repository [LICENSE](LICENSE) (MIT).
