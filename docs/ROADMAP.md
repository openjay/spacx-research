# SPACX roadmap

Platform code: **SPACX** · Listed equity: **SPCX** (Space Exploration Technologies Corp.)

## Workstreams

### 1. SEC evidence — Phase 1 (`workstreams/sec-evidence-phase1/`)

**Status:** Complete (2026-06-04 audit pass with exceptions)

- Structured tables `00`–`04` from Form S-1 / S-1/A only
- Tracks A–D audit workpapers under `audit/`
- Cached primary HTML (`s1*.htm`) for reproducibility
- **Blocked for Phase 2:** final Form 424B4 pricing prospectus and listing date

**Entry:** [00-phase1-summary.md](../workstreams/sec-evidence-phase1/00-phase1-summary.md) · **Synthesis:** [audit/00-integrated-audit-opinion.md](../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)

### 2. AI-native analysis

**Status:** Planned

- Evidence schemas agents can query without re-parsing raw HTML
- Automated diff on new SEC amendments and 10-Q/10-K
- Synthesis layers on top of Workstream 1 tables (no replacement of source trace)

### 3. Trading workflows

**Status:** Planned

- Research-only pipelines: signals, sizing frameworks, execution assumptions
- Explicit separation from production trading keys and live orders
- Depends on Workstream 2 metric surfaces and post-listing market data

## Principles

- **Repo identity:** SPACX platform — not "IPO repo"
- **Source hierarchy:** SEC filings > derived tables > commentary
- **No investment advice** in repository artifacts
