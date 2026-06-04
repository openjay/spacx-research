# Starlink Quality Table (Connectivity flywheel)

**Proposed symbol:** SPCX (pending 424B4 and first trade)  
**SEC source:** Form S-1/A #2 (2026-06-03) — Segment Operating Data, Note 3 revenue, Prospectus Summary  
**Registry:** `plugin/metrics/registry.yaml` → `flywheels.starlink`  
**Baselines:** `plugin/metrics/baselines.json` → `flywheel_starlink`

Amounts in **USD millions** unless noted. Subscriber and ARPU from Segment Operating Data (p. ~27).

---

| Metric | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 | Unit | Watch / flywheel ID |
|--------|---------|---------|---------|---------|---------|------|---------------------|
| **Starlink subscribers** | 10.3 | 5.0 | 8.9 | 4.4 | 2.3 | M | W03, F_SL01 |
| **Starlink ARPU** | $66 | $86 | $81 | $91 | $99 | $/mo | W04, F_SL02 |
| **Connectivity revenue** | 3,257 | 2,475 | 11,387 | 7,599 | 3,869 | USD M | F_SL03 |
| **Connectivity Adj. EBITDA** | 2,087 | 1,618 | 7,168 | 3,849 | 1,602 | USD M | W05, F_SL04 |
| **Connectivity capex** | 1,332 | 814 | 4,178 | 3,498 | 2,455 | USD M | F_SL05 |
| **Adj. EBITDA margin** | **64.1%** | 65.4% | 63.0% | 50.6% | 41.4% | % | F_SL06 |
| **Starlink V3 via Starship** | Target **2H 2026** | — | — | — | — | milestone | F_SL07 |

*Margin Q1 2026 = Adj. EBITDA / revenue (auditor-calculated per `05-master-evidence-tables.md` §2.7).*

---

## Operational context (SEC narrative)

| Item | Disclosure |
|------|------------|
| Satellites in LEO | ~**9,600** (Mar 31, 2026) |
| Markets | **164** countries/territories |
| V3 spec | ~**1 Tbps** downlink each; up to **60** sats per Starship launch |
| V3 deployment | Via Starship expected **2H 2026** |

---

## Thresholds (Phase 2 monitor)

| Signal | Amber | Red |
|--------|-------|-----|
| Subscriber QoQ growth | **<3%** | Negative QoQ |
| ARPU | **<$60** two consecutive quarters | — |
| Connectivity Adj. EBITDA (quarterly) | **<$1.5B** | — |
| V3 / Starship deploy | — | No V3-related milestone progress by **YE 2026** (paired with Starship table) |

*Full machine-readable thresholds: `plugin/metrics/registry.yaml`.*

---

*Phase 1 evidence: `workstreams/sec-evidence-phase1/02-segment-financials.md` (Connectivity), `audit/05-master-evidence-tables.md` Table 2.*
