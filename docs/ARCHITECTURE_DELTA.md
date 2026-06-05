# Architecture Delta — Valuation & External Evidence Layer

**Status:** Approved direction (2026-06-05 CFA audit)  
**Trigger:** [VALUATION_AUDIT.md](./VALUATION_AUDIT.md)  
**Verdict:** **Partial re-architecture** — additive layer; SEC evidence unchanged  
**Compliance:** Level 2 — no auto-trading; ValuationAnalystAgent read-only

---

## 1. Summary

SPACX adds a **parallel valuation lane** that ingests C-tier external research (Morningstar, New Constructs, underwriter scenarios) without mutating A-tier SEC metrics. The existing stack remains:

```text
Data → Evidence → Metrics → Statistical → LLM → Risk → Action → Audit
```

**New parallel branch:**

```text
Data → Evidence (SEC A-D) ──────────────────────────┐
       External Research (C + conflicts) → Valuation ┘→ Metrics → …
```

---

## 2. Layer Stack (Updated)

| Layer | Path | Responsibility | AI may | AI must not |
|-------|------|----------------|--------|-------------|
| **Evidence (SEC)** | `workstreams/sec-evidence-phase1/` | Grade A financial facts | Extract claims | Promote C-tier to A |
| **Valuation (NEW)** | `plugin/valuation/` | SOTP, reverse DCF, scenario bands, price anchors | Compute implied multiples | Override SEC share count or segment revenue |
| **External research (NEW)** | `workstreams/valuation-research/` | Third-party models, assumptions tables | Index and tag sources | Treat Morningstar $60 as fact |
| **Metrics** | `plugin/metrics/registry.yaml` | Formulas + SEC baselines | Add valuation-derived **observation** metrics | Change SEC-sourced baselines |
| **Statistical** | `plugin/models/` | `VALUATION_REASONABLE` posterior | Update P(thesis) from sealed packets | Place orders |
| **Agents** | `plugin/agents/ValuationAnalystAgent/` | Read-only synthesis | Compare anchors vs price | Auto-trade; override SEC |

---

## 3. New Directory: `plugin/valuation/`

| File | Purpose |
|------|---------|
| `README.md` | SOTP 4-layer model: (1) Starlink base, (2) Launch/Starship option, (3) AI probability-discounted, (4) Orbital/Mars OTM — EN + 中文 |
| `price_anchors.yaml` | Three anchors with CFA labels (see §4) |
| `scenario_bands.yaml` | Conservative / base / bull / ipo_bull / sentiment_only bands |
| `reverse_dcf.py` | Given target EV, back-solve required revenue CAGR and NOPAT margin; `EXTERNAL_REFERENCE` tags |
| `sotp_calculator.py` | Segment weights from SEC FY2025 revenue/adj. EBITDA; AI haircut parameter |
| `implied_multiples.py` | EV/Revenue, EV/EBITDA at arbitrary price using SEC cash/debt |
| `__init__.py` | Public API surface for tests and ValuationAnalystAgent |

### 3.1 `price_anchors.yaml` (schema)

```yaml
anchors:
  dcf_conservative_anchor:
    label: "External fair value estimate — NOT verified"
    price_usd_per_share: 60.0          # implied from ~$780B / 13.08B
    enterprise_value_usd_bn: 780.0
    cfa_tier: C
    evidence_grade: C
    source_type: EXTERNAL_REFERENCE
    provider: Morningstar (via Reuters)
    verified_model: false
    conflict_flags: [EXTERNAL_DCF_NOT_VERIFIED, BELOW_IPO_ISSUE_ANCHOR]

  ipo_issue_anchor:
    label: "Expected issue price — SEC filing"
    price_usd_per_share: 135.0
    enterprise_value_usd_bn: 1750.0    # S-1/A framing; per-share math uses SEC 13.08B share count when needed
    cfa_tier: A
    evidence_grade: A
    sec_citation: "S-1/A #2 Cover; Use of Proceeds"
    blocker: FINAL_PROSPECTUS_PENDING
    shares_count: 13075865175

  fomo_trading_band:
    label: "Sentiment observation only — no fundamental claim"
    price_usd_per_share_low: 185.0
    price_usd_per_share_high: 300.0
    cfa_tier: OBSERVATION
    evidence_grade: D
    fundamental_claim: false
    conflict_flags: [NO_FUNDAMENTAL_BASIS, SOCIAL_SENTIMENT_RISK]
```

---

## 4. New Workstream: `workstreams/valuation-research/`

