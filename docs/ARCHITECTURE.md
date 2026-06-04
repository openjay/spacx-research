# SPACX Intelligence — Architecture

**Product:** SPACX autonomous market intelligence plugin · **Asset:** SPCX · **V0:** research + alerts + proposals (compliance level 2)

---

## English

### Design thesis

AI-era investing treats markets as a **continuous event stream**, not a five-day report cycle. SPACX maintains a 24/7 **world model** (metrics, thesis probabilities, risk budget) and only emits **action candidates** when evidence grade, statistical gates, and compliance level align. Execution is deliberately后置 (postponed).

> **LLM is the researcher; statistics are the auditor; risk is the constitution; evidence is the chain of custody.**

### Layer stack

```text
Data → Evidence → Metrics → Statistical → LLM → Risk → Action → Audit
```

| Layer | Responsibility | AI may | AI must not |
|-------|----------------|--------|-------------|
| **Data** | SEC EDGAR, exchange, market, on-chain, RWA attestations | Ingest, dedupe, timestamp | Invent unsourced numbers |
| **Evidence** | Grade A/B/C/D, extract claims, hash packets | Map filing → claims | Promote social posts to core financials |
| **Metrics** | Formulas, baselines, thresholds (registry) | Compute ARPU, capex/revenue, float | Change formulas ad hoc |
| **Statistical** | Event study, Bayesian thesis, regime, factors, anomalies | Update P(thesis), flag AMBER/RED | Place orders |
| **LLM** | Explain deltas, write reports, hypothesize | Summarize conflicts | Override hard metrics or risk veto |
| **Risk** | Position caps, thematic exposure, blockers | HOLD / shrink proposals | Be bypassed by domain agents |
| **Action** | `ActionProposal` (observe, paper, size) | Propose | Auto-execute at level ≤2 |
| **Audit** | Receipts, evidence seals, optional on-chain hash | Log every state change | Mutate thesis without sealed evidence |

### Data flow

```mermaid
flowchart LR
  subgraph ingest [Data]
    SEC[SEC EDGAR]
    MKT[Market data]
    CHAIN[On-chain / RWA]
  end
  subgraph core [Core pipeline]
    EV[Evidence A-D]
    MET[Metrics engine]
    STAT[Statistical models]
    TH[Thesis state]
  end
  subgraph govern [Governance]
    LLM[LLM agents]
    RSK[Risk engine]
    ACT[Action proposals]
    AUD[Audit receipts]
  end
  SEC --> EV
  MKT --> EV
  CHAIN --> EV
  EV --> MET
  MET --> STAT
  STAT --> TH
  EV --> LLM
  MET --> LLM
  TH --> RSK
  MET --> RSK
  RSK --> ACT
  EV --> AUD
  ACT --> AUD
```

### 24/7 scheduler tiers

Hybrid **event-driven + cron** (see `plugin/scheduler.yaml` when present):

| Tier | Cadence | Targets |
|------|---------|---------|
| T0 | 1–5 min | Crypto, stablecoin, RWA liquidity, oracle deviation |
| T1 | 15 min | Futures, peers, vol, pre/after-hours |
| T2 | 1 hour | SEC EDGAR, exchange notices, tier-1 news |
| T3 | Daily | Thesis report, portfolio risk, watchlist |
| T4 | Weekly | Model scoring (Brier), threshold calibration |
| T* | Event | 424B4, earnings, lock-up, Starship, Nasdaq-100, RWA stress |

Market close ≠ system idle: filings, macro, and chain state still update the world model.

### Compliance levels (0–6)

| Level | Capability |
|-------|------------|
| **0** | Read-only research plugin |
| **1** | Automated reports and alerts |
| **2** | **Current V0** — trade *candidates*, no orders |
| **3** | Paper portfolio |
| **4** | Small live size, whitelist, human approval |
| **5** | Policy-bound auto-execution + kill switch |
| **6** | External advisory / fund management (legal/licensing) |

Robo-adviser and algorithmic trading supervision apply if level ≥4–6; this repo stays at **0–2** until explicitly gated.

### Web3 / RWA (roadmap)

- **Phase 1 (now):** Evidence hash only — seal `EvidencePacket` / `AuditReceipt` digests; no trading on-chain.
- **Phase 2:** RWA monitor (redemption, custody, oracle).
- **Phase 3:** Policy-bound execution with jurisdiction and custody guards.

Details: [ROADMAP.md](./ROADMAP.md).

### Repository map

| Path | Role |
|------|------|
| `plugin/manifest.yaml` | Plugin contract |
| `plugin/schemas/` | JSON Schema SSOT |
| `plugin/api/` | Agent-callable stubs |
| `plugin/metrics/` | Registry + threshold engine |
| `plugin/models/` | Statistical interfaces |
| `plugin/agents/` | Eight agent roles |
| `workstreams/sec-evidence-phase1/` | Phase 1 SEC evidence (complete) |

---

## 中文

### 设计命题

AI 时代投资研究的对象是**连续事件流**，而不是「等财报 → 写报告 → 工作日复盘」。SPACX 7×24 维护**世界模型**（指标、thesis 概率、风险预算），仅在证据等级、统计门禁与合规级别同时满足时输出**行动建议**；交易执行故意后置。

> **大模型做研究员；统计做审计员；风控做宪法；证据做监管链。**

### 分层架构

```text
数据 → 证据 → 指标 → 统计 → 大模型 → 风控 → 行动 → 审计
```

| 层 | 职责 | 允许 | 禁止 |
|----|------|------|------|
| **数据** | SEC、行情、链上、RWA | 采集、去重、打时间戳 | 无来源数字入库 |
| **证据** | A/B/C/D 分级、抽取 claim、哈希封存 | 申报文件→结构化主张 | 社媒数字进核心财务表 |
| **指标** | 公式、基线、阈值 | 计算 ARPU、capex/revenue | 随意改公式 |
| **统计** | 事件研究、贝叶斯 thesis、 regime | 更新 P(thesis) | 下单 |
| **大模型** | 解释、报告、假设 | 总结冲突 | 覆盖硬指标或风控否决 |
| **风控** | 仓位上限、主题暴露、阻塞项 | HOLD / 缩小建议 | 被业务 agent 绕过 |
| **行动** | `ActionProposal` | 提议 | V0 自动成交 |
| **审计** | 收据、证据 seal、可选上链哈希 | 全链路留痕 | 无证据改 thesis |

### 7×24 调度层级

| 层级 | 频率 | 对象 |
|------|------|------|
| T0 | 1–5 分钟 | 加密、稳定币、RWA 流动性 |
| T1 | 15 分钟 | 期货、同业、波动率 |
| T2 | 1 小时 | SEC、交易所公告、高质量新闻 |
| T3 | 每日 | Thesis 报告、组合风险 |
| T4 | 每周 | 模型评分、阈值校准 |
| T* | 事件触发 | 424B4、财报、解禁、Starship |

### 合规分级（0–6）

当前仓库 **V0 = Level 2**：可生成交易**候选**，不可自动下单。对外资管或全自动执行需 Level 6 法律结构，不在本阶段范围。

### Web3

第一阶段仅**证据哈希上链**（可验证研究状态时间点），不将 RWA token 默认为无监管资产。详见路线图 Web3 小节。

---

## Related docs

- [ROADMAP.md](./ROADMAP.md)
- [plugin/README.md](../plugin/README.md)
- Phase 1 synthesis: [workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md](../workstreams/sec-evidence-phase1/audit/00-integrated-audit-opinion.md)
