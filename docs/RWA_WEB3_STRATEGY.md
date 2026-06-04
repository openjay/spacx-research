# Web3 / RWA strategy — SPACX pre-layer (预埋)

**Platform:** SPACX · **Asset context:** proposed / expected listing symbol SPCX (Space Exploration Technologies Corp.; pending 424B4 and first trade)  
**Status:** Planned / pre-layer — not production trading, not auto on-chain execution  
**Audience:** Engineering, agent operators, compliance reviewers (EN + 中文)

---

## 1. Constitutional thesis

Real-world asset (RWA) and Web3 infrastructure matter to SPACX as **programmable settlement, custody, redemption, audit, and compliance rails** — not as a shortcut where “token = liquidity.”

| Principle | Meaning for SPACX |
|-----------|-------------------|
| **Value = rails** | Tokenization is record-keeping + workflow automation on regulated infrastructure; economic value comes from faster, verifiable settlement and collateral mobility, not from secondary-market hype. |
| **Ownership ≠ market** | Tokenized ownership is **not** the same as a tradable, liquid, 24/7 secondary market. Agents must treat on-chain balances as **claims with legal wrappers**, not as spot equity. |
| **Maturity ladder** | Adopt complexity in order: stablecoin / tokenized deposits → collateral & repo → tokenized equities → complex RWAs. Do not skip rungs. |
| **Now = observe** | Current phase: **data lane** (`rwa/`), **evidence hash**, **chain-state monitors** — not the main trading layer, not autonomous on-chain execution. |
| **Friction → risk** | Every reduction in settlement friction **migrates** counterparty, custody, and oracle risk onto the platform; that demands harder **24/7 risk and audit** discipline, not looser gates. |

> **Agent constitutional rule (first):** *Tokenized ownership ≠ tradable liquid market.* No agent may infer NAV tradability, Grade-A financial status, or execution permission from chain balance or DEX depth alone.

---

## 2. What RWA value actually is

Institutional tokenization programs (wholesale deposits, DTC-custodied securities, collateral networks) converge on the same functional wins:

- **Atomic settlement** and programmability (conditions, time windows, compliance hooks)
- **Collateral mobility** across time zones without waiting for banking hours
- **Reconcilable ownership records** that tie on-chain state to off-chain entitlements
- **Audit surfaces** — proof-of-reserve, manifest hashes, immutable event logs

SPACX does **not** treat Total Value Locked (TVL), wallet count, or pool APY as primary success metrics. Success is **evidence-grade chain attestations** that can be cross-walked to SEC Workstream 1 tables and plugin `EvidencePacket` / `AuditReceipt` schemas.

---

## 3. Tokenized ownership vs liquid market

Three distinct layers must stay separated in architecture and agent prompts:

```text
Legal entitlement (off-chain) → Token / security entitlement (on-chain record) → Secondary liquidity (market)
```

| Layer | Question it answers | SPACX stance |
|-------|---------------------|--------------|
| Entitlement | Who owns what under law? | Map to issuer-sponsored or third-party custodial/synthetic taxonomies; never default to “permissionless DeFi.” |
| Token record | What does the ledger show? | Monitor; hash; correlate to `SourceRecord` / SEC IDs. |
| Liquidity | Can I exit at NAV now? | **Out of scope** for V0–W3; optional human-gated research in W4+ only. |

Synthetic or linked structures may be securities or security-based swaps with **stricter** counterparty rules than spot equity — agents must not collapse these into “crypto exposure.”

---

## 4. Maturity ladder (adoption order)

| Rung | Instruments | SPACX pre-layer focus |
|------|-------------|------------------------|
| **L0** | Stablecoins, tokenized deposits, tokenized T-bills | Chain monitor: peg deviation, reserve attestation lag, issuer pause events |
| **L1** | Collateral, repo, margin tokens | Risk scoring inputs: haircut, recall latency, CCP/oracle stress |
| **L2** | Tokenized equities & ETFs (DTC/NYSE/Nasdaq pilots) | Entitlement parity checks; **no** conflation with SPCX spot thesis |
| **L3** | Complex RWAs (credit, real estate, private credit) | Watchlist only; Grade C/D unless SEC-primary evidence exists |