| File | Purpose |
|------|---------|
| `README.md` | Index external models; link to VALUATION_AUDIT.md |
| `assumptions/morningstar-780b.yaml` | C-tier; fair_value_usd, key doubts (AI, orbital) |
| `assumptions/new-constructs-reverse-dcf.yaml` | C-tier; 23% NOPAT, 50% CAGR, $500B bear case |
| `assumptions/goldman-ai-surge-reuters.yaml` | C-tier + `conflict_flags: [LEAD_UNDERWRITER]` |
| `sources/` | Cached excerpts + SHA-256 (optional; no paywall scraping) |

### 4.1 Assumptions table template (per model)

| Field | Required |
|-------|----------|
| `source` | Yes |
| `as_of` | Yes |
| `tier` | C, D, or OBSERVATION |
| `fair_value_usd` | If applicable |
| `implied_price` | Per-share if stated |
| `conflict_flags[]` | e.g. `LEAD_UNDERWRITER`, `COMPENSATED_RESEARCH` |
| `assumptions[]` | Revenue CAGR, margin, WACC, terminal g, segment weights, or qualitative model limits |
| `sec_crosswalk` | A-tier fields used for sanity (share count, FY2025 revenue/EBITDA) |
| `verified_model` | `false` for third-party summaries not rebuilt from primary source |

---

## 5. Schema Extensions

### 5.1 `plugin/schemas/ExternalResearchPacket.json` (NEW)

```json
{
  "required": ["packet_id", "source", "tier", "fair_value_usd", "implied_price", "assumptions", "as_of"],
  "properties": {
    "source": { "type": "string" },
    "tier": { "enum": ["A", "B", "C", "D", "OBSERVATION"] },
    "conflict_flags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "fair_value_usd": { "type": "number" },
    "fair_value_basis": { "enum": ["enterprise_value", "equity_value", "market_cap"] },
    "implied_price": { "type": "number" },
    "assumptions": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" }
    },
    "verified_model": { "type": "boolean" },
    "source_url": { "type": "string", "format": "uri" },
    "projections": { "type": "object" },
    "stress_cases": { "type": "object" },
    "notes": { "type": "string" },
    "sec_crosswalk": {
      "type": "object",
      "properties": {
        "revenue_fy25_musd": { "type": "number" },
        "adj_ebitda_fy25_musd": { "type": "number" },
        "matches_sec": { "type": "boolean" }
      }
    }
  }
}
```

### 5.2 `plugin/schemas/EvidencePacket.json` (EXTEND)

Add optional fields (backward compatible):

| Field | Type | Description |
|-------|------|-------------|
| `source_tier` | enum A/B/C/D | Alias of `confidence`; explicit for valuation lane |
| `conflict_flags` | string[] | CFA Standard VI disclosures |
| `model_assumptions` | object[] | For C-tier valuation claims only; `ExternalResearchPacket` uses `assumptions[]` strings |

**Rule:** Packets with `confidence: A` **must not** carry `model_assumptions` from external DCF.

---

## 6. Thesis: `VALUATION_REASONABLE`

Already in `plugin/schemas/ThesisState.json` and `plugin/models/thesis_keys.py`.

| Field | Value |
|-------|-------|
| `thesis_key` | `VALUATION_REASONABLE` |
| Definition | Offered / trading valuation reasonable vs peers and SOTP anchors |
| Evidence | Sealed A-tier (issue price, financials) + C-tier (external FV) — **C-tier alone cannot push BULL** |
| Default prior | 0.40 (WATCH band) until 424B4 + first trade |
| LR packets | From `price_anchors.yaml` distance metrics |

---

## 7. New Metrics (`plugin/metrics/registry.yaml`)

Add under `valuation_metrics:` (new section):

| metric_id | Formula | Unit | Source priority |
|-----------|---------|------|-----------------|
| `V01_implied_market_cap_usd` | `price × shares_outstanding_a_plus_b` | USD | market_data, S-1/A_2 |
| `V02_enterprise_value_usd` | `market_cap + total_debt − cash` | USD | S-1/A_2, market_data |
| `V03_ev_to_revenue_fy25` | `EV / consolidated_revenue_fy25` | ratio | auditor_calculated, 10-Q |
| `V04_ev_to_adj_ebitda_fy25` | `EV / consolidated_adj_ebitda_fy25` | ratio | auditor_calculated, 10-Q |
| `V05_price_vs_dcf_anchor_pct` | `(price − dcf_anchor_price) / dcf_anchor_price` | ratio | price_anchors.yaml, market_data |
| `V06_price_vs_ipo_anchor_pct` | `(price − 135) / 135` | ratio | 424B4, market_data |

