# Track C — Risk Disclosure & Metrics Audit

**Auditor:** Track C (Risk / CFA metrics)  
**Primary filing:** Form S-1/A #2, filed **2026-06-03** (`s1a2-main.htm`)  
**Cross-checks:** `03-risk-metrics-map.md`, `00-phase1-summary.md`, `01-offering-terms.md`, `02-segment-financials.md`  
**Scope:** Full major-theme risk mapping (not top-10 sampling), Anthropic contract verification, 12 watch metrics + governance KPIs, accuracy audit of Table 3.

---

## 1. Anthropic / xAI contract verification

### 1.1 Anthropic Cloud Services Agreements — **PASS** (prospectus narrative)

**Verbatim (Business / Prospectus Summary — AI segment), S-1/A #2:**

> In May 2026, we entered into **Cloud Services Agreements** with **Anthropic PBC** … with respect to access to compute capacity across **COLOSSUS** and **COLOSSUS II**. Compute capacity provided includes approximately **325,000 NVIDIA GPUs**, backed by hyperscale-class CPUs, exabyte-scale storage and high-speed networking … Pursuant to these agreements, the customer has agreed to pay us **$1.25 billion per month through May 2029**, with capacity ramping in **May and June 2026 at a reduced fee**. **After the initial three-month period**, the agreements may be terminated by either party upon **90 days’ notice**. The customer will retain ownership and intellectual property rights in its content, AI models, and related data.

| Claim in `03-risk-metrics-map.md` | Filing match | Status |
|-----------------------------------|--------------|--------|
| $1.25B / month | Exact | **PASS** |
| Through May 2029 | Exact | **PASS** |
| Ramp May–June 2026, reduced fee | Exact | **PASS** |
| 90-day termination after initial 3 months | Exact | **PASS** |
| ~325,000 NVIDIA GPUs | Exact | **PASS** |
| COLOSSUS & COLOSSUS II (Memphis / Southaven) | Exact | **PASS** |
| Customer retains model/content IP | Exact | **PASS** |

**Note:** The same paragraph appears twice in the extracted HTML (Prospectus Summary + Business) — consistent, not conflicting.

### 1.2 Exhibit / financial-statement footnote — **PARTIAL** (less granular)

**Cloud Services Agreement (unaudited footnote, ~F-63), May 3, 2026:**

> … customer has agreed to pay a **monthly fee** through **May 2029**, with capacity ramping in **May 2026** at a reduced fee. The agreement may be terminated by either party upon **90 days’ notice**.

| Field | Prospectus narrative | F-63 footnote | Gap |
|-------|---------------------|---------------|-----|
| Dollar amount | $1.25B/mo stated | “monthly fee” only | Footnote omits quantum |
| Ramp window | May–June 2026 | May 2026 only | June not repeated |
| Termination carve-out | After initial 3-month period | Not stated | Carve-out only in narrative |
| GPU count | ~325,000 | Not in footnote | Scale only in narrative |
| Agreement count | Plural “Agreements” | Singular “agreement” | Wording only |

**Audit conclusion:** Use **Prospectus Summary / Business** as the monitoring source of truth for economics; treat F-63 as confirmation of existence/date, not full terms. No 424B4 exhibit text was available to reconcile.

### 1.3 xAI — **N/A (no commercial cloud contract in filing)**

S-1/A #2 discloses **xAI Merger** (effective **Feb 2, 2026**) and **X Merger** (Mar 28, 2025) as **common-control combinations** — not third-party cloud services economics comparable to Anthropic.

There is **no** xAI counterparty schedule with $/month, GPU count, termination, or end date. Track C marks xAI contract verification **N/A**; monitor via segment integration, Grok/X KPIs, and related-party disclosures instead.

---

## 2. Accuracy audit — `03-risk-metrics-map.md`

