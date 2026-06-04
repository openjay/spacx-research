# SPACX Intelligence Plugin (V0)

**Plugin id:** `spacx-intelligence` · **Version:** 0.1.0 · **Compliance:** Level 2 (proposals only, no execution)

24/7 autonomous market intelligence for **SPCX**. Agents call structured APIs instead of parsing `workstreams/` by hand.

## Quick start (agents)

```python
# From repo root with PYTHONPATH=.
from plugin.api import evidence, ingest, metrics, risk, thesis, alerts

# Ingest SEC filing reference
ingest.ingest_source({
    "source_id": "sec_spcx_s1a2_20260603",
    "source_type": "SEC_FILING",
    "uri": "workstreams/sec-evidence-phase1/s1a2-main.htm",
    "ingested_at": "2026-06-04T00:00:00Z",
})

# Read watch metric
metrics.get_metric("SPCX", "AI_CAPEX_REVENUE")

# Thesis + risk + proposal chain
thesis.get_thesis_state("SPCX")
risk.risk_evaluate("SPCX", portfolio_context={"cash_pct": 20})
risk.generate_action_proposal("SPCX", portfolio_context={})

# Seal evidence before thesis probability changes
evidence.seal_evidence("pkt_phase1_starlink_q1_2026", packet={...})

# Alerts
alerts.get_risk_alerts("SPCX")
```

## REST mapping

| Method | Path | Python |
|--------|------|--------|
| POST | `/ingest/source` | `ingest.ingest_source` |
| POST | `/extract/events` | `ingest.extract_events` |
| POST | `/metrics/update` | `metrics.metrics_update` |
| GET | `/metrics/{asset}/{metric_id}` | `metrics.get_metric` |
| POST | `/thesis/update` | `thesis.thesis_update` |
| GET | `/thesis/{asset}` | `thesis.get_thesis_state` |
| POST | `/risk/evaluate` | `risk.risk_evaluate` |
| POST | `/action/propose` | `risk.propose_action` |
| POST | `/alert/dispatch` | `alerts.alert_dispatch` |
| POST | `/evidence/seal` | `evidence.seal_evidence` |
| POST | `/report/generate` | `evidence.generate_report` |

Base path: `/api/v1/spacx` (see `manifest.yaml`).

## Schemas

JSON Schema under `plugin/schemas/`:

| File | Purpose |
|------|---------|
| `SourceRecord.json` | Ingested source metadata + hash |
| `EvidencePacket.json` | Graded claims (A–D) |
| `MetricDefinition.json` | Registry entry shape |
| `MetricSnapshot.json` | Live metric + GREEN/AMBER/RED |
| `ThesisState.json` | P(thesis) + WATCH/BULL/BEAR |
| `RiskState.json` | Risk budget output |
| `ActionProposal.json` | Observe/hold/size proposals |
| `AuditReceipt.json` | Immutable operation log |

## Principles

- **LLM interprets** — narratives and attribution only.
- **Stats judge** — event study, Bayesian thesis, regime detection (`plugin/models/`).
- **Risk constrains** — caps, blockers, `blocked_actions`.
- **Evidence grades** — A = SEC/exchange/regulator; D = social (never core financials).

Phase 1 SEC tables: `workstreams/sec-evidence-phase1/`. Metric registry: `plugin/metrics/registry.yaml` (parallel workstream).

## Compliance

`compliance_level: 2` — research, alerts, and `ActionProposal` generation **without** order routing. See `docs/COMPLIANCE.md` and `docs/ARCHITECTURE.md`.

## 中文（代理调用）

代理应通过 **工具/API** 读写结构化对象，而不是直接改 Markdown 底稿。核心流程：采集源 → 提取事件 → 更新指标 → 贝叶斯更新 thesis → 风控评估 → 生成建议 → 封存证据哈希。V0 禁止自动下单；424B4、上市日、首份财报未齐前默认 `OBSERVE_ONLY`。
