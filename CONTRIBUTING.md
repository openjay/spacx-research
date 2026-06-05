# Contributing to SPACX

Thank you for improving SPACX. This project is **research and education tooling** — not investment advice.

## AI-native workflow

SPACX is built for **agent-assisted** development. Humans gate **P0 nodes only**; agents own routine P1 commits when CI passes.

| Tier | Gate owner | Examples |
|------|------------|----------|
| **P0 — human** | Maintainer | 424B4 / listing status, compliance level changes, external distribution, SECURITY triage, pricing-day anchors |
| **P1 — agent** | Cursor / CI agents | `THIRD_PARTY_NOTICES`, `DEPENDENCY_LICENSES`, tests, registry YAML, evidence table drafts, docs |

**Agents may commit** P1 changes directly (feature branches or maintainer-approved automation). Every commit must:

- Pass `pytest` and `compileall` (see CI)
- Preserve research-only disclaimers — no buy/sell/hold solicitations
- Not touch P0-gated files without explicit human approval (`docs/LISTING_STATUS.md`, compliance level bumps, published audit opinions)

P0/P1 definitions align with [`docs/AGENTS.md`](docs/AGENTS.md) and [`docs/OPEN_SOURCE_READINESS.md`](docs/OPEN_SOURCE_READINESS.md).

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
- Bilingual financial terms must follow [docs/TERMINOLOGY.md](docs/TERMINOLOGY.md). Do not mechanically translate terms such as `greenshoe`; use **超额配售选择权（greenshoe）**.

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

Report vulnerabilities per [SECURITY.md](SECURITY.md) — do not open public issues for sensitive reports.

## Dependency licenses

Direct dependencies are listed in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The full transitive table lives in [`docs/DEPENDENCY_LICENSES.md`](docs/DEPENDENCY_LICENSES.md).

Regenerate after changing `pyproject.toml` dependencies:

```bash
pip install -e ".[dev]" pip-licenses
pip-licenses --format=markdown --with-urls > docs/DEPENDENCY_LICENSES.md
```

CI runs an **optional** `pip-licenses` step (non-blocking) and warns if the committed file drifts. Commit the updated markdown with your dependency change.

## License

By contributing, you agree that your contributions are licensed under the repository [LICENSE](LICENSE) (MIT).