| Issue | Severity | Detail |
|-------|----------|--------|
| **Under-mapped regulatory risk** | High | Table 3 lists FAA/spectrum briefly but omits **AI/X platform regulation**, **export controls**, **international legal regimes**, **payments licenses**, **Section 230–style legislative risk**, and **EchoStar Spectrum Transaction** closing conditions (FCC approved May 12, 2026; closing conditions remain). |
| **Supply chain / AI processors thin** | High | Filing stresses **sole/limited-source suppliers**, **no long-term chip supplier contracts**, **GPU availability**, **power/water** for datacenters — only partially captured under “AI compute & capex.” |
| **Debt / liquidity under-specified** | Medium | Table 3 mentions bridge/credit generically; filing quantifies **$20B SpaceX Bridge Loan** (matures **Sep 2, 2027**), **$5B amended revolving credit facility** (May 2026), **$1.5B available** on revolver as of Mar 31, 2026, **3.75:1** leverage covenant (step-up to **4.25:1** post-qualifying acquisition). |
| **Material weaknesses** | Low | Table 3 says “count stable across amendments” — filing discusses **material weakness / significant deficiency** risk qualitatively; **no numeric count** of weaknesses in extracted text. Rephrase to “disclosure of ICFR weaknesses” not “count stable.” |
| **Insurance / launch failure** | Medium | Missing: **no insurance** on satellites/launch vehicles; **launch delays/failures** as recurring theme. |
| **Government customer concentration** | Medium | U.S. government program funding, debarment, ITAR/export — not in Table 3. |
| **F-63 vs narrative** | Low | Table 3 does not flag footnote vs narrative delta (Section 1.2 above). |
| **Correct items** | — | Starlink KPIs, lock-up schedule, Musk ~82.4% / controlled company, Anthropic economics (narrative), Musk no early lock-up — **verified**. |

---

## 3. Major risk themes — completeness map (all themes, not top-10)

**Method:** Full-text pass of *Risk Factors* (pp. 27–~72) + Prospectus Summary risk bullets (items 58–74 in cover extract). **116** distinct risk lead sentences in the Business RF block; grouped into **26 major themes** below.

