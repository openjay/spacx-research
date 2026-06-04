# SPACX compliance framework

**Research and education only.** This document defines automation compliance levels for the SPACX plugin agents. It is **not** legal advice. Consult qualified counsel before any commercial or advisory use.

**Phase 1 evidence anchor:** [workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md](../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)

**Related policies:** [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md) · [LISTING_STATUS.md](./LISTING_STATUS.md) · [DATA_PROVENANCE.md](./DATA_PROVENANCE.md)

---

## Research-only disclaimer

SPACX artifacts (agents, scheduler, reports) are produced for **internal research and education**. They do **not** constitute:

- Investment advice or a recommendation to buy, sell, or hold any security
- An offer or solicitation of securities
- A personalized recommendation for any particular investor
- Affiliation with SpaceX, xAI, the SEC, FINRA, or any broker-dealer

Users must verify all figures against current SEC filings and perform independent diligence.

**Listing status:** SPCX is the **proposed / expected listing symbol** (not a confirmed listed ticker) until Form 424B4 and first trading confirmation. See [LISTING_STATUS.md](./LISTING_STATUS.md).

---

## Compliance levels 0–6

| Level | Name | Automation allowed | External distribution |
|-------|------|--------------------|------------------------|
| **0** | Offline draft | Local files only; no network | None |
| **1** | Ingest only | EDGAR/chain read; no synthesis | None |
| **2** | Internal monitor | Alerts to operator console; gated drafts | None (default floor in `scheduler.yaml`) |
| **3** | Internal report | Daily thesis **draft**; human publish gate required | None without gate |
| **4** | Team share | Gated export to private team channels | Requires compliance review + disclaimer footer |
| **5** | Subscriber research | Licensed research distribution | Requires RIA/robo-adviser legal stack (see below) |
| **6** | Execution-adjacent | Order routing, allocation, custody | **Out of scope** — OnchainRWAAgent and all agents **forbidden** |

**Current deployment target:** Level **2–3** (monitor + gated draft). Level 6 is explicitly excluded.

---

## Robo-adviser / FINRA notes (informational)

If SPACX outputs were ever offered to paying subscribers as systematic recommendations, US regulatory touchpoints may include (non-exhaustive):

| Topic | Note |
|-------|------|
| **Investment Advisers Act** | Discretionary or individualized advice → investment adviser analysis; may require SEC/state registration or exemption (e.g., publisher exclusion — facts-specific). |
| **Robo-adviser guidance** | SEC staff guidance on digital advisers emphasizes disclosure, algorithm governance, and compliance programs for automated recommendations. |
| **FINRA** | Broker-dealer channels implicate suitability, Reg BI, communications supervision (Rule 2210), and AML if accounts are involved. |
| **Marketing rule (IA)** | Performance presentations and testimonials have heightened requirements under Advisers Act Marketing Rule. |

**SPACX default posture:** Research tooling only — **not** a registered investment adviser, **not** a broker-dealer, **no** client accounts, **no** trade execution. Bull/Base/Bear scenarios are **evidence-driven framing**, not price targets or orders.

---

## Agent-specific boundaries

| Agent | Hard rule |
|-------|-----------|
| All agents | No `place_orders`, no buy/sell/hold solicitations |
| SECFilingAgent | Numeric claims from EDGAR primary docs only |
| EvidenceAuditorAgent | No grade A without SEC excerpt |
| OnchainRWAAgent | **NO TRADING** — monitoring and hashing only |
| LockupFloatAgent | No listing-date assumption without 424B4 |
| MacroLiquidityAgent | Macro labels cannot upgrade to grade A |

---

## Evidence integrity

- **OnchainRWAAgent** publishes SHA-256 manifests; mismatches trigger `hash_mismatch_investigation` human gate.
- **EvidenceAuditorAgent** is authoritative for A/B/C/D grades.
- Conflicts defer to SEC primary documents per Phase 1 source hierarchy (see [CFA_RESEARCH_POLICY.md](./CFA_RESEARCH_POLICY.md) and [ROADMAP.md](ROADMAP.md)).

---

## 中文合规摘要

- **等级 0–6：** 从离线草稿到执行层；当前目标 **2–3**（内部监控 + 人工门控日报），**禁止 6 级交易**。
- **非投资建议：** 所有代理输出仅供研究，不构成买卖建议或与 SpaceX/SEC 的关联。
- **若商业化：** 需单独评估投资顾问法、机器人顾问指引、FINRA 沟通规则；本仓库默认不进入该模式。
