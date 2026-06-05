# SpaceX Valuation Report Audit — CFA Standard

**Scope:** External synthesis report ($780B vs $1.75T) vs SPACX SEC evidence base  
**Status:** Internal research audit — not investment advice  
**Primary SEC anchor:** Form S-1/A Amendment No. 2 (2026-06-03) — Grade **A**  
**Audit date:** 2026-06-05

Related: [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md) · [ARCHITECTURE.md](./ARCHITECTURE.md) · [ARCHITECTURE_DELTA.md](./ARCHITECTURE_DELTA.md) · [05-master-evidence-tables.md](../workstreams/sec-evidence-phase1/audit/05-master-evidence-tables.md)

---

## Executive Summary (English)

**Verdict:** The report’s *direction* is CFA-aligned: it separates **great company** from **great price**, treats Morningstar’s $780B as an **external fair value estimate** (not market price or verified intrinsic value), and correctly warns that $1.75T IPO framing embeds near-perfect execution on AI and optionality. **Partial architecture change is warranted** — add a **Valuation & External Evidence Layer** parallel to SEC evidence; do **not** replace the SEC-first pipeline or collapse into a trading bot.

**$780B anchor:** **Valid as a conservative C-tier fair value estimate** when Starlink is weighted heavily, AI/orbital/Mars are probability-discounted, and capex/governance overhang are respected. **Incomplete** as sole valuation — it may understate engineering compounding (Starship cost curve) and does not replace issuer cap table math or A-tier segment financials.

**Critical correction:** Share-count math in the report uses **~12.96B** shares; SEC S-1/A #2 cap table shows **13,075,865,175** Class A+B post-IPO (~**13.08B**). At $135/sh, implied equity value is **~$1.77T**, not exactly $1.75T. The ~$60/sh DCF-implied price moves only ~1% ($59.65 vs $60.19) — immaterial to discipline, but **material to audit hygiene**.

**Reverse DCF (New Constructs):** The cited stress case (23% NOPAT margin, 50% revenue CAGR to 2035 → ~$1.1T revenue, ~$248B NOPAT) is **arithmetically consistent** with FY2025 revenue $18.67B as base; **primary source verification required** for WACC, terminal value, and segment attribution inside New Constructs’ model (not in repo).

**Three price anchors** ($60 DCF / $135 IPO / $185–300 FOMO) map to **ActionProposal gates** (`OBSERVE_ONLY` default), not buy recommendations.

---

## 中文执行摘要

**裁定：** 报告**方向正确**——区分「伟大公司」与「伟大价格」；Morningstar **$780B** 应标注为 **C 级外部公允价值估计**（非市价、非经核实的内在价值）；$1.75T IPO 叙事隐含 AI 与期权价值近乎完美兑现。**架构需局部增补**：在 SEC 证据层之上并联 **估值与外部证据层**；**不得**取代 SEC-first 流水线，**不得**退化为交易机器人。

**$780B 锚：** 作为**保守 C 级公允价值估计**成立（Starlink 高权重、AI/轨道/火星概率折扣、capex 与治理折价）。**不能**作为唯一估值——可能低估工程复利（Starship 成本曲线），且不能替代申报文件 cap table 与 A 级分部财务。

**关键修正：** 报告用 **~12.96B** 股本；S-1/A #2 显示 A+B 合计 **13,075,865,175**（约 **13.08B**）。$135/股对应约 **$1.77T** 市值，非精确 $1.75T。反推 ~$60/股差异约 1%，对纪律影响小，但对**审计口径**影响大。

**反向 DCF（New Constructs）：** 23% NOPAT、50% CAGR 至 2035（收入约 $1.1T、NOPAT 约 $248B）自 FY2025 收入 $18.67B 起算**算术自洽**；WACC、终值、分部假设须**回查原始模型**（仓库内无）。

**三价格锚**（$60 DCF / $135 IPO / $185–300 FOMO）对应 **ActionProposal 门禁**，非买入建议。

---

## 1. Verdict on the $780B Anchor

### 1.1 Terminology (CFA discipline)

| Term | Definition | $780B classification |
|------|------------|----------------------|
| **Fair value estimate** | Third-party model output (DCF/SOTP) with stated assumptions | Morningstar ~$780B via Reuters — **C-tier external estimate** |
| **Market price** | Observable transaction price post-listing | **Unknown** until 424B4 + first trade |
| **Intrinsic value** | Analyst-owned DCF/SOTP with full assumption disclosure in workpapers | **Not established** in SPACX repo; Morningstar model **not ingested** |

