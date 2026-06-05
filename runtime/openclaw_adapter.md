# OpenClaw / Longter adapter sketch (V0)

Maps **SPACX Intelligence Plugin** API paths (`plugin/manifest.yaml`) to agent-callable tools. Compliance level **2** — research, alerts, proposals only.

## Base

- **Plugin id:** `spacx-research-intelligence`
- **API base:** `/api/v1/spacx`
- **Runtime health:** `GET` equivalent → `python -m runtime.health` (local) or HTTP wrapper (future)

## Tool manifest (sketch)

| Tool name | HTTP | Runtime / stub | Agent consumers |
|-----------|------|----------------|-----------------|
| `spacx_ingest_source` | `POST /ingest/source` | `plugin.api.ingest` | SECFilingAgent, OnchainRWAAgent |
| `spacx_extract_events` | `POST /extract/events` | ingest pipeline | All ingest tiers |
| `spacx_metrics_update` | `POST /metrics/update` | `plugin.api.metrics` | Segment analysts |
| `spacx_metrics_read` | `GET /metrics/{asset}/{metric_id}` | registry + baselines | All analysts |
| `spacx_thesis_update` | `POST /thesis/update` | `plugin.api.thesis` | EvidenceAuditorAgent |
| `spacx_thesis_read` | `GET /thesis/{asset}` | thesis stub | Daily thesis gate |
| `spacx_risk_evaluate` | `POST /risk/evaluate` | `plugin.api.risk` | All (constraint layer) |
| `spacx_action_propose` | `POST /action/propose` | `plugin.api.risk.propose_action` | Human-over-the-loop |
| `spacx_alert_dispatch` | `POST /alert/dispatch` | `plugin.api.alerts` | P0 424B4, metric amber |
| `spacx_evidence_seal` | `POST /evidence/seal` | `runtime.persistence` + `plugin.api.evidence` | EvidenceAuditorAgent, OnchainRWAAgent |
| `spacx_report_generate` | `POST /report/generate` | `plugin.api.evidence.generate_report` | Thesis daily |
| `spacx_runtime_readiness` | — (local V0) | `runtime.health.readiness` | Orchestrator / Longter supervisor |
| `spacx_edgar_poll` | — (local V0) | `runtime.edgar_poll.poll_edgar` | SECFilingAgent |
| `spacx_worker_once` | — (local V0) | `runtime.worker.run_once` | Scheduler driver |

## Packet streams (agent adapters)

Runtime emits structured JSON via `runtime.packets` and `runtime_events` table:

| Packet | `packet_kind` | When |
|--------|---------------|------|
| Thesis update | `thesis_update` | After thesis API / daily gate (future) |
| Risk alert | `risk_alert` | Blocker or metric amber (V0: post EDGAR poll) |
| Next action (NAP) | `next_action` | Default `OBSERVE_ONLY` while blockers active |

Example NAP when 424B4 pending:

```json
{
  "packet_kind": "next_action",
  "action_type": "OBSERVE_ONLY",
  "priority": "P0",
  "blocked_by": ["FINAL_PROSPECTUS_PENDING", "LOCKUP_DAY0_UNKNOWN", "FIRST_EARNINGS_PENDING"],
  "target_agent": "SECFilingAgent",
  "requires_human_approval": true,
  "compliance_level": 2
}
```

## EDGAR events

| Event | Emitter | Human gate |
|-------|---------|------------|
| `filing.detected` | `edgar_poll` | — |
| `filing.detected` with `form: FWP` | `edgar_poll` | Evidence review only; does not clear 424B4 blockers |
| `filing.p0_424b4` | `edgar_poll` (Form 424B4) | `p0_424b4_review` |
| `filing.424b4_pending` | `edgar_poll` (no 424B4 in feed) | — |

## Scheduler alignment

| Tier | Cron (ET unless noted) | OpenClaw schedule hint |
|------|------------------------|-------------------------|
| `crypto_1_5m` | `*/5 * * * *` (UTC) | `spacx_worker_once --tiers crypto_1_5m` |
| `market_15m` | `*/15 * * * *` | 15m |
| `sec_1h` | `0 * * * *` (15m if `watch_424b4_active`) | **Live EDGAR in V0** |
| `evidence_6h` | `30 */6 * * *` | 6h |
| `space_4h` | `0 */4 * * *` | 4h |
| `float_daily` | `0 7 * * *` | daily |
| `thesis_daily` | `0 18 * * *` | daily + `thesis_publish` gate |

## Blocker flags (wire-up)

Synced from `plugin/metrics/baselines.json` + live EDGAR:

- `FINAL_PROSPECTUS_PENDING` — cleared when Form **424B4** in recent feed
- `LOCKUP_DAY0_UNKNOWN` — cleared when 424B4 present (prospectus anchor TBD until human `day0_anchor_confirmation`)
- `FIRST_EARNINGS_PENDING` — cleared when **10-Q** in recent feed

## Authentication (future)

V0: local process only. Phase 2+: API key or mTLS for `/api/v1/spacx/*`; runtime worker remains sidecar with shared SQLite path or event bus.
