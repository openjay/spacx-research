# Track C — Phase 1 Gap Register (pre-424B4)

**Purpose:** Items Phase 1 tables (`00`–`04`, `03-risk-metrics-map`) **cannot answer** until the final prospectus (**Form 424B4**) or post-IPO periodic reports.  
**Auditor:** Track C  
**As-of:** S-1/A #2 (2026-06-03)

---

## Gap severity key

| Code | Meaning |
|------|---------|
| **P0** | Blocks valuation / risk model calibration |
| **P1** | Blocks monitoring KPI baselines |
| **P2** | Improves precision but workaround exists |

---

## A. Offering & pricing (Table 1 gaps)

| ID | Gap | Why Phase 1 cannot answer | Pre-424B4 workaround | Severity |
|----|-----|---------------------------|----------------------|----------|
| G-01 | **Final IPO price** | S-1/A #2 uses *expected* **$135** only | Sensitivity at $135 ±5/10% | **P0** |
| G-02 | **Underwriting discount & commission ($ and %)** | Preliminary table shows **“$” placeholders** | Assume range from comps; no SEC number | **P0** |
| G-03 | **Exact listing / first trade date** | Not in registration statement | Calendar assumption | **P1** |
| G-04 | **Final share count if upsized/downsized** | Fixed in S-1/A #2 but may change at pricing | Use 555.6M + 83.3M greenshoe as base case | **P1** |
| G-05 | **Directed share allocation outcome** | 5% reserved; actual allocation unknown | Model 5% max | **P2** |
| G-06 | **Final net proceeds** | Depends on G-01, G-02 | Use ~$74.4B / ~$85.7B from S-1/A math | **P1** |

---

## B. Financial & segment KPI gaps (Table 2 gaps)