| # | Major theme (SEC) | Representative disclosure | Watch metric(s) | Threshold / trigger (CFA-style) |
|---|-------------------|---------------------------|-----------------|--------------------------------|
| 1 | **Starship scale & cadence** | Failure/delay at scale delays growth strategy | Starship orbital payload milestone; launch count QoQ | No payload-to-orbit by **YE 2026** → **red**; launch cadence **<150/yr** FY run-rate → **amber** |
| 2 | **Launch infrastructure** | Extended launch pad unavailability | Pad downtime days; manifest slip | **>90 days** single-pad outage → **red** |
| 3 | **Launch vehicle ↔ constellation mismatch** | Falcon cannot deploy V3 / V2 Mobile; Starship required | % launches on Starship vs Falcon for new gen | **0** Starship commercial sat deploys by **H2 2027** → **red** |
| 4 | **FAA / launch licensing** | FAA launch & reentry licenses; delays disrupt ops | FAA enforcement actions; license renewal lag | License delay **>6 mo** → **red** |
| 5 | **Space regulation (export / ITAR)** | Export controls; foreign-person tech release | Export license denials; ITAR violations | Any **debarment** notice → **red** |
| 6 | **Starlink growth & ARPU** | Subscriber growth, enterprise adoption | Subscribers (M); ARPU ($/mo); Connectivity revenue | Subscribers QoQ **<3%** → **amber**; ARPU **<$60** two quarters → **amber** |
| 7 | **Constellation deployment & environment** | ~9,600 sats; deployment risk; space environment | Satellite count; collision/debris events | Net sat count decline QoQ → **red** |
| 8 | **Spectrum / EchoStar transaction** | Spectrum Transaction FCC-approved; closing conditions | Transaction close; spectrum modification progress | No close **6 mo** post-FCC approval → **amber** |
| 9 | **Satellite-to-mobile regulatory** | FCC + foreign approvals; ~30 country MNO deals | Countries live; regulatory denials | Partnership count flat **4 quarters** → **amber** |
| 10 | **Service reliability / outages** | Outages erode subscriber trust | Downtime incidents; churn (if disclosed) | Material nationwide outage → **red** |
| 11 | **No launch/satellite insurance** | Bear full cost of losses | Launch failure count; mission anomaly rate | **2** high-visibility failures in **12 mo** → **red** |
| 12 | **AI segment integration & history** | Recently formed; integration/execution risk | AI op. loss; integration milestones in MD&A | Op. loss widens **>20%** YoY while rev flat → **amber** |
| 13 | **AI competition & customer concentration** | Limited AI customers vs peers | Customer concentration % (future 10-Q) | **>50%** AI rev from one customer → **amber** |
| 14 | **Anthropic contract economics** | $1.25B/mo through May 2029; ramp; termination | Recognized rev vs contractual run-rate; 8-K amendments | Recognized **<80%** of ramp-adjusted run-rate **2 Q** → **amber**; termination 8-K → **red** |
| 15 | **Third-party AI customer credit** | Customers may not be cash-flow positive | Receivables; impairments; DSO | DSO **>90 days** on AI rev → **amber** |
| 16 | **xAI / Grok / X platform** | Rapid iteration; regulation; app stores | Daily posts; AI op. loss; platform actions (Brazil precedent) | Regulatory ban in **G7** market → **red** |
| 17 | **AI compute infrastructure** | Power, water, GPUs, networking | Nameplate GW; AI capex; capex/revenue | Capex/revenue **>8x** (Q1 baseline ~9.4x) two quarters → **amber** |
| 18 | **Supply chain / semiconductors** | Sole-source; no long-term chip contracts | GPU supply commentary; supplier concentration | Public shortage disclosure + margin hit → **red** |
| 19 | **Power / datacenter fuel** | Natural gas / turbine dependence | Power cost; outage at Colossus sites | Datacenter power curtailment **>7 days** → **red** |
| 20 | **Capital intensity & FCF** | Substantial capex across segments | Total capex; consolidated Adj. EBITDA | Consolidated Adj. EBITDA **negative** FY → **amber** |
| 21 | **Indebtedness & covenants** | $20B bridge; revolver; leverage tests | Net debt; leverage ratio; maturity wall | Leverage **>3.5x** (pre step-up) → **amber**; bridge refinanced **<6 mo** to maturity → **amber** |
| 22 | **Liquidity** | Cash $15.9B; securities $7.8B; revolver availability | Cash + securities; revolver draw | Liquidity **<$10B** without IPO proceeds modeled → **review** |
| 23 | **Related-party / Musk conflicts** | RPTs; Musk control; potential conflicts | RPT $ disclosed; new 8-K exhibits | RPT **>5%** of quarterly opex → **amber** |
| 24 | **Key person (Musk) & talent** | Dependence on Musk; engineering talent war | Musk role changes; headcount cost trend | CEO departure → **red** |
| 25 | **Cyber / data / privacy** | Disruption or unauthorized access | Breach disclosures; compliance spend | Material breach → **red** |
| 26 | **Governance / offering structure** | Controlled co.; dual-class; lock-up; forum/arbitration | See Section 4 | See Section 4 |

**Risks mapped:** **26 major themes** (full RF taxonomy); **16** condensed bullets in Prospectus Summary risk list.

---

## 4. Twelve watch metrics + governance (CFA monitoring pack)

Replaces/extends Phase 1 “12 metrics” with **measurable thresholds** and explicit **governance** line items.

