# Valuation & External Evidence Layer

**Parallel to SEC evidence — does not override A-tier financials.**

CFA-aligned valuation scaffolding for SPCX. SEC segment revenue, EBITDA, cash, and debt come from `workstreams/sec-evidence-phase1/audit/05-master-evidence-tables.md` (Form S-1/A #2, A-tier). External models are **C-tier** references only.

## SOTP 4-layer model

| Layer | Segment | Role | SEC FY2025 anchor |
|-------|---------|------|-------------------|
| **Starlink base** | Connectivity | Core cash-generating base | $11,387M rev / $7,168M Adj. EBITDA |
| **Launch option** | Space | Launch cadence + Starship option | $4,086M rev / $653M Adj. EBITDA |
| **AI discounted** | AI | Compute / Anthropic — probability haircut | $3,201M rev / $(1,237)M Adj. EBITDA |
| **Orbital/Mars OTM** | Corporate | Deep OTM optionality | No SEC anchor (D-tier framing) |

## Price anchors (`price_anchors.yaml`)

| Anchor | Price / EV | CFA tier | Notes |
|--------|------------|----------|-------|
| `dcf_conservative_anchor` | ~$60/sh (~$780B) | **C** | Morningstar via Reuters; **not** a verified SPACX model |
| `ipo_issue_anchor` | $135/sh (~$1.75T) | **A** | SEC S-1/A #2 expected IPO price |
| `fomo_trading_band` | $185–300 | Observation | Sentiment only; no fundamental claim |

## Scenario bands (`scenario_bands.yaml`)

- **Conservative:** $500–800B EV
- **Base:** $800B–1.2T EV
- **Bull:** $1.2–1.7T EV
- **IPO bull:** $1.75T+ (S-1/A #2 terms)

## Modules

| File | Purpose |
|------|---------|
| `sotp_calculator.py` | Segment weights from SEC FY2025; `ai_probability_haircut` parameter |
| `implied_multiples.py` | EV/Revenue, EV/Adj. EBITDA at arbitrary price |
| `reverse_dcf.py` | Back-solve CAGR/margin for target EV; New Constructs stress as `EXTERNAL_REFERENCE` |
| `risk_gate.py` | `OBSERVE_ONLY` when price > 2× DCF anchor without 424B4 + earnings |
| `sec_fy25.py` | A-tier SEC inputs (single import point) |

## Agent

`ValuationAnalystAgent` reads SEC A-tier + external C-tier; **forbidden:** auto trade, override SEC numbers.

## Registry metrics

`IMPLIED_MARKET_CAP_USD`, `EV_TO_REVENUE_FY25`, `EV_TO_ADJ_EBITDA_FY25`, `PRICE_VS_DCF_ANCHOR_PCT` — see `plugin/metrics/registry.yaml`.