The report correctly frames $780B as **long-horizon cash-flow discipline**, not a day-one price forecast. CFA Standard V(A) requires reasonable basis: **acceptable as a labeled external anchor**; **unacceptable as Grade A fact** or sole input to core financial metrics.

### 1.2 When the $780B anchor is valid

- **Segment cash-flow heterogeneity** matches SEC evidence: Connectivity generates adj. EBITDA ($7,168M FY2025); AI is deeply loss-making (adj. EBITDA **$(1,237)M** FY2025) with **~9.4×** capex/revenue in Q1 2026.
- **Probability-weighting** of unproven lines (orbital data centers, Mars) is appropriate; issuer S-1 does not capitalize these as near-term revenue.
- **Governance / supply overhang** is A-tier: ~82.4% Musk voting, ~60% restricted >1yr, staged lock-up, directed shares ~27.8M without standard lock-up.
- **Pre-GAAP profitability** (FY2025 net loss **$(4,937)M**) supports caution vs passive-index inclusion narratives (S&P 500 rules — C-tier news, cross-check only).

### 1.3 When the $780B anchor is incomplete

- **Starship optionality:** DCF may underweight step-change unit economics if commercial cadence beats filing baselines (40 launches Q1 2026 vs 170 FY2025).
- **Starlink moat duration:** Global LEO scale and adj. EBITDA margin **64.1%** (Q1 2026) may deserve higher terminal value than generic broadband comps — external model weights unknown.
- **AI ground infrastructure:** Anthropic contract ($1.25B/mo through May 2029, Grade A) is real revenue; discount rate on contract quality vs capex intensity is a **model choice**, not a filing fact.
- **No substitute for SEC cap table:** All per-share math must use **13.08B** basic A+B (+ option/RSU overhang per notes).

### 1.4 Implied per-share math (corrected)

