# SPACX roadmap

Platform code: **SPACX** · Proposed / expected listing symbol: **SPCX** (Space Exploration Technologies Corp.; pending Form 424B4 and first trading confirmation — see [LISTING_STATUS.md](./LISTING_STATUS.md))

## Workstreams

### 1. SEC evidence — Phase 1 (`workstreams/sec-evidence-phase1/`)

**Status:** Complete (2026-06-04 audit pass with exceptions)

- Structured tables `00`–`04` from Form S-1 / S-1/A only
- Tracks A–D audit workpapers under `audit/`
- Cached primary HTML (`s1*.htm`) for reproducibility
- **Blocked for Phase 2:** final Form 424B4 pricing prospectus and listing date

**Entry:** [00-phase1-summary.md](../workstreams/sec-evidence-phase1/00-phase1-summary.md) · **Synthesis:** [audit/00-integrated-audit-opinion.md](../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)

### 2. AI-native intelligence plugin (`plugin/`)

**Status:** V0 scaffold (runtime / EDGAR poll next)

- Plugin id `spacx-intelligence` — compliance **level 2** (research, alerts, proposals; no auto execution)
- JSON schemas: evidence, metrics, thesis, risk, action, audit (`plugin/schemas/`)
- Agent API stubs: ingest, evidence, metrics, thesis, risk, alerts (`plugin/api/`)
- Architecture: [ARCHITECTURE.md](./ARCHITECTURE.md) — Data→Evidence→Metrics→Stat→LLM→Risk→Action→Audit
- Web3/RWA **pre-layer** detail: [RWA_WEB3_STRATEGY.md](./RWA_WEB3_STRATEGY.md) · Workstream 3 below
- Parallel: metric registry, statistical models, eight agents (`plugin/metrics/`, `plugin/models/`, `plugin/agents/`)
- Automated diff on new SEC amendments and 10-Q/10-K (Phase 2+)
- Synthesis layers on top of Workstream 1 tables (no replacement of source trace)

#### PHASE2_MARKET_INTELLIGENCE_PLUGIN_V0

- [x] Metrics registry and baselines (`plugin/metrics/registry.yaml`, `baselines.json`, `threshold_engine.py`)
- [x] Seven statistical models (`plugin/models/`, [MODELS.md](./MODELS.md))
- [x] Phase 2 quality tables (`workstreams/sec-evidence-phase2/`)
- [x] Architecture and agent docs ([ARCHITECTURE.md](./ARCHITECTURE.md), [AGENTS.md](./AGENTS.md))
- [ ] Runtime worker, EDGAR poll, and live metric ingestion (next)


### 3. Web3 / RWA pre-layer (预埋)

**Status:** Planned / pre-layer — monitor and evidence only (no auto on-chain execution)

**Strategy:** [RWA_WEB3_STRATEGY.md](./RWA_WEB3_STRATEGY.md)

| Phase | Name | Deliverables | Compliance |
|-------|------|--------------|------------|
| **W1** | Evidence hash + chain state monitor | SHA-256 manifests for `EvidencePacket` / artifacts; stablecoin + tokenized treasury watch surfaces; `OnchainRWAAgent` schedules (T0) | Level 2 — no trading |
| **W2** | RWA risk scoring engine | Beyond-TVL dimensions (redemption SLA, attestation freshness, oracle divergence, legal wrapper metadata); feeds risk state / thesis appendix | Level 2 — scores only |
| **W3** | Settlement abstraction | Interfaces for programmable settlement *observation* (Agorá/DTCC-style rails); entitlement parity checks vs DTC/NYSE pilots — no order routing | Level 2–3 |
| **W4** | Policy-bound wallet | Gated, **manual-approval** wallet connect for research reconciliation only; jurisdiction + custody policy pack | Level 4+ human gate |

**Constitutional rules (agents):** tokenized ownership ≠ liquid market; chain data cannot promote to Grade A without SEC-primary evidence.

**Not in pre-layer:** main trading layer, auto swaps/bridges, production custody, TVL-as-KPI.

### 4. Trading workflows

**Status:** Planned

- Research-only pipelines: signals, sizing frameworks, execution assumptions
- Explicit separation from production trading keys and live orders
- Depends on Workstream 2 plugin metric surfaces, Workstream 3 monitors (optional context), and post-listing market data

## Principles

- **Repo identity:** SPACX platform — not "IPO repo"
- **Source hierarchy:** SEC filings > derived tables > commentary
- **No investment advice** in repository artifacts
