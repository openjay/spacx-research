# Starship Milestones Table (Space flywheel)

**Asset:** SPCX  
**SEC source:** Form S-1/A #2 (2026-06-03) — Segment Operating Data, Business, Prospectus Summary  
**Registry:** `plugin/metrics/registry.yaml` → `flywheels.starship`  
**Baselines:** `plugin/metrics/baselines.json` → `flywheel_starship`

Amounts in **USD millions** unless noted.

---

| Metric | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 | Unit | Watch / flywheel ID |
|--------|---------|---------|---------|---------|---------|------|---------------------|
| **Launches (count)** | 40 | 38 | 170 | 138 | 98 | # | F_ST01, F_ST06 |
| **Mass to orbit** | 556 | 450 | 2,213 | 1,699 | 1,210 | metric tons | F_ST02 |
| **Starship R&D spend** | 930 | — | 3,004 | — | — | USD M | F_ST03 |
| **Space revenue** | 619 | 865 | 4,086 | 3,796 | 3,557 | USD M | F_ST05 |
| **Space op income (loss)** | (662) | (70) | (657) | 21 | (1) | USD M | — |
| **Space Adj. EBITDA** | (351) | 224 | 653 | 1,154 | 997 | USD M | — |
| **Starship payload to orbit** | Target **2H 2026** | — | — | — | — | milestone | W09, F_ST04 |

---

## Narrative milestones (SEC text)

| Milestone | Timing / fact |
|-----------|----------------|
| Starship payload delivery to orbit | Expected **2H 2026** |
| Flight-proven Falcon missions | >**540** historically |
| Falcon 9 LEO capacity | ~**23** metric tons |
| Falcon Heavy | ~**64** metric tons |
| Starlink V3 deployment vehicle | Starship; up to **60** satellites per launch |

---

## Thresholds (Phase 2 monitor)

| Signal | Amber | Red |
|--------|-------|-----|
| Launch cadence (FY run-rate) | **<150**/yr | — |
| Starship payload-to-orbit | — | None by **YE 2026** |
| Starship commercial sat deploys (V3 gen) | — | **0** by **H2 2027** (risk theme 3) |
| FAA license delay | — | **>6 months** (risk theme 4) |

*Watch metric #9 (`W09_starship_payload_orbit_milestone`) is the primary IPO-era gate for this table.*

---

*Phase 1 evidence: `02-segment-financials.md` (Space), `audit/C-risk-disclosure-audit.md` themes 1–4, `05-master-evidence-tables.md` Table 2.4.*
