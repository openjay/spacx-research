# Track A — Segment Financial Audit

**Auditor:** Track A (ISA/PCAOB-style trace + CFA Level II analysis)  
**Primary source:** Form S-1/A Amendment No. 2 (`s1a2-main.htm`, filed 2026-06-03)  
**Cross-check filings:** `s1-original.htm` (2026-05-20), `s1a1-main.htm` (2026-06-01) — segment KPI numbers unchanged across all three versions  
**Workpaper reviewed:** `02-segment-financials.md`, `00-phase1-summary.md`  
**Date:** 2026-06-04

---

## Executive Summary

| Metric | Result |
|--------|--------|
| **Errors in `02-segment-financials.md`** | **4** (1 material, 3 immaterial) |
| **Numeric mismatches vs. consolidated (>1%)** | **0** — segment revenue and Segment Adjusted EBITDA sum to consolidated for every period where segment revenue is disclosed |
| **Segment KPI table vs. Notes gap** | Segment **revenue** for FY2024/FY2023 and Q1 2025 appears in **Notes to Consolidated Financial Statements** (revenue disaggregation), not in the Prospectus Summary KPI table |
| **Amendment drift** | No segment financial number changes detected across S-1 → S-1/A#1 → S-1/A#2 |

**Top 3 corrections:** (1) FY2024/FY2023 segment revenue is disclosed in Note 3 — not “not disclosed”; (2) add Q1 2025 segment revenue from the same note; (3) expand consolidated reference table to Q1 2025, FY2024, FY2023.

---

## Assertion Framework

| Assertion | Scope | Result |
|-----------|-------|--------|
| **Occurrence** | Every number in corrected tables traced to `s1a2-main.htm` | Pass |
| **Completeness** | All segment periods in filing captured; prior-year revenue gap in workpaper flagged | **Fail** — workpaper omits Note-disclosed revenue |
| **Accuracy** | Recalculation vs. primary source | Pass — no numeric errors in disclosed figures |
| **Cutoff** | Q1 2026 = 3 mo. ended Mar 31, 2026; FY = calendar year | Pass |
| **Classification** | Space / Connectivity / AI mapping consistent with filing definitions | Pass |
| **Presentation** | Units ($ millions), derived capex totals labeled | Minor — capex totals are sums, not a filing line item |

**Materiality (qualitative):** Omitting FY2024/FY2023 segment revenue impairs YoY margin and growth analysis (Connectivity +49.8% revenue growth, AI capex/revenue 397.6% in FY2025) — classified **material** for research completeness.

---

## 1. Corrected Segment Tables (USD millions)

**Sources:**
- *Prospectus Summary* — segment revenue (Q1 2026, FY2025 only), capex, Starship R&D
- *Segment Operating and Financial Data (unaudited)* — op income, Segment Adj. EBITDA, operational KPIs (p. 26–27, pre–Risk Factors)
- *MD&A — Non-GAAP Financial Measures* — Segment Adj. EBITDA reconciliation (pp. 119–121)
- *Notes to Consolidated Financial Statements — Revenue disaggregated by type and segment* — segment revenue Q1 2025, FY2024, FY2023 (F-23 annual; F-72 interim)

### 1.1 Segment Revenue

| Segment | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|---------|---------|---------|---------|---------|---------|
| **Space** | 619 | 865 | 4,086 | 3,796 | 3,557 |
| **Connectivity** | 3,257 | 2,475 | 11,387 | 7,599 | 3,869 |
| **AI** | 818 | 727 | 3,201 | 2,620 | 2,961 |
| **Consolidated** | **4,694** | **4,067** | **18,674** | **14,015** | **10,387** |
| **Segment sum = Consolidated** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Variance** | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

*Q1 2026 / FY2025 segment revenue: Prospectus Summary. Q1 2025 / FY2024 / FY2023 segment revenue: Note 3 revenue disaggregation (not in KPI table).*

### 1.2 Income (Loss) from Operations

| Segment | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|---------|---------|---------|---------|---------|---------|
| **Space** | (662) | (70) | (657) | 21 | (1) |
| **Connectivity** | 1,188 | 1,033 | 4,423 | 2,006 | 469 |
| **AI** | (2,469) | (936) | (6,355) | (1,561) | (3,973) |
| **Total reportable segments** | **(1,943)** | **27** | **(2,589)** | **466** | **(3,505)** |
| **Consolidated** | **(1,943)** | **27** | **(2,589)** | **466** | **(3,505)** |
| **Variance** | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

