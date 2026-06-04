# SpaceX IPO Research (SEC S-1 / S-1A)

Standalone research workbook built **only from SEC EDGAR filings** (Phase 1 structured tables + Tracks A–D audit workpapers). Not affiliated with SpaceX or the SEC.

## Disclaimer

This repository is for **research and education**. It is **not investment advice**, not a solicitation, and not an audit opinion on SpaceX. Verify all figures against current SEC filings before any decision.

**Integrated audit synthesis:** [audit/00-integrated-audit-opinion.md](audit/00-integrated-audit-opinion.md)

## Filings used

| Filing | Date | EDGAR index |
|--------|------|-------------|
| S-1 | 2026-05-20 | https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/ |
| S-1/A #1 | 2026-06-01 | https://www.sec.gov/Archives/edgar/data/1181412/000162828026039276/ |
| S-1/A #2 | 2026-06-03 | https://www.sec.gov/Archives/edgar/data/1181412/000162828026040364/ |

Primary HTML (S-1/A #2): https://www.sec.gov/Archives/edgar/data/1181412/000162828026040364/spaceexplorationtechnologib.htm

## Repository layout

| Path | Contents |
|------|----------|
| `00-phase1-summary.md` | Phase 1 conclusion + watch metrics |
| `01-offering-terms.md` | Offering / fee / directed-share table |
| `02-segment-financials.md` | Segment financials (Note F-23 trace) |
| `03-risk-metrics-map.md` | Risk themes → metrics map |
| `04-s1-amendment-diff.md` | S-1 vs S-1/A amendment diff |
| `s1-original.htm`, `s1a1-main.htm`, `s1a2-main.htm` | Cached filing HTML (reproducibility) |
| `audit/` | Tracks A–D workpapers (see below) |

## Audit workpapers (`audit/`)

| File | Track |
|------|-------|
| [00-integrated-audit-opinion.md](audit/00-integrated-audit-opinion.md) | **D** — synthesis |
| [05-master-evidence-tables.md](audit/05-master-evidence-tables.md) | **D** — corrected master tables |
| [A-segment-financial-audit.md](audit/A-segment-financial-audit.md) | A — segment trace + ratios |
| [A-segment-data-corrections.csv](audit/A-segment-data-corrections.csv) | A — correction register |
| [B-offering-governance-audit.md](audit/B-offering-governance-audit.md) | B — offering math, cap table |
| [B-lock-up-schedule.md](audit/B-lock-up-schedule.md) | B — lock-up timeline |
| [C-risk-disclosure-audit.md](audit/C-risk-disclosure-audit.md) | C — risk disclosure audit |
| [C-gap-register.md](audit/C-gap-register.md) | C — pre-424B4 gaps |

**Track D (2026-06-04):** Pass with exceptions — six master-table corrections; Phase 2 blocked on 424B4 and prospectus date. Details in the [integrated opinion](audit/00-integrated-audit-opinion.md).

## License

MIT — see [LICENSE](LICENSE).
