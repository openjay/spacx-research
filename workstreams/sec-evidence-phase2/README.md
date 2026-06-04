# SEC Evidence — Phase 2 (Watchlist & Quality Tables)

Phase 2 turns Phase 1 SEC extractions into a **machine-readable metric registry** and **segment flywheel quality tables** for ongoing SPCX monitoring.

---

## Phase 1 (source of truth)

| Document | Role |
|----------|------|
| [00-phase1-summary.md](../sec-evidence-phase1/00-phase1-summary.md) | Executive synthesis |
| [05-master-evidence-tables.md](../sec-evidence-phase1/audit/05-master-evidence-tables.md) | Corrected offering, segment, and watch baselines |
| [03-risk-metrics-map.md](../sec-evidence-phase1/03-risk-metrics-map.md) | Risk theme → metric mapping |
| [C-risk-disclosure-audit.md](../sec-evidence-phase1/audit/C-risk-disclosure-audit.md) | §4 twelve watch metrics + thresholds |

---

## Phase 2 deliverables

| File | Description |
|------|-------------|
| [starlink-quality.md](./starlink-quality.md) | Connectivity / Starlink KPIs (subs, ARPU, EBITDA, capex, margin, V3) |
| [ai-compute-quality.md](./ai-compute-quality.md) | AI segment economics + Anthropic contract |
| [starship-milestones.md](./starship-milestones.md) | Space launch cadence + Starship milestones |

---

## Plugin registry (machine-readable)

| Path | Description |
|------|-------------|
| [`plugin/metrics/registry.yaml`](../../plugin/metrics/registry.yaml) | 12 watch metrics, 7 governance metrics, 3 flywheels (21 flywheel metrics), 3 blocker flags |
| [`plugin/metrics/baselines.json`](../../plugin/metrics/baselines.json) | Numeric SEC baselines (Q1 2026) |
| [`plugin/metrics/threshold_engine.py`](../../plugin/metrics/threshold_engine.py) | Snapshot → GREEN / AMBER / RED evaluation |

### Active blockers (pre-IPO)

- `FINAL_PROSPECTUS_PENDING` — 424B4 not filed  
- `LOCKUP_DAY0_UNKNOWN` — prospectus anchor date TBD  
- `FIRST_EARNINGS_PENDING` — lock-up earnings gates unknown  

### Quick evaluate

```bash
python plugin/metrics/threshold_engine.py
```

---

*Proposed / expected listing symbol: **SPCX** (Space Exploration Technologies Corp.; pending Form 424B4 and first trading confirmation). SEC CIK 0001181412.*