*Source: Segment Operating and Financial Data; MD&A Segment Adj. EBITDA reconciliation; Consolidated Statements of Operations (F-5, F-64).*

### 1.3 Segment Adjusted EBITDA

| Segment | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|---------|---------|---------|---------|---------|---------|
| **Space** | (351) | 224 | 653 | 1,154 | 997 |
| **Connectivity** | 2,087 | 1,618 | 7,168 | 3,849 | 1,602 |
| **AI** | (609) | (112) | (1,237) | 347 | 1,222 |
| **Total reportable segments** | **1,127** | **1,730** | **6,584** | **5,350** | **3,821** |
| **Consolidated Adjusted EBITDA** | **1,127** | **1,730** | **6,584** | **5,350** | **3,821** |
| **Variance** | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

*Source: MD&A — Non-GAAP Financial Measures, reconciliation tables (pp. 119–121).*

### 1.4 Capital Expenditures (by segment)

| Segment | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|---------|---------|---------|---------|---------|---------|
| **Space** | 1,052 | 759 | 3,832 | 2,032 | 1,497 |
| **Connectivity** | 1,332 | 814 | 4,178 | 3,498 | 2,455 |
| **AI** | 7,723 | 2,567 | 12,727 | 5,633 | 463 |
| **Total (derived sum)** | **10,107** | **4,140** | **20,737** | **11,163** | **4,415** |

*Source: Prospectus Summary (Q1 2026, FY2025); MD&A capital expenditures narrative (Space / Connectivity / AI subsections). **Total row is auditor-derived** — filing does not present a consolidated capex total line.*

### 1.5 Operational KPIs (Segment Operating and Financial Data)

| KPI | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|-----|---------|---------|---------|---------|---------|
| Space — mass to orbit (metric tons) | 556 | 450 | 2,213 | 1,699 | 1,210 |
| Space — launches | 40 | 38 | 170 | 138 | 98 |
| Connectivity — Starlink subscribers (M) | 10.3 | 5.0 | 8.9 | 4.4 | 2.3 |
| Connectivity — Starlink ARPU ($/mo) | 66 | 86 | 81 | 91 | 99 |
| AI — nameplate compute draw (GW) | 1 | 0.3 | 0.8 | 0.3 | 0 |

*Space Starship R&D (Prospectus Summary, not in KPI table): Q1 2026 $930; FY2025 $3,004.*

---

## 2. Consolidated Reference (expanded)

| Period | Revenue | Loss from operations | Adjusted EBITDA | Net income (loss) |
|--------|---------|----------------------|-----------------|-------------------|
| Q1 2026 | 4,694 | (1,943) | 1,127 | (4,276) |
| Q1 2025 | 4,067 | 27 | 1,730 | (528) |
| FY 2025 | 18,674 | (2,589) | 6,584 | (4,937) |
| FY 2024 | 14,015 | 466 | 5,350 | 791 |
| FY 2023 | 10,387 | (3,505) | 3,821 | (4,628) |

*Sources: Consolidated Statements of Operations (F-5, F-64); MD&A Non-GAAP reconciliation (p. 119).*

---

## 3. Adjusted EBITDA — Definition & Add-backs

### 3.1 Consolidated Adjusted EBITDA

**Definition** (*MD&A — Non-GAAP Financial Measures*, p. 119):

> Adjusted EBITDA is defined as net income (loss) excluding (i) depreciation and amortization, (ii) share-based compensation, (iii) impairment, (iv) restructuring charges, (v) interest expense, (vi) interest income, (vii) other income (expense), net and (viii) provision for income taxes.

**Add-backs to net income (loss) — Q1 2026 / FY2025 ($ millions):**

| Add-back | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|----------|---------|---------|---------|---------|---------|
| Depreciation & amortization | 2,442 | 1,443 | 6,701 | 3,824 | 2,635 |
| Share-based compensation | 639 | 232 | 1,947 | 784 | 679 |
| Restructuring charges | (11) | 4 | 487 | 213 | 237 |
| Impairments | — | 24 | 38 | 63 | 3,775 |
| Interest expense | 664 | 447 | 1,945 | 1,580 | 1,693 |
| Interest income | (213) | (117) | (492) | (371) | (249) |
| Other (income) expense, net | 1,876 | 211 | 177 | (985) | 42 |
| Provision for (benefit from) income taxes | 6 | 14 | 718 | (549) | (363) |
| **Adjusted EBITDA** | **1,127** | **1,730** | **6,584** | **5,350** | **3,821** |

