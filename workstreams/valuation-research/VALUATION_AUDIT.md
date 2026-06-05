# Valuation Audit — External vs SEC Anchors

**Date:** 2026-06-05  
**Auditor role:** Valuation & External Evidence Layer (CFA discipline)  
**SEC SSOT:** `workstreams/sec-evidence-phase1/audit/05-master-evidence-tables.md`

---

## 1. Tier classification

| Claim type | Min grade | This workstream |
|------------|-----------|-----------------|
| Segment revenue / EBITDA | A | SEC Table 2 only |
| Cash / debt | A | SEC Table 3.2 |
| IPO price / share count | A | SEC Table 1 (pending 424B4) |
| Third-party DCF / fair value | C | `ExternalResearchPacket` |
| Sentiment trading band | Observation | `fomo_trading_band` — no fundamental claim |

---

## 2. Anchor conflict matrix

| Anchor | EV (approx.) | vs SEC IPO ($1.75T) | Flags |
|--------|--------------|---------------------|-------|
| Morningstar / Reuters | $780B | −55% | `EXTERNAL_DCF_NOT_VERIFIED` |
| New Constructs | $500B | −71% | `EXTERNAL_DCF_NOT_VERIFIED` |
| S-1/A #2 IPO | $1.75T | baseline | `FINAL_PROSPECTUS_PENDING` |
| FOMO band ($185–300) | $2.4–3.9T | +37–123% | `NO_FUNDAMENTAL_BASIS` |

---

## 3. Reverse DCF stress (illustrative)

Using FY2025 consolidated revenue **$18,674M** (A-tier):

| Target EV | Required 10y revenue CAGR (illustrative) | Tier |
|-----------|----------------------------------------|------|
| $500B | ~28%+ | C — New Constructs reference |
| $780B | ~22%+ | C — Morningstar reference |
| $1,750B | ~35%+ | A — IPO issue anchor |

*Margin and terminal multiple assumptions documented in `plugin/valuation/reverse_dcf.py`.*

---

## 4. Action gate

When observed price **> 2×** `dcf_conservative_anchor` (~$120/sh) while `FINAL_PROSPECTUS_PENDING` and `FIRST_EARNINGS_PENDING` are active → default `OBSERVE_ONLY` (`plugin/valuation/risk_gate.py`, `plugin/api/risk.py`).

---

## 5. Open items

- [ ] Reconcile EV math when 424B4 confirms final share count and net proceeds
- [ ] Ingest first 10-Q for post-IPO cash/debt refresh
- [ ] Rebuild external packets when Morningstar / New Constructs update models