| # | Metric | Phase 1 baseline (S-1/A #2) | Threshold / action |
|---|--------|------------------------------|-------------------|
| **1** | **IPO price vs benchmark** | Expected **$135.00** | Final 424B4 price **±5%** → rebase all per-share models |
| **2** | **First-day pop (lock-up trigger)** | TBD post-listing | **≥30%** above IPO for **5 of 10** days unlocks **+455.8M** shares (*Shares Eligible*) |
| **3** | **Starlink subscribers (M)** | **10.3** (Q1 2026) | QoQ growth **<3%** → amber; negative → red |
| **4** | **Starlink ARPU ($/mo)** | **$66** (Q1 2026) | **<$60** for 2 consecutive quarters → amber |
| **5** | **Connectivity Segment Adj. EBITDA** | **$2,087M** (Q1 2026) | **<$1.5B** quarterly → amber |
| **6** | **Anthropic revenue vs contract** | **$1.25B/mo** contractual (May 2029 end) | Recognized revenue **<75%** ramp-adjusted run-rate for **2 Q** → amber; contract termination filing → red |
| **7** | **AI operating loss / revenue** | **$(2,469)M / $818M** (Q1 2026) | Loss/revenue ratio **>4.0x** two quarters → amber |
| **8** | **AI capex / revenue** | **$7,723M / $818M** ≈ **9.4x** (Q1 2026) | **>10x** two quarters → red |
| **9** | **Starship / launch cadence** | **40** launches Q1 2026; Starship payload **2H 2026** | Zero Starship commercial milestones by **YE 2026** → red |
| **10** | **Lock-up supply releases** | Staged: day **70/90/105/120/135**, Q3 earnings, day **180**, extended through **day 366** (Musk) | Model **float %** each gate; Musk **no early release** |
| **11** | **Net leverage & debt wall** | Bridge **$20B** due **Sep 2, 2027**; covenant **3.75:1** | Leverage **>3.5x** → amber; no refi plan **12 mo** before maturity → red |
| **12** | **Musk voting + RPT flow** | **~82.4%** voting; controlled company | Voting **>85%** post-offering → governance red flag; material new RPT without audit committee review → amber |

### Governance watch metrics (non-optional for Track C)

| Metric | Disclosure (S-1/A #2) | Monitor |
|--------|----------------------|---------|
| **Controlled company** | Yes; intends to rely on Nasdaq / Nasdaq Texas exemptions | Track **board independence %** vs exemption requirements |
| **Class B 10:1 + board election** | Class B **10 votes/share**; Class B elects **majority of board** | Class B as **% total votes** (post-IPO **~88.5%** class vote weight) |
| **Musk voting power** | **~82.4%** total | Change **>2 pp** quarter-over-quarter |
| **Texas / Business Court forum** | Internal disputes → **Texas Business Court**; Exchange Act claims per bylaws | Litigation venue shifts; adverse rulings on forum provisions |
| **Mandatory arbitration** | Bylaws require **mandatory arbitration** for certain shareholder claims | Arbitration filings; cost of dissent enforcement |
| **TBOC / derivative limits** | Texas Business Organizations Code provisions limit certain derivative claims | Legislative or court challenges to TBOC applicability |
| **Lock-up vs governance** | Musk **~7.8B** shares restricted **>1 year**; **no early release** | Compare insider sales post-day 366 vs other holders |

---

## 5. Related-party & concentration (CFA addendum)

| Concentration vector | Filing fact | Metric |
|--------------------|-------------|--------|
| **Anthropic (AI compute)** | Up to **~$15B/yr** run-rate if fully ramped ($1.25B × 12) | % of consolidated / AI segment revenue once recognized |
| **Musk control** | **~82.4%** votes; CEO/CTO/Chairman | Governance discount sensitivity |
| **EchoStar spectrum** | License purchase; FCC approved **May 12, 2026** | Close timing; cash/stock consideration per pro forma |
| **Tesla** | Terafab collaboration (Mar 2026); historical RPT context | New RPT $ in *Related Person Transactions* / Exhibit 10.x |
| **Government** | Space & Connectivity government revenue streams | % revenue government; program cancellation headlines |
| **GPU supplier** | NVIDIA ~325k GPUs cited for Anthropic deal alone | Supply chain disclosure in MD&A / risk updates |
| **Debt concentration** | **$20B** single bridge facility | % total cap; refi spread at maturity |

---

## 6. Track C verdict (summary)

| Item | Result |
|------|--------|
| **Anthropic contract verification** | **PASS** (narrative terms); **PARTIAL** on F-63 footnote granularity |
| **xAI contract verification** | **N/A** (merger only) |
| **Major risks mapped** | **26 themes** (complete taxonomy pass) |
| **`03-risk-metrics-map.md` accuracy** | **Needs expansion** on regulatory, supply chain, debt, insurance; fix material-weakness wording |
| **12 watch metrics + governance** | **Defined above** with thresholds |

**Primary source URL:** https://www.sec.gov/Archives/edgar/data/1181412/000162828026040364/spaceexplorationtechnologib.htm