**CFA note:** Q1 2026 other expense add-back ($1,876M) is the dominant bridge item — largely drives consolidated Adj. EBITDA positive despite $(1,943)M operating loss. Review *Other expense, net* composition before using Adj. EBITDA as cash-proxy.

### 3.2 Segment Adjusted EBITDA

**Definition** (*MD&A — Non-GAAP Financial Measures*, p. 119):

> Segment Adjusted EBITDA is defined as segment income (loss) from operations excluding (i) depreciation and amortization, (ii) share-based compensation, (iii) restructuring charges, and (iv) impairment.

**Segment add-backs — Q1 2026 ($ millions):**

| Add-back | Space | Connectivity | AI | Total |
|----------|-------|--------------|-----|-------|
| D&A | 166 | 783 | 1,493 | 2,442 |
| SBC | 145 | 116 | 378 | 639 |
| Restructuring | — | — | (11) | (11) |
| **Segment Adj. EBITDA** | **(351)** | **2,087** | **(609)** | **1,127** |

*Segment reconciliation does not add interest or tax — segment measure stops at operating level + D&A/SBC/restructuring/impairment.*

---

## 4. CFA Ratios (auditor-calculated)

### 4.1 Segment Adjusted EBITDA Margin

| Segment | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|---------|---------|---------|---------|---------|---------|
| Space | -56.7% | 25.9% | 16.0% | 30.4% | 28.0% |
| Connectivity | **64.1%** | 65.4% | **62.9%** | 50.7% | 41.4% |
| AI | -74.4% | -15.4% | -38.6% | 13.2% | 41.3% |

### 4.2 Segment Operating Margin

| Segment | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|---------|---------|---------|---------|---------|---------|
| Space | -106.9% | -8.1% | -16.1% | 0.6% | ~0.0% |
| Connectivity | 36.5% | 41.7% | 38.8% | 26.4% | 12.1% |
| AI | -301.8% | -128.7% | -198.5% | -59.6% | -134.2% |

### 4.3 Capex / Revenue

| Segment | Q1 2026 | Q1 2025 | FY 2025 | FY 2024 | FY 2023 |
|---------|---------|---------|---------|---------|---------|
| Space | 170.0% | 87.7% | 93.8% | 53.5% | 42.1% |
| Connectivity | 40.9% | 32.9% | 36.7% | 46.0% | 63.5% |
| AI | **944.1%** | 353.1% | **397.6%** | 215.0% | 15.6% |

### 4.4 YoY Revenue Growth (FY2025 vs FY2024)

| Segment | Growth | SEC cited (Connectivity only) |
|---------|--------|-------------------------------|
| Space | +7.6% | — |
| Connectivity | **+49.8%** | Prospectus Summary ✓ |
| AI | +22.2% | — |
| Consolidated | +33.3% | — |

### 4.5 YoY Segment Adjusted EBITDA Growth (FY2025 vs FY2024)

| Segment | Growth | SEC cited |
|---------|--------|-----------|
| Space | -43.4% | — |
| Connectivity | **+86.2%** | Prospectus Summary ✓ |
| AI | -456.5% | — |
| Consolidated | +23.1% | — |

### 4.6 Capex vs D&A (FY2025, segment)

| Segment | Capex | D&A (from recon) | Capex/D&A |
|---------|-------|------------------|-----------|
| Space | 3,832 | 757 | 5.1× |
| Connectivity | 4,178 | 2,376 | 1.8× |
| AI | 12,727 | 3,568 | 3.6× |

*D&A from Segment Adj. EBITDA reconciliation; capex from MD&A.*

---

## 5. Reconciliation to Consolidated — Detail

### 5.1 Revenue (assertion: accuracy)

| Period | Σ Segment Revenue | Consolidated Revenue | Δ $ | Δ % |
|--------|-------------------|----------------------|-----|-----|
| Q1 2026 | 4,694 | 4,694 | 0 | 0.0% |
| Q1 2025 | 4,067 | 4,067 | 0 | 0.0% |
| FY 2025 | 18,674 | 18,674 | 0 | 0.0% |
| FY 2024 | 14,015 | 14,015 | 0 | 0.0% |
| FY 2023 | 10,387 | 10,387 | 0 | 0.0% |

**No inter-segment revenue elimination disclosed** — segments sum exactly to consolidated total per Note 3 disaggregation.

### 5.2 Segment Adjusted EBITDA vs Consolidated (assertion: accuracy)

