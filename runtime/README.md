# SPACX V0 runtime

Read-only worker for **Longter / OpenClaw** 24/7 agent integration. Not production trading.

## Quick start

From repository root (`spacx/`):

```bash
# One scheduler pass (EDGAR poll + tier stubs)
python -m runtime.worker --once

# JSON envelope to stdout
python -m runtime.worker --once --json

# Readiness gates (CLI)
python -m runtime.health

# Live EDGAR refresh + readiness
python -m runtime.health --refresh-edgar

# EDGAR poll only
python -m runtime.edgar_poll
```

Requires **Python 3.11+** and PyYAML (`pip install pyyaml` if not already available).

## Layout

| Module | Role |
|--------|------|
| `worker.py` | Main loop; reads `plugin/scheduler.yaml` tiers |
| `edgar_poll.py` | CIK `0001181412` submissions feed; 424B4 / 10-Q watch |
| `persistence.py` | SQLite + JSONL under `runtime/data/` (gitignored) |
| `health.py` | `readiness()` gates for orchestrators |
| `packets.py` | `ThesisUpdatePacket`, `RiskAlertPacket`, `NAP` |
| `openclaw_adapter.md` | Tool manifest sketch for agent adapters |

## Readiness gates

`python -m runtime.health` returns:

| Field | Meaning |
|-------|---------|
| `sec_cache_ok` | Last EDGAR state available or successful poll |
| `blocker_flags` | `FINAL_PROSPECTUS_PENDING`, `LOCKUP_DAY0_UNKNOWN`, `FIRST_EARNINGS_PENDING` |
| `last_edgar_check` | ISO timestamp of last poll |
| `schema_contract_ok` | Required `plugin/schemas/*.json` present and valid |
| `ready` | `sec_cache_ok` ∧ `schema_contract_ok` (observation worker; blockers may still be active) |

Blockers are sourced from `plugin/metrics/baselines.json` and updated live when **424B4** or **10-Q** appear in the EDGAR recent feed.

## SEC EDGAR

Set a descriptive User-Agent (SEC policy):

```bash
export SPACX_SEC_USER_AGENT="YourOrg YourApp (contact: you@example.com)"
```

No **424B4** in feed → `status_424b4: pending` and `FINAL_PROSPECTUS_PENDING: true`.

## Scheduler tiers (V0)

| Tier | V0 behavior |
|------|-------------|
| `sec_1h` | Live `edgar_poll` + risk/NAP packets |
| `crypto_1_5m`, `market_15m`, … | Stub dispatch logged |
| `thesis_daily` | Stub; human gate `thesis_publish` |

Full orchestration: [`plugin/scheduler.yaml`](../plugin/scheduler.yaml), [`docs/AGENTS.md`](../docs/AGENTS.md).

## Data directory

- `runtime/data/spacx_v0.db` — seals, receipts, snapshots, events
- `runtime/data/jsonl/*.jsonl` — optional tail for agents

See [`docs/RUNTIME.md`](../docs/RUNTIME.md) for scope, blockers, and eight-agent integration.