Advancement across rungs requires **compliance level** upgrades (see [ARCHITECTURE.md](./ARCHITECTURE.md)) and explicit human gates — not scheduler promotion alone.

---

## 5. Pre-buried layer scope (预埋 — what we build now)

**预埋** means wiring interfaces, schemas, and monitors today so regulated settlement rails can plug in later **without** rewriting the evidence → metrics → risk pipeline.

| In scope (W1–W2) | Explicitly out of scope |
|------------------|-------------------------|
| `rwa/` data lane under Market Intelligence Core | Main order routing or production trading keys |
| SHA-256 evidence manifests + optional anchor metadata | Auto swaps, bridges, staking, custody moves |
| On-chain state monitor (stablecoin, tokenized treasury surfaces) | Wallet connect / sign / policy-bound execution (W4, gated) |
| `OnchainRWAAgent` watchlists + anomaly events | Promoting chain claims to Grade A without SEC |

Deliverables trace to [ROADMAP.md](./ROADMAP.md) Workstream 3 phases W1–W4.

---

## 6. Risk migration and 24/7 governance

As TradFi adopts 24/7 tokenized venues and instant settlement, **operational risk shifts from “market closed” to “always on.”** SPACX mirrors that with scheduler tier T0 (1–5 min) for chain/RWA monitors while keeping **compliance level 2** (proposals only).

When friction drops, these risks **rise** in relative importance (beyond TVL):

- Redemption queue / NAV basis blowouts
- Custodian and SPV insolvency (legal enforceability gap)
- Oracle and proof-of-reserve staleness or manipulation
- Compliance-controller freezes (ERC-3643-style) vs investor expectations
- Cross-layer reconciliation failure (“ghost tokens”)

Mitigation in pre-layer: continuous monitor → `onchain.rwa_anomaly` / `evidence.hash_mismatch` → human gates → audit receipts. Risk engine remains constitution; agents do not bypass.

---

## 7. Market infrastructure landscape (context)

External programs define the rails SPACX observes — not the trading logic SPACX executes.

| Actor | Development | Relevance to SPACX pre-layer |
|-------|-------------|------------------------------|
| **BIS Project Agorá** | Tokenised wholesale CB money + commercial bank deposits on a programmable platform; prototype → real-value testing | Template for **deposit rail** monitoring and cross-border settlement semantics |
| **DTCC** | ComposerX tokenization; collateral AppChain; DTC NAL for DTC-custodied tokenized assets (H2 2026 rollout) | **Collateral & entitlement** monitor targets; parity with traditional CUSIP entitlements |
| **SEC staff** | Jan 2026 tokenized securities taxonomy (issuer-sponsored vs third-party custodial/synthetic) | Compliance vocabulary for agent prompts and `SourceRecord` typing |
| **ICE / NYSE** | Tokenized securities platform (24/7 design); rule changes for tokenized form on existing book | **Liquidity calendar mismatch** — on-chain transferability vs T+1 banking/settlement |

SPACX research on SPCX remains **SEC-first** (Workstream 1). Chain data is **supplementary** evidence at Grade B/C unless tied to filing-primary claims.

---

## 8. Beyond-TVL risk model

DeFi-style TVL is an **inadequate** control metric for RWAs. Pre-layer scoring (Phase W2) should weight:

| Dimension | Example signals |
|-----------|-----------------|
| **Legal linkage** | SPV docs, jurisdiction, bankruptcy remoteness (metadata only in V0) |
| **Operational** | Attestation freshness, custodian change events, reconciliation gaps |
| **Liquidity illusion** | On-chain transfer enabled but off-chain redemption SLA > 24h |
| **Technical** | Oracle divergence, bridge pause, admin key rotation |
| **Compliance** | Transfer restriction flags, investor class mismatch |

Outputs feed **risk state** and thesis appendices — never auto-size positions at level ≤2.

---

## 9. SPACX implementation charter