All periods: segment sum = consolidated Adjusted EBITDA (0.0% variance). Confirms reportable-segment coverage equals consolidated non-GAAP metric.

### 5.3 Operating income (assertion: classification)

Reportable-segment operating income equals consolidated operating income for all five periods — **no corporate/unallocated operating loss line** in reconciliation tables.

---

## 6. Findings on `02-segment-financials.md`

| ID | Severity | Assertion | Finding | Correction | SEC citation |
|----|----------|-----------|---------|------------|--------------|
| **A-001** | **Material** | Completeness | FY2024 and FY2023 segment **revenue** marked "**not disclosed**" | Populate: Space $3,796 / $3,557; Connectivity $7,599 / $3,869; AI $2,620 / $2,961 | *Notes to Consolidated Financial Statements — Revenue disaggregated by type and segment* (F-23) |
| **A-002** | Immaterial | Completeness | Q1 2025 segment revenue omitted (only "not in KPI table") | Add: Space $865; Connectivity $2,475; AI $727 | Same note, interim (F-72) |
| **A-003** | Immaterial | Completeness | Consolidated reference table stops at Q1 2026 / FY2025 | Add Q1 2025, FY2024, FY2023 per §2 above | *Consolidated Statements of Operations* (F-5, F-64); *MD&A Non-GAAP* (p. 119) |
| **A-004** | Immaterial | Presentation | AI nameplate compute Q1 2026 shown as "1.0" GW | Filing KPI table shows **1** GW (integer) | *Segment Operating and Financial Data* |

**Verified correct (no change required):**
- All numeric values present in workpaper match primary source
- Connectivity FY2025 YoY growth rates (49.8% / 120.4% / 86.2%) — accurate
- Capex by segment all periods — accurate
- Total capex sums — arithmetic correct (derived)
- Anthropic contract ($1.25B/mo through May 2029, ~325K GPUs, 90-day termination) — accurate (*Prospectus Summary / Business*)
- ~9,600 satellites, 164 countries — accurate (*Business*)
- Starship R&D $930M / $3,004M — accurate (*Prospectus Summary*)
- xAI merger Feb 2, 2026; X Holdings Mar 28, 2025 — accurate (*Prospectus Summary*)

---

## 7. Disclosure Gaps (filing-level, not workpaper errors)

| Gap | Impact |
|-----|--------|
| Segment revenue **not in Prospectus Summary KPI table** for Q1 2025, FY2024, FY2023 | Must use Note 3 disaggregation — easy to miss |
| Segment **gross margin** not disclosed by segment | Cannot compute from filing |
| Segment **FCF** not reported | Adj. EBITDA only; consolidated cash flow at entity level |
| **Unaudited** Q1 2026 interim + **retrospective** presentation for xAI/X common-control combinations | Comparability risk — MD&A states retrospective combination |
| **Pro forma** shareholder table (*The following table summarizes… adjusted pro forma*) — not segment P&L | Distinct from segment actuals |
| **Customer concentration**: Customer A = 20.9% / 24.2% / 25.2% of consolidated revenue (FY2025–2023); revenue across all three segments | Not in workpaper |
| Q1 2026 **impairment $0** vs Q1 2025 **$24M** (Space) | Segment recon footnote |
| AI FY2023 Segment Adj. EBITDA **$1,222M** includes **$3,775M impairment add-back** at consolidated level — segment AI op loss $(3,973)M | Distorts YoY AI EBITDA comparability |

---

## 8. Amendment Stability Check

Segment KPI table values (op income, Segment Adj. EBITDA, operational metrics) and Prospectus Summary segment revenue/capex figures are **identical** in `s1-original.htm`, `s1a1-main.htm`, and `s1a2-main.htm`. No restatement detected in Phase 1 cache.

---

## 9. Auditor Conclusion

**Segment financial data in the filing is internally consistent.** Revenue and Segment Adjusted EBITDA reconcile to consolidated statements with **zero variance** across all five periods. The primary workpaper deficiency is **mislabeling Note-disclosed segment revenue as "not disclosed"** for FY2024/FY2023 — a material completeness error for CFA-style segment analysis. No fabricated or arithmetically wrong numbers were found in disclosed fields.

**Recommended action:** Update `02-segment-financials.md` using corrected tables in §1 and expanded consolidated reference in §2; retain footnote that KPI table omits historical segment revenue while Note 3 provides it.

---

*End of Track A audit workpaper.*
