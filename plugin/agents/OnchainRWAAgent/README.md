# OnchainRWAAgent

**Web3/RWA pre-layer (预埋)** · Workstream 3 Phase **W1** · Compliance level **2**

Full strategy: [docs/RWA_WEB3_STRATEGY.md](../../../docs/RWA_WEB3_STRATEGY.md)

---

## EN — Scope

`OnchainRWAAgent` owns the **`rwa/`** data lane in the Market Intelligence Core. It is a **monitor-and-hash** agent only.

| In scope (W1) | Out of scope |
|---------------|--------------|
| SHA-256 evidence manifests for plugin artifacts | Main trading layer or order routing |
| Chain state monitor: stablecoin peg, tokenized treasury attestations | Auto on-chain execution (swaps, bridges, staking) |
| `onchain.rwa_anomaly` and `evidence.hash_mismatch` events | Wallet connect, sign, or custody |
| Correlate chain events to SEC `evidence_auditor` IDs | Promote chain data to Grade A without SEC-primary evidence |
| Emit attestation staleness metrics | Treat TVL or DEX depth as liquidity truth |

### Constitutional rules (agents)

1. **Tokenized ownership ≠ tradable liquid market** — chain balance is not an exit quote.
2. **RWA value = programmable settlement/custody/redemption/audit/compliance** — not “token = liquidity.”
3. **Maturity ladder** — W1 caps at L0/L1 surfaces (stablecoin, tokenized treasury); equities/complex RWAs are later phases.

### Hard boundary

**NO TRADING** — no exceptions. Forbidden actions are enumerated in `agent.yaml` (`forbidden_actions`).

### Roadmap phases (not this agent alone)

| Phase | Capability |
|-------|------------|
| W2 | RWA risk scoring engine (beyond TVL) |
| W3 | Settlement abstraction (observe rails) |
| W4 | Policy-bound wallet — **gated, manual approval** |

---

## 中文 — 职责与边界

`OnchainRWAAgent` 负责市场情报核心下的 **`rwa/`** 数据通道，属于 **预埋** 阶段 W1：**仅监控与证据哈希**。

- 监控稳定币偏离、代币化国债/国库券储备证明等链上状态。
- 维护 `EvidencePacket` 相关制品的 SHA-256 清单；异常触发人工门禁。
- **禁止**：钱包、签名、兑换、桥、托管、质押、任何下单或自动链上执行。
- **禁止**：仅凭链上余额或 TVL 推断可交易流动性或将链上数据升为 A 级证据（无 SEC 依据时）。

调度：T0（1–5 分钟）链上监控；每小时哈希清单汇总。详见 `agent.yaml`。

---

## Schedule

- **T0:** 1–5 min — `rwa/` chain monitor (scheduler default 5m)
- **Hourly:** `evidence.content_hash_manifest` rollup

See `plugin/scheduler.yaml` and [docs/ARCHITECTURE.md](../../../docs/ARCHITECTURE.md).

---

*Not affiliated with Space Exploration Technologies Corp. (SpaceX). Research only — [BRAND_USAGE_POLICY](../../../docs/BRAND_USAGE_POLICY.md).*