| Component | Role |
|-----------|------|
| `plugin/agents/OnchainRWAAgent/` | W1 owner: monitors + hashes; **NO TRADING** |
| `plugin/api/evidence.py` | Canonical hash / seal hooks |
| `plugin/schemas/EvidencePacket.json` | Optional `web3_anchor` metadata (document-only in W1) |
| `docs/ARCHITECTURE.md` | `rwa/` data lane diagram + compliance ladder |
| Future `plugin/rwa/` (W2+) | Risk scoring engine interfaces |

**Exit criteria for leaving pre-layer:** human-approved compliance level ≥4, registered wallets, jurisdiction policy pack, and independent audit of redemption/custody runbooks — none of which are implied by this repository today.

---

## 中文摘要

### 核心命题

- RWA 的价值在于**可编程的结算、托管、赎回、审计与合规**，而非“上链就有流动性”。
- **代币化所有权 ≠ 可交易的流动性市场**（智能体第一条宪法规则）。
- **成熟度阶梯**：稳定币/代币化存款 → 抵押品/回购 → 代币化股票 → 复杂 RWA。
- **当前阶段（预埋）**：`rwa/` 数据通道 + 证据哈希 + 链上监控；**不是**主交易层，**不是**自动链上执行。
- 摩擦降低会把风险**迁移**到对手方、托管与预言机 — 需要更强的 **7×24 风控与审计**。

### 与监管基础设施的关系

BIS Agorá 探索批发层代币化存款与央行准备金；DTCC 推进代币化抵押品与 DTC 托管证券代币化；SEC 2026 年明确代币化证券仍适用联邦证券法；ICE/NYSE 推进 24/7 代币化证券交易设计。SPACX 仅**观察并对齐词汇**，SPCX 核心证据仍以 SEC 申报为最高等级。

### 智能体边界

`OnchainRWAAgent` 仅监控与哈希，禁止钱包、签名、兑换与下单。链上数据不得在无 SEC 依据时升为 A 级证据。

---

## References (URLs)

| Topic | URL |
|-------|-----|
| BIS Project Agorá (press, Apr 2024) | https://www.bis.org/press/p240403.htm |
| BIS Project Agorá (report) | https://www.bis.org/publ/othp110.htm |
| DTCC tokenized collateral platform (Apr 2025) | https://www.dtcc.com/news/2025/april/02/dtcc-announces-new-platform-for-tokenized-real-time-collateral-management |
| DTCC ComposerX (Feb 2025) | https://www.dtcc.com/news/2025/february/04/dtcc-announces-composerx |
| DTCC DTC tokenization NAL (Dec 2025) | https://www.dtcc.com/news/2025/december/11/paving-the-way-to-tokenized-dtc-custodied-assets |
| SEC staff — Statement on Tokenized Securities (Jan 28, 2026) | https://www.sec.gov/newsroom/speeches-statements/corp-fin-statement-tokenized-securities-012826-statement-tokenized-securities |
| SEC Commissioner Peirce — tokenization of securities (Jul 9, 2025) | https://www.sec.gov/newsroom/speeches-statements/peirce-statement-tokenization-securities-070925 |
| ICE / NYSE tokenized securities platform (Jan 19, 2026) | https://ir.theice.com/press/news-details/2026/The-New-York-Stock-Exchange-Develops-Tokenized-Securities-Platform/default.aspx |
| ICE House — NYSE 24/7 platform (podcast) | https://www.ice.com/insights/conversations/inside-the-ice-house/inside-nyses-24-7-tokenized-securities-platform-with-michael-blaugrund-and-jonp-herrick |
| RWA legal/operational risk (illustrative) | https://www.nethermind.io/blog/securing-tokenized-real-world-assets-the-legal-technical-and-operational-framework |

---

*Related: [ROADMAP.md](./ROADMAP.md) · [ARCHITECTURE.md](./ARCHITECTURE.md) · [COMPLIANCE.md](./COMPLIANCE.md) · [OnchainRWAAgent](../plugin/agents/OnchainRWAAgent/README.md)*