| Input | Report | SEC A-tier (S-1/A #2) |
|-------|--------|-------------------------|
| Shares (A+B post-IPO) | ~12.96B | **13,075,865,175** (~13.08B) |
| Price anchor | $135/sh | **$135.00** expected (A) |
| Equity value at $135 | ~$1.75T | **~$1,765B** (~$1.77T) |
| Implied price at $780B EV | ~$60/sh | **~$59.65/sh** |

Greenshoe fully exercised adds **83,333,333** Class A → **13,159,198,508** total A+B; $780B / 13.159B ≈ **$59.27/sh**.

---

## 2. Reverse DCF Audit (New Constructs Claims)

### 2.1 Claims under review

| Claim | Source tier | SPACX verification |
|-------|-------------|-------------------|
| To justify ~$1.75T, NOPAT margin must rise to **23%** immediately | C — New Constructs | **Requires primary model** — not reproduced in repo |
| Revenue **50% CAGR** to 2035 → ~**$1.1T** revenue | C — New Constructs | **Arithmetic check: PASS** (see below) |
| NOPAT ~**$248B** at that revenue/margin | C — New Constructs | **Arithmetic check: PASS** |
| Alternate: **19%** NOPAT margin, **34%** CAGR → ~**$500B** valuation | C — New Constructs | Revenue path plausible; **EV bridge needs WACC/terminal** — not verified |

### 2.2 Arithmetic sanity check (auditor-calculated, FY2025 base)

Using SEC A-tier consolidated revenue **$18,674M** (FY2025):

```
50% CAGR × 10 years → 18.674 × 1.5^10 ≈ $1,077B revenue  ✓ (≈ $1.1T cited)
23% NOPAT margin     → 1,077 × 0.23 ≈ $248B NOPAT         ✓

34% CAGR × 10 years → 18.674 × 1.34^10 ≈ $337B revenue
19% NOPAT margin    → 337 × 0.19 ≈ $64B NOPAT
```

**Interpretation:** The New Constructs *narrative* is internally consistent at the revenue/NOPAT layer. What remains **unverified without primary source**:

- Discount rate (WACC), terminal growth, and net debt treatment in EV
- Whether “23% NOPAT immediately” is modeled from consolidated or segment mix
- Segment attribution (AI $322B by 2030 per Goldman leak vs filing AI revenue $3,201M FY2025)
- Sensitivity to Anthropic concentration (Customer A **20.9%** FY2025 revenue — A-tier)

### 2.3 SEC baselines for multiple context (A-tier)

At **$135/sh** and **13.076B** shares (equity **~$1,765B**):

| Metric | SEC numerator | Implied multiple @ $135 |
|--------|---------------|-------------------------|
| EV / Revenue (FY2025) | Revenue $18,674M; pro forma cash $90,305M; bridge $20,000M | **~90–95×** (EV ≈ equity − net cash post-IPO, simplified) |
| EV / Adj. EBITDA (FY2025) | Adj. EBITDA $6,584M | **~25–27×** |

These are **observation metrics**, not fair value. Valuation layer must compute with explicit EV formula in `plugin/valuation/implied_multiples.py` (see [ARCHITECTURE_DELTA.md](./ARCHITECTURE_DELTA.md)).

---

## 3. Source Hierarchy — External Research

Aligned with [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md) §2; extended for valuation workstream.

| Grade | Source | Valuation use | Conflict / caveat |
|-------|--------|---------------|-------------------|
| **A** | SEC S-1/A #2, future 424B4, 10-Q/K | Share count, $135 expected price, segment financials, lock-up, use of proceeds | **Required** for all per-share and segment inputs |
| **B** | Company IR tied to filing | Offering roadshow statements | Supplementary |
| **C** | Morningstar (Owens), New Constructs, PitchBook ranges | Fair value **estimates**, reverse DCF narratives | Model opaque; **not** DCF inputs without assumptions table |
| **C + conflict** | Goldman Sachs revenue projections via Reuters/FT | Bull-case scenario only | **Lead underwriter** (S-1/A cover) — CFA Standard VI(A) disclosure mandatory |
| **C** | Reuters, Business Insider | News, allocation, index, retail % | **Not** DCF inputs without A-tier cross-check |
| **D** | Social, unattributed leaks | Forbidden for core financials | — |

**Rule:** External fair value **never upgrades** to Grade A. `ValuationAnalystAgent` is **read-only** vs SEC numbers.

---

## 4. Three Price Anchors → ActionProposal Gates

**Not buy recommendations.** Default `proposal_type` = **`OBSERVE_ONLY`** per [ActionProposal.json](../plugin/schemas/ActionProposal.json) and compliance level 2.

| Anchor | Price (approx.) | Implied cap (13.08B sh.) | Evidence grade | ActionProposal gate |
|--------|-----------------|---------------------------|----------------|---------------------|
| **DCF conservative** | **~$60/sh** | **~$780B** | C — Morningstar via Reuters; **external estimate** | `OBSERVE_ONLY`; block `SIZE_UP` / `PAPER_BUY` when `PRICE_VS_DCF_ANCHOR_PCT` > 100% without human Level 3+ gate |
| **IPO issue** | **$135/sh** | **~$1.77T** | A — S-1/A #2 expected price | Pre-424B4: `FINAL_PROSPECTUS_PENDING` → observe only; rebase models on ±5% final price |
| **FOMO trading band** | **$185–300/sh** | **~$2.4–3.9T** | None (market sentiment) | `OBSERVE_ONLY` + `risk_state: RED` if price > 2× DCF anchor without earnings confirmation; narrative tags `ipo_boom` / `supply_overhang` only |

**Pre-listing blockers (active):** `FINAL_PROSPECTUS_PENDING`, `LOCKUP_DAY0_UNKNOWN`, `FIRST_EARNINGS_PENDING` — all `SIZE_UP` proposals blocked regardless of anchor.

---

## 5. What the Report Gets RIGHT (SPACX Discipline)

1. **Separates narrative from DCF** — matches SPACX layer stack (Evidence → Metrics → Statistical; LLM cannot override).
2. **Segment-aware valuation logic** — aligns with flywheels in `registry.yaml` (Starlink, AI, Starship).
3. **Reverse DCF framing** — “what must be true for $1.75T?” is the correct question for `VALUATION_REASONABLE` thesis (already in `ThesisState.json`).
4. **Underwriter conflict awareness** — Goldman as lead underwriter (A-tier list) + C-tier revenue leak = conflict flag required.
5. **Lock-up / float / governance** — matches Phase 1 Tables 1 & 5; supports `LOCKUP_OVERWHELMS_DEMAND` and `GOVERNANCE_DISCOUNT_EXPANDS` theses.
6. **S&P 500 vs Nasdaq-100 distinction** — reduces passive-flow certainty; appropriate skepticism.
7. **Three-anchor discipline** — prevents conflating fair value, issue price, and trading euphoria.
8. **“Great company ≠ great price”** — consistent with `OBSERVE_ONLY` default and CFA observation vs recommendation gates.

---

## 6. What the Report RISKS (Audit Flags)

| ID | Risk | Severity | Remediation |
|----|------|----------|-------------|
| R-001 | **Share count 12.96B vs 13.08B A+B** | Medium | All SPACX valuation modules use `05-master-evidence-tables.md` Table 1 |
| R-002 | **$1.75T label vs $1.77T at SEC shares** | Low | Tag as “~$1.75T marketing round” vs computed $1,765B |
| R-003 | **Morningstar $780B / $60 treated as fact** | High | Label C-tier; ingest via `ExternalResearchPacket` with assumptions[] |
| R-004 | **Goldman $474B / AI $322B by 2030** | High | C-tier + `conflict_flags: [LEAD_UNDERWRITER]`; Reuters unverified primary |
| R-005 | **New Constructs model not in repo** | Medium | `workstreams/valuation-research/` assumptions table + URL cache |
| R-006 | **Retail 30% allocation (BI)** | Medium | C-tier; cross-check vs directed share 5% (A-tier ~27.8M) — different concepts |
| R-007 | **Implicit buy/hold framing** (“首发观察仓”) | Medium | Map to `OBSERVE_ONLY` + disclosure footer; no solicitation |
| R-008 | **Connectivity operating income $4.4B** | Low | SEC shows segment **op income** $4,423M FY2025 — close; use A-tier table |
| R-009 | **Mixing fair value with trading targets** | Medium | Enforce three-anchor schema in `price_anchors.yaml` |

---

## 7. Architecture Verdict

| Question | Answer |
|----------|--------|
| Full repo restructure? | **NO** — SEC evidence phase remains SSOT for financial facts |
| Partial re-architecture? | **YES** — add **Valuation & External Evidence Layer** parallel to `workstreams/sec-evidence-phase1/` |
| Replace evidence pipeline? | **NO** |
| Trading bot / auto-execution? | **NO** — compliance level 2; ValuationAnalystAgent read-only |
| New thesis key? | **Already present:** `VALUATION_REASONABLE` in `ThesisState.json` |
| Collapse layers? | **FORBIDDEN** — Data → Evidence → **Valuation (parallel ingest)** → Metrics → … |

**Implementation pointer:** [ARCHITECTURE_DELTA.md](./ARCHITECTURE_DELTA.md)

---

## 8. Scenario Bands (Report vs SPACX Schema)

Report intervals are **opinion framing** (C-tier synthesis). SPACX will store in `scenario_bands.yaml` with explicit assumptions — not as facts.

| Band | EV range (report) | SPACX label |
|------|-------------------|-------------|
| Conservative | $500B–$800B | `conservative` |
| Base | $800B–$1.2T | `base` |
| Bull | $1.2T–$1.7T | `bull` |
| IPO bull | $1.75T+ | `ipo_bull` |
| Extreme sentiment | $3T+ | `sentiment_only` — no fundamental claim |

---

## 9. References (External — C-tier unless noted)

| Ref | URL | Tier |
|-----|-----|------|
| Reuters — Morningstar $780B | https://www.reuters.com/business/media-telecom/morningstar-values-spacex-780-billion-half-its-ipo-target-2026-06-02/ | C |
| New Constructs — reverse DCF | https://www.newconstructs.com/spacex-spcx-going-boldly-where-no-one-has-gone-before/ | C |
| Morningstar — valuation article | https://www.morningstar.com/stocks/does-spacexs-sky-high-valuation-make-sense | C |
| Reuters — Goldman AI revenue | https://www.reuters.com/business/media-telecom/goldman-sachs-expects-spacexs-ai-revenue-surge-100-fold-by-2030-ft-reports-2026-06-04/ | C + conflict |
| SEC S-1/A #2 | `workstreams/sec-evidence-phase1/s1a2-main.htm` | **A** |

---

*End of valuation audit. Supersedes any informal chat synthesis on share count or anchor grades.*
