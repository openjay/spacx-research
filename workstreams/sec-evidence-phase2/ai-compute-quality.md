# AI Compute Quality Table (AI flywheel)

**Asset:** SPCX  
**SEC source:** Form S-1/A #2 (2026-06-03) — Segment Operating Data, Prospectus Summary (Anthropic), MD&A  
**Registry:** `plugin/metrics/registry.yaml` → `flywheels.ai`  
**Baselines:** `plugin/metrics/baselines.json` → `flywheel_ai`

Amounts in **USD millions** unless noted.

---

| Metric | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 | Unit | Watch / flywheel ID |
|--------|---------|---------|---------|---------|---------|------|---------------------|
| **AI revenue** | 818 | 727 | 3,201 | 2,620 | 2,961 | USD M | F_AI01 |
| **AI operating loss** | (2,469) | (936) | (6,355) | (1,561) | (3,973) | USD M | F_AI02 |
| **Op loss / revenue** | **3.02×** | 1.29× | 1.99× | 0.60× | 1.34× | ratio | W07, F_AI03 |
| **AI capex** | 7,723 | 2,567 | 12,727 | 5,633 | 463 | USD M | F_AI04 |
| **Capex / revenue** | **9.44×** | 3.53× | 3.98× | 2.15× | 0.16× | ratio | W08, F_AI05 |
| **Nameplate compute (GW)** | 1.0 | 0.3 | 0.8 | 0.3 | 0.0 | GW | F_AI06 |
| **AI Adj. EBITDA** | (609) | (112) | (1,237) | 347 | 1,222 | USD M | F_AI08 |
| **Anthropic contract run-rate** | **$1.25B/mo** | — | — | — | — | USD/mo | W06, F_AI07 |

*Ratios derived from segment table (`05-master-evidence-tables.md` §2.3–2.4, §2.7).*

---

## Anthropic contract (SEC verified)

| Term | Value |
|------|-------|
| Counterparty | Anthropic PBC |
| Infrastructure | COLOSSUS & COLOSSUS II |
| Scale | ~**325,000** NVIDIA GPUs + CPUs, exabyte storage |
| Payment | **$1.25 billion / month** through **May 2029** |
| Ramp | Reduced fee **May–June 2026** |
| Termination | After **initial 3 months**, either party **90 days' notice** |

**Monitor post-IPO:** recognized revenue vs ramp-adjusted **$1.25B/mo** run-rate (`W06_anthropic_revenue_vs_contract_pct`). F-63 footnote omits dollar quantum — use Prospectus narrative as source of truth.

---

## Thresholds (Phase 2 monitor)

| Signal | Amber | Red |
|--------|-------|-----|
| Anthropic recognition vs contract | **<75%** ramp-adjusted run-rate **2 quarters** | Contract termination **8-K** |
| AI op loss / revenue | **>4.0×** two quarters | — |
| AI capex / revenue | **>8×** two quarters (risk theme 17) | **>10×** two quarters |
| Segment gross margin | Not segment-disclosed in S-1/A #2 | — |

---

*Phase 1 evidence: `02-segment-financials.md` (AI), `audit/C-risk-disclosure-audit.md` §1, §4.*