| ID | Gap | Why Phase 1 cannot answer | Pre-424B4 workaround | Severity |
|----|-----|---------------------------|----------------------|----------|
| G-07 | ~~**Segment revenue FY 2023–2024**~~ | **Resolved (Track A)** — in Note F-23; applied in `02-segment-financials.md` | — | — |
| G-08 | **Segment gross margin** | Not broken out in extracted tables | Use op. income / EBITDA proxies | **P1** |
| G-09 | **Connectivity FCF bridge** | Adj. EBITDA only; no segment FCF | Consolidated cash flow only | **P1** |
| G-10 | **AI gross margin trend** | Not segment-disclosed | Op. loss / revenue ratio (Track C metric #7) | **P1** |
| G-11 | **Anthropic recognized revenue vs $1.25B/mo** | Contract May 2026; Q1 2026 predates ramp | None — wait for 10-Q | **P0** |
| G-12 | **Ramp pricing mechanics ($)** | “Reduced fee” — no dollar amount | Model % haircut scenarios | **P0** |
| G-13 | **Post-IPO quarterly cadence** | S-1 is point-in-time through Mar 31, 2026 | N/A until earnings | **P1** |

---

## C. Contract & exhibit gaps (Anthropic / xAI)

| ID | Gap | Why Phase 1 cannot answer | Pre-424B4 workaround | Severity |
|----|-----|---------------------------|----------------------|----------|
| G-14 | **Full Cloud Services Agreement text** | Economics in narrative; **Exhibit 10.x** not in local HTML cache | Narrative terms only (Track C PASS) | **P1** |
| G-15 | **F-63 footnote vs narrative reconciliation** | Footnote lacks $1.25B, 3-month carve-out, June ramp | Trust narrative; flag in audit | **P1** |
| G-16 | **SLAs, penalties, capacity definitions** | Not in prospectus extract | None | **P2** |
| G-17 | **xAI commercial contract terms** | No customer contract — merger only | Monitor segment + RPT | **N/A** |
| G-18 | **Cursor option / acquisition terms** | Option described; exercise price contingent on VWAP | Scenario only | **P2** |

---

## D. Risk → metric monitoring gaps (Table 3 gaps)

| ID | Gap | Why Phase 1 cannot answer | Pre-424B4 workaround | Severity |
|----|-----|---------------------------|----------------------|----------|
| G-19 | **Customer concentration % (Anthropic)** | Pre-revenue recognition / no 10-Q footnote | Contractual max ~$15B/yr theoretical | **P0** |
| G-20 | **ICFR material weakness count & remediation** | Qualitative risk only in S-1 | Wait for post-IPO 10-K | **P1** |
| G-21 | **Insurance coverage decisions** | Explicit **no** sat/launch insurance — no $ cap | Model full loss scenarios | **P2** |
| G-22 | **Real-time FAA / FCC docket status** | Risk disclosure only | External regulatory tracking | **P2** |
| G-23 | **Export license / ITAR event history** | Not tabulated | News / 8-K | **P2** |
| G-24 | **GPU supplier contract duration** | Explicit: **no** long-term chip contracts | Supply risk qualitative | **P1** |
| G-25 | **EchoStar Spectrum Transaction close date & cash paid** | FCC approved; closing conditions open | Pro forma footnote partial | **P1** |
| G-26 | **Leverage ratio actual vs covenant** | Covenant disclosed; **pro forma post-IPO leverage** not in Table 3 | MD&A debt section + model | **P1** |
| G-27 | **Interest rate sensitivity ($)** | Filing gives ~$200M per 100bps on bridge — not in Table 3 | Add from MD&A | **P2** |
| G-28 | **Brazil / X regulatory precedent $ impact** | Narrative only | Legal reserve unknown | **P2** |

---

## E. Governance & legal gaps

| ID | Gap | Why Phase 1 cannot answer | Pre-424B4 workaround | Severity |
|----|-----|---------------------------|----------------------|----------|
| G-29 | **Final bylaws / charter (effective at close)** | Form attached but post-offering effectiveness | Use described terms (10:1, Business Court, arbitration) | **P1** |
| G-30 | **Board composition post-IPO** | Names in S-1; independence exemptions applied later | Controlled-co. exemption checklist | **P1** |
| G-31 | **Arbitration enforceability case law** | Forward-looking legal risk | Qualitative | **P2** |
| G-32 | **Musk milestone vesting certifications timing** | 1.302B Class B tranches — certification dates unknown | 8-K upon milestones | **P1** |
| G-33 | **Actual lock-up release shares traded** | Schedule disclosed; market volume unknown until events | Calendar model from Table 3 | **P1** |

---

## F. Related-party transaction gaps

| ID | Gap | Why Phase 1 cannot answer | Pre-424B4 workaround | Severity |
|----|-----|---------------------------|----------------------|----------|
| G-34 | **Complete RPT dollar schedule** | Section p. 243 not machine-extracted in Phase 1 HTML | Pull Exhibit **10.x** from EDGAR index | **P1** |
| G-35 | **Tesla Terafab economic terms** | Collaboration announced; financial terms sparse | Monitor subsequent 8-K | **P1** |
| G-36 | **Musk personal loan / guarantee balances** | May be in exhibits not cached locally | EDGAR exhibit pull | **P2** |

---

## G. What Phase 1 tables **can** answer today (no gap)

- Expected price **$135**, share count **555.6M**, greenshoe **83.3M**
- Segment Q1 2026 / FY 2025 KPIs (subscribers, ARPU, capex, EBITDA, launches)
- Anthropic **narrative** economics (PASS per Track C)
- Lock-up **calendar mechanics** and Musk **no early release**
- Musk **~82.4%** voting; controlled company; Class B **10:1**
- Bridge **$20B** / revolver **$5B** capacity (debt facts in filing, weakly in Table 3)

---

## Top 10 gaps (priority for Phase 2 / 424B4)

| Rank | ID | Gap |
|------|-----|-----|
| 1 | G-01 | Final IPO price |
| 2 | G-02 | Underwriting spread ($) |
| 3 | G-11 | Anthropic recognized revenue |
| 4 | G-12 | Anthropic ramp fee ($) |
| 5 | G-19 | Customer concentration % |
| 6 | G-14 | Full Anthropic contract exhibit |
| 7 | G-07 | Historical segment revenue |
| 8 | G-26 | Pro forma leverage post-IPO + IPO proceeds |
| 9 | G-25 | EchoStar close & consideration |
| 10 | G-34 | Complete RPT exhibit schedule |

---

## Phase 2 handoff checklist

When **424B4** files:

1. Re-run Track C contract verification against final exhibits.  
2. Lock **G-01, G-02, G-06** to final offering table.  
3. Reconcile **G-15** (F-63 vs final prospectus narrative).  
4. Seed monitoring dashboard with Section 4 metrics in `C-risk-disclosure-audit.md`.  
5. Close **G-11, G-19** after first **10-Q** customer concentration footnote.