**Baselines (SEC, A-tier):**

- `shares_outstanding_a_plus_b`: **13,075,865,175**
- `consolidated_revenue_fy25`: **18,674** USD millions
- `consolidated_adj_ebitda_fy25`: **6,584** USD millions
- `pro_forma_cash_post_ipo`: **90,305** USD millions
- `bridge_loan`: **20,000** USD millions

---

## 8. New Agent: `ValuationAnalystAgent`

Path: `plugin/agents/ValuationAnalystAgent/`

| Attribute | Value |
|-----------|-------|
| Role | Read-only valuation synthesis |
| Inputs | SEC A-tier tables, `ExternalResearchPacket`, `price_anchors.yaml` |
| Outputs | Metric snapshots, thesis LR packets, narrative draft (LLM) |
| Forbidden | `place_orders`, override SEC numbers, promote C → A |
| Schedule | T2 (hourly) + T* on 424B4 / first trade / >30% day-one pop |

`agent.yaml` capabilities: `metrics.read`, `thesis.update` (valuation thesis only), `report.generate` — **not** `action.propose` with `SIZE_UP`.

---

## 9. Compliance Updates

### 9.1 `docs/CFA_RESEARCH_POLICY.md` — add §3.1

**Third-party research disclaimer** (append to exports):

```text
THIRD-PARTY RESEARCH NOTICE
External fair value estimates (e.g., Morningstar, New Constructs) are Grade C context.
They are NOT verified by SPACX, may rely on opaque assumptions, and do NOT override
SEC EDGAR figures. See workstreams/valuation-research/ and docs/VALUATION_AUDIT.md.
```

### 9.2 Underwriter conflict template (CFA Standard VI)

```text
CONFLICT — UNDERWRITER RESEARCH
Provider: [Goldman Sachs / syndicate member]
Role in offering: Lead underwriter (Form S-1/A #2 cover)
Source: [Reuters / FT] — primary research report NOT independently verified
Use: Scenario framing only; excluded from Grade A metrics and core DCF inputs.
```

### 9.3 `docs/COMPLIANCE.md` — agent table row

| Agent | Hard rule |
|-------|-----------|
| ValuationAnalystAgent | C-tier only for FV; never override SEC; no SIZE_UP proposals |

---

## 10. ActionProposal Gate Logic

Implement in `plugin/valuation/gates.py` (or extend `runtime/risk.py`):

```python
def valuation_action_gate(price: float, anchors: dict, blockers: list[str]) -> str:
    """Returns proposal_type; default OBSERVE_ONLY."""
    if "FINAL_PROSPECTUS_PENDING" in blockers:
        return "OBSERVE_ONLY"
    dcf = anchors["dcf_conservative_anchor"]["price_usd_per_share"]
    if price > 2.0 * dcf:
        return "OBSERVE_ONLY"  # blocked_by: PRICE_ABOVE_DCF_2X
    return "OBSERVE_ONLY"  # V0: never auto SIZE_UP from valuation layer
```

**V0 policy:** Valuation layer **never** emits `PAPER_BUY` or `SIZE_UP`; only tightens `blocked_by` and `risk_state`.

---

## 11. Documentation Updates (follow-on PR)

| File | Change |
|------|--------|
| `docs/ARCHITECTURE.md` | Add valuation lane to mermaid + layer table |
| `docs/ROADMAP.md` | Workstream 5: `valuation-research` |
| `plugin/README.md` | Register `plugin/valuation/` |
| `plugin/manifest.yaml` | `valuation_policy` + `ValuationAnalystAgent` ref |

---

## 12. Implementation Order

| Phase | Deliverable | Depends on |
|-------|-------------|------------|
| **D1** | `price_anchors.yaml`, `scenario_bands.yaml`, `valuation-research/README.md` | This audit |
| **D2** | `reverse_dcf.py`, `sotp_calculator.py`, `implied_multiples.py` | D1 + SEC tables |
| **D3** | `ExternalResearchPacket.json`, EvidencePacket extension | D1 |
| **D4** | Registry metrics V01–V06 | D2 |
| **D5** | `ValuationAnalystAgent` + tests | D3–D4 |
| **D6** | Compliance templates + ARCHITECTURE.md sync | D5 |

---

## 13. Explicit Non-Goals

- Rename repository
- Auto-trading or level ≥4 execution
- Ingest Morningstar model as Grade A
- Replace `workstreams/sec-evidence-phase1/` as SSOT
- Single “fair value” number in thesis dashboard without band + tier labels

---

*Architecture delta approved per CFA valuation audit 2026-06-05.*
