# Track B — Offering & Governance Audit (Phase 1 Double-Check)

**Auditor:** Track B (CFA-style offering terms, cap table, dilution, governance)  
**Date:** 2026-06-04  
**Primary SEC source:** Form S-1/A Amendment No. 2 (2026-06-03, CIK 0001181412)  
**Compared:** `s1-original.htm` (S-1), `s1a1-main.htm` (S-1/A #1), `s1a2-main.htm` (S-1/A #2)  
**Research cross-check:** `01-offering-terms.md`, `04-s1-amendment-diff.md`

---

## Executive verdict

| Check | Result |
|-------|--------|
| **555,555,555 × $135 gross** | **VERIFIED** ($74,999,999,925) |
| **Greenshoe 83,333,333 (15%)** | **VERIFIED** (14.999999955% of base) |
| **Total with full greenshoe** | **VERIFIED** (638,888,888 shares; gross $86,249,999,880) |
| **Net proceeds ~$74.4B / ~$85.7B** | **CONSISTENT** with SEC text; implies **~$600M** all-in fee drag vs gross (not only $55M expenses) |
| **Offering expenses ~$55M** | **VERIFIED** (exclusive of underwriting discounts/commissions) |
| **424B4 final prospectus** | **NOT FILED** for SpaceX as of EDGAR pull 2026-06-04 |
| **01-offering-terms.md accuracy** | **Mostly correct** — minor rounding/clarification fixes applied |
| **04-s1-amendment-diff.md accuracy** | **Mostly correct** — one lock-up % nuance clarified below |

---

## 1. Proceeds math

### Gross proceeds

```
555,555,555 × $135.00 = $74,999,999,925  (~$75.0B rounded)
(555,555,555 + 83,333,333) × $135.00 = $86,249,999,880  (~$86.25B rounded)
```

| Item | SEC / calculated |
|------|------------------|
| Primary shares | 555,555,555 Class A |
| Greenshoe | 83,333,333 Class A (15% of primary; 30 days) |
| Total if greenshoe full | **638,888,888** |
| Expected price | **$135.00** per share (expected, not a range) |
| Net proceeds (issuer) | **~$74.4 billion** base; **~$85.7 billion** full greenshoe |

### Net vs underwriting expenses

| Component | Amount | Source |
|-----------|--------|--------|
| Estimated **offering expenses** (excl. discounts/commissions) | **~$55 million** | *Underwriting* |
| Underwriting discounts/commissions | **Not filled** ($ placeholders on cover pricing table) | Cover / *Underwriting* |
| Greenshoe commission | **None** on over-allotment shares | *Underwriting* footnote |
| **Implied total deduction (base)** | **~$599,999,925** | $74.999999925B − $74.4B |
| **Implied total deduction (full greenshoe)** | **~$549,999,880** | $86.25B − $85.7B |

**Audit note:** `01-offering-terms.md` correctly cites **$55M offering expenses** but readers may confuse that with the full gap to net proceeds. The **~$600M** base-case gap is predominantly **un disclosed underwriting spread** until 424B4.

**Sensitivity (SEC):** ±1M primary shares → **±$135M** net proceeds (*Use of Proceeds*).

---

## 2. Capitalization table (re-extracted, S-1/A #2)

*As of March 31, 2026; dollars in millions unless share counts noted.*

### Pro forma corporate actions (before IPO)

1. Preferred conversion → **3,448,110,450** Class A + **3,274,452,900** Class B  
2. Class C reclassification → **494,050,675** Class A  
3. Charter effectiveness (Class D eliminated)

### Share counts — common stock

| Line | Actual | Pro forma | Pro forma as adjusted (post-IPO base) |
|------|--------|-----------|--------------------------------------|
| **Class A** issued/outstanding | 2,964,501,353 / **2,882,480,230** | **6,824,641,355** | **7,380,196,910** |
| **Class B** | **2,421,215,365** | **5,695,668,265** | **5,695,668,265** |
| **Class C** | 494,050,675 | **0** | **0** |
| **Class A if greenshoe full** | — | — | **7,463,530,243** |

**Total common (A+B) post-IPO (base):** 7,380,196,910 + 5,695,668,265 = **13,075,865,175** (matches dilution table).

**IPO primary increment on Class A:** 6,824,641,355 + 555,555,555 = 7,380,196,910 ✓

### Equity capitalization ($M)

| | Actual | Pro forma | Pro forma as adjusted |
|--|--------|-----------|---------------------|
| Cash | 15,852 | 15,852 | **90,305** |
| Total long-term debt | 29,111 | 29,111 | 29,111 |
| Redeemable preferred | 7,049 | — | — |
| Total shareholders' equity | 34,533 | 41,582 | **116,028** |
| **Total capitalization** | 70,693 | 72,762 | **147,208** |

### Voting & control (post-IPO)

| Metric | Value | Citation |
|--------|-------|----------|
| Class A votes per share | 1 | *Description of Capital Stock* |
| Class B votes per share | **10**; elects **majority of board** | *The Offering* |
| **Musk total voting power** | **~82.4%** ( **~82.3%** if greenshoe full) | Cover / *The Offering* |
| **Musk voting from Class B only** | **~81.1%** | *The Offering* |
| Class A % of **total voting power** | **11.5%** (11.6% if greenshoe) | *The Offering* |
| Class B % of **total voting power** | **88.5%** (implied) | 100% − 11.5% |
| **Controlled company** | Yes (Nasdaq + Nasdaq Texas exemptions intended) | *The Offering* |

**Beneficial ownership (pre- vs post-offering table):** Musk **84.4%** combined voting power post-offering (*Security Ownership*) vs **82.4%** in *The Offering* — reflect different definitions/timing (options, conversion, footnotes); **not treated as a documentation error** but must be labeled in models.

### Options / RSUs (equity overhang)

IPO **capitalization table does not add options/RSUs to share counts**; overhang appears in **Notes / Description of Capital Stock / Equity incentive** disclosures:

| Instrument | Approx. outstanding (from financial statement tables in prospectus) |
|------------|----------------------------------------------------------------------|
| Stock options | **~10.5M** (10,468,474 in extracted FY2025 table row) |
| RSUs | **~47.0M** (47,043,062 in extracted FY2025 table row) |
| Future plan reserves | Additional **millions** authorized under 2024 Plan (see *Executive Compensation*) |

**Post-IPO:** Class C awards convert to Class A per plan description; Musk received **no** 2025 equity grants.

**CFA dilution inputs:** Use **13.08B** basic post-IPO (A+B) + treasury-style option/RSU dilution from notes; greenshoe adds **83.3M** Class A. **Fully diluted** not on cap table page — build from options/RSUs/warrants footnotes.

---

## 3. Use of proceeds — exact allocation (quote)

> “We intend to use the net proceeds from this offering to fund our growth strategy, including **the expansion of our AI compute infrastructure**, **enhancements to our launch infrastructure and launch vehicles**, **increases in the scale and capacity of our satellite constellations**, and **any remaining amounts for general corporate purposes**.”

— *Use of Proceeds* (also *Prospectus Summary — Use of proceeds*)

### Audit flags — use of proceeds

| Flag | Severity | Detail |
|------|----------|--------|
| **General corporate purposes** | Medium | Residual bucket; no % split across AI / launch / satellites |
| **No quantified capex plan** | Medium | Proceeds tied to strategy narrative, not line-item budget |
| **Pro forma cash** | Info | $90.3B cash pro forma as adjusted vs $15.9B actual — driven by net proceeds application |

---

## 4. Principal stockholders & resale (summary)

| Item | Disclosure |
|------|------------|
| Musk economic (existing + new table) | **12,520,309,620** shares pre-offering group; **~95.8%** of pre-IPO share count / **52%** of total consideration at avg **$6.48** |
| New investors | **555,555,555** shares; **4.2%** count / **48%** of total consideration at **$135** |
| Registration rights | **~12.2B** Class A (incl. B conversion) post-offering |
| **>1-year lock cohort** | **~7.8B** shares (incl. all Musk stock) |

See **`B-lock-up-schedule.md`** for day-by-day release table.

---

## 5. S-1 → S-1/A #1 → S-1/A #2 — material change audit trail

| Topic | S-1 (2026-05-20) | S-1/A #1 (2026-06-01) | S-1/A #2 (2026-06-03) | Materiality |
|-------|------------------|----------------------|----------------------|-------------|
| **IPO price** | Blank range | Blank range | **$135.00** fixed expected | **HIGH** |
| **Share count** | Blank | Blank | **555,555,555** + greenshoe | **HIGH** |
| **Net proceeds** | Not quantified | Not quantified | **$74.4B / $85.7B** | **HIGH** |
| **Anthropic GPUs** | Not disclosed | **~325,000 NVIDIA GPUs** | Retained | **HIGH** |
| **Anthropic termination** | 90-day notice | **3-month initial carveout**, then 90-day | Retained | **MEDIUM** |
| **Anthropic wording** | “unused compute” | “**portion of** compute” | Retained | **MEDIUM** |
| **Lock-up schedule** | Framework | **7.8B** >1-year language | Full staged + **366d** Musk | **HIGH** |
| **Nasdaq Texas** | Inc. | **LLC** | LLC | **LOW** (entity name) |
| **Musk voting % on cover** | Not in same form | Similar | **82.4%** | **MEDIUM** |
| **Financial restatement** | ~28 “restate” hits | ~29 | ~29 | **No new restatement event** flagged |

---

## 6. Errors found & fixes to research files

### Errors / corrections in `01-offering-terms.md`

| # | Issue | Action |
|---|-------|--------|
| 1 | Gross proceeds shown only as **~$75.0B** | **Clarified** exact $74,999,999,925 in audit; rounding acceptable |
| 2 | Implied **~$600M** fee gap vs **$55M** expenses not explained | **Added** implied deduction note in corrected `01-offering-terms.md` |
| 3 | Lock-up **60% vs 63%** | **Clarified** different denominators (post-IPO vs pre-IPO) |
| 4 | Directed share count not shown | **Added** ~27,777,778 shares (5% × 555,555,555) |

### Errors / corrections in `04-s1-amendment-diff.md`

| # | Issue | Action |
|---|-------|--------|
| 1 | Lock-up row “**7.8B** >1-year” on A#1 — accurate | No change |
| 2 | Missing **60% vs 63%** nuance | **Added** footnote in corrected file |
| 3 | 424B4 status | **Confirmed** still pending on EDGAR 2026-06-05; two 2026-06-04 FWPs do not clear final-prospectus blockers |

### SEC filing quirks (not research file errors)

- Duplicate “**of the of the**” in extended lock-up share table  
- **82.4%** (voting) vs **84.4%** (beneficial ownership table) — label metric in models  

---

## 7. Governance discount factors (CFA framing)

| Factor | Observation | Valuation implication |
|--------|-------------|------------------------|
| **Dual-class** | B = 10 votes; B elects majority of directors | Economic ownership ≠ control; apply voting/control premium to insider block |
| **Controlled company** | Nasdaq exemptions expected | Weaker minority governance; committee independence risk |
| **Musk lock-up** | 366 days, **no** early release | Largest supply tranche back-ended |
| **Staged insider releases** | Earnings-linked + price trigger (+30% pop) | Supply reflexive to post-IPO performance |
| **Directed shares** | 5%, no lock-up | Day-1 float additive (~27.8M shares) |
| **Option/RSU overhang** | ~10.5M options; ~47M RSUs (orders of magnitude) | Additional dilution beyond IPO primary |
| **Greenshoe** | 83.3M primary shares, **no** underwriter discount on option | Issuer-friendly; dilution if exercised |

---

## 8. 424B4 EDGAR status check

**CIK:** 0001181412 (SPACE EXPLORATION TECHNOLOGIES CORP)  
**Checked:** 2026-06-04 via `https://data.sec.gov/submissions/CIK0001181412.json`

**Recent filings (relevant):**

| Date | Form | Accession |
|------|------|-----------|
| 2026-06-03 | S-1/A | 0001628280-26-040364 |
| 2026-06-01 | S-1/A | 0001628280-26-039276 |
| 2026-05-20 | S-1 | 0001628280-26-036936 |

**Form 424B4:** **None** in recent submission feed for this CIK.

**Status:** **Pending** — final offering price, underwriting spread, and listing date remain subject to 424B4 (or pricing press release).

---

## 9. Return payload (parent agent)

**Errors found:** 0 critical math errors on primary deal terms; 3 documentation clarifications (net fee gap, lock-up % bases, directed share count); 1 SEC typo; voting % metric labeling.

**$135 / 555M verified:** **Yes.**

**424B4:** **Not filed** as of 2026-06-05 EDGAR; 2026-06-04 FWPs are offering communications, not final pricing prospectuses.
