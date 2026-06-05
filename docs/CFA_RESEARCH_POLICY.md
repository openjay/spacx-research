# CFA-aligned research policy

**Scope:** SPACX repository artifacts (workstreams, plugin agents, models, reports)  
**Status:** Internal research and education — **not** retail distribution  
**Not legal advice.** Consult qualified counsel before any commercial or advisory use.

Related: [COMPLIANCE.md](./COMPLIANCE.md) · [LISTING_STATUS.md](./LISTING_STATUS.md)

---

## 1. Facts vs opinions

| Class | Definition | Examples in SPACX |
|-------|------------|-------------------|
| **Facts** | Verifiable from primary or cited secondary sources | S-1/A table rows, EDGAR accession IDs, SHA-256 of cached HTML |
| **Opinions / framing** | Judgment, scenario weighting, synthesis | Bull/Base/Bear thesis labels, regime tags, “watch” narratives |
| **Projections** | Forward-looking estimates not in filings | Model stubs, non-GAAP bridges, Phase 3 data contracts |

**Rule:** Facts and opinions must be **visually and structurally separated** (tables vs narrative, schema fields vs LLM prose). LLM output may **not** invent filing numbers or upgrade evidence grades.

---

## 2. Source hierarchy (A / B / C / D)

Aligned with Phase 1 audit tracks and `plugin/manifest.yaml` `evidence_policy`:

| Grade | Sources | Use for core financials |
|-------|---------|-------------------------|
| **A** | SEC EDGAR primary documents (S-1, 10-K/Q, 424B4), exchange/regulator filings | **Required** |
| **B** | Company IR, tier-1 newswire tied to primary doc | Supplementary only |
| **C** | Reputable secondary analysis, industry data | Context; never sole basis for metrics |
| **D** | Social, unattributed web, chain gossip | **Forbidden** for core financials |

**SEC-first:** On conflict, defer to the latest SEC primary document. See [workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md](../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md).

---

## 3. Disclosures, third-party research, and conflicts

### 3.1 Third-party valuation research

Append to human-gated exports (Level 3+) and any share that cites external fair value:

```text
THIRD-PARTY RESEARCH NOTICE
External fair value estimates (e.g., Morningstar, New Constructs) are Grade C context.
They are NOT verified by SPACX, may rely on opaque assumptions, and do NOT override
SEC EDGAR figures. See workstreams/valuation-research/ and docs/VALUATION_AUDIT.md.
```

Assumption packets live under [`workstreams/valuation-research/assumptions/`](../workstreams/valuation-research/assumptions/) and map to `plugin/schemas/ExternalResearchPacket.json`. See [VALUATION_AUDIT.md](./VALUATION_AUDIT.md). C-tier packets **must not** promote external DCF outputs to Grade A metrics or thesis **BULL** without sealed A-tier corroboration.

### 3.2 Underwriter conflict template (CFA Standard VI)

Use when syndicate research or media leaks reference offering participants (e.g. Goldman AI surge via Reuters/FT):

```text
CONFLICT — UNDERWRITER RESEARCH
Provider: Goldman Sachs
Role in offering: Lead underwriter (Form S-1/A #2 cover)
Source: Reuters citing Financial Times — primary research report NOT independently verified
Claim: AI revenue ~$322B by 2030; total revenue ~$474B by 2030 (thematic projection)
Use: Scenario framing only; excluded from Grade A metrics and core DCF inputs.
Conflict flags: LEAD_UNDERWRITER, UNVERIFIED_FT_REPORT
```

Flag in packets: `conflict_flags: [LEAD_UNDERWRITER, UNVERIFIED_FT_REPORT]` (see `assumptions/goldman-ai-surge-reuters.yaml`).

### 3.3 Conflicts of interest disclosure template

Include in human-gated exports (Level 3+) and any external share:

```text
DISCLOSURE — SPACX Research Output
Date: [YYYY-MM-DD]
Prepared by: [name / agent run id]

Conflicts of interest:
- [ ] Author holds or intends to hold SPCX or related securities (SpaceX ecosystem, peers)
- [ ] Author is compensated by issuer, underwriter, or affiliated entity
- [ ] Author has received non-public information (describe or N/A)
- [ ] No material conflicts declared

Distribution: Private research — not for retail investor distribution.
Not investment advice. See docs/CFA_RESEARCH_POLICY.md and docs/COMPLIANCE.md.
```

---

## 4. Record retention

| Artifact | Retention | Purpose |
|----------|-----------|---------|
| Cached SEC HTML (`workstreams/.../s1*.htm`) | Indefinite in repo; SHA-256 in ingest metadata | Reproducibility |
| `EvidencePacket` + `AuditReceipt` JSON | Immutable log per state change | Chain of custody |
| Agent run logs / scheduler receipts | Minimum 7 years (policy target for production) | Regulatory inquiry readiness |
| Evidence audit workpapers | Versioned with commit hash | CFA Standard V(A) diligence |

**Evidence packets:** Seal before thesis probability or grade changes (`evidence.seal`). Mismatch triggers `hash_mismatch_investigation` human gate (OnchainRWAAgent).

---

## 5. Model limitations (V0)

| Limitation | Detail |
|------------|--------|
| **Non-GAAP** | Segment metrics may use issuer-defined non-GAAP; always cite filing footnotes |
| **Stubs** | `plugin/models/` V0 returns placeholder estimates — not production signals |
| **No live data** | V0 has no live market feed, no live EDGAR poll in default deploy |
| **Pre-listing** | SPCX is **proposed symbol** until 424B4 + first trade ([LISTING_STATUS.md](./LISTING_STATUS.md)) |
| **LLM** | Narrative only; cannot override metrics, risk veto, or evidence grade |

---

## 6. Observation vs recommendation gates

`ActionProposal` schema default: **`OBSERVE_ONLY`**.

| Gate | Requirement |
|------|-------------|
| Pre-424B4 | `FINAL_PROSPECTUS_PENDING` blocker active → no size-up proposals |
| Pre-first-trade | Listing blockers → observe / research only |
| Grade A missing | No actionable buy/sell framing on core financial claims |
| Compliance level ≤2 | Proposals internal; no order routing |

Agents **must not** emit buy/sell/hold solicitations. Risk layer may shrink or block proposals; domain agents cannot bypass.

---

## 7. Distribution gates

| Level | Audience | Gate |
|-------|----------|------|
| 0–2 | Operator / repo contributors | Default |
| 3 | Internal draft report | Human `thesis_publish` gate |
| 4+ | Team or subscriber channels | Compliance review + disclosure footer |
| Retail | **Prohibited** | This repository is **private research tooling**, not a retail research product |

Do not redistribute cached SEC HTML or synthesis as a standalone “research note” without provenance footer and [DATA_PROVENANCE.md](./DATA_PROVENANCE.md) notice.

---

## Reference links

| Topic | URL |
|-------|-----|
| CFA Institute Code of Ethics & Standards | https://www.cfainstitute.org/ethics-standards/codes-standards-guidance |
| CFA Standard V(A) — Diligence and Reasonable Basis | https://www.cfainstitute.org/ethics-standards/codes-standards-guidance/standards-of-practice-handbook/standard-v-investment-analysis-recommendations-and-actions |
| FINRA Regulatory Notice 15-09 (digital advice) | https://www.finra.org/rules-guidance/notices/15-09 |
| SEC — Investment adviser use of AI (staff bulletin) | https://www.sec.gov/newsroom/speeches-statements/investment-adviser-use-artificial-intelligence |
