# SPACX statistical models (V0)

Research-grade, **auditable** Python modules for **SPCX** monitoring. V0 ships interfaces, stub estimators, and explicit **Phase 3 data contracts** — no live market feed required.

**Disclaimer:** Research tooling only; not investment advice.

---

## Module index

| Module | Purpose | V0 estimator | Phase 3 data |
|--------|---------|--------------|--------------|
| `event_study.py` | Abnormal return / volume around events | Mean-adjusted CAR | Daily OHLCV, event calendar |
| `bayesian_thesis.py` | P(thesis \| evidence) | Log-odds + LR packets | Calibrated LRs, evidence schema |
| `regime_detection.py` | Macro/thematic regime labels | Rule-based scores | Rates, AI breadth, SPCX vol |
| `factor_exposure.py` | Factor betas vs peers | OLS stub / priors | FF + AI_GROWTH, peer returns |
| `anomaly_detection.py` | Metric breaches → AMBER/RED | Threshold rules | Metrics registry snapshot |
| `portfolio_risk_budget.py` | Position & thematic caps | Policy checker | Holdings, NAV limits |
| `forecast_scoring.py` | Agent forecast quality | Brier + hit rate | Resolved outcomes log |

---

## CFA-style methodology notes

### 1. Event study (`event_study.py`)

**Question:** Did returns or volume around a corporate event differ from “normal”?

**Method (V0):**

- Estimation window: default 120 trading days ending day −1 before the event.
- Event window: [−5, +20] calendar days around `event_date` (configurable).
- Expected return: mean return in the estimation window (market-model **stub**; benchmark OLS in Phase 3).
- Abnormal return (AR): \( AR_t = R_t - \hat{\mu} \).
- Cumulative abnormal return (CAR): sum of AR over the event window.
- Volume: z-score vs estimation-window mean/variance when volume is supplied.

**Event types:** `424B4`, `earnings`, `lock_up`, `starship_milestone`, `sec_amendment`, `index_inclusion`.

**Audit:** Each `run()` emits `AuditRecord` with `inputs_hash`, window parameters, and CAR.

**Phase 3:** Align trading calendar; use market-model or Fama-French adjusted returns; peer basket for launch-adjacent noise.

---

### 2. Bayesian thesis (`bayesian_thesis.py`)

**Question:** How should belief in each structural thesis change given new evidence?

**Thesis keys (five):**

| Key | Phase 1 anchor |
|-----|----------------|
| `connectivity_starlink` | Starlink users, ARPU, Connectivity EBITDA |
| `space_starship_execution` | Launches, Starship orbit, FAA |
| `ai_capex_monetization` | AI capex/revenue, Anthropic recognition |
| `governance_control` | Musk voting %, controlled company, RPT |
| `supply_lockup_float` | Staged lock-up, float path |

**Method (V0):**

- Prior \( P_0 \) per thesis (defaults from observation framework).
- Evidence packets carry `likelihood_ratio` and `confidence` dampener.
- Update: \( \text{logit}(P_{n+1}) = \text{logit}(P_n) + \ln(LR \cdot \text{confidence}) \).
- Theses updated **independently** in V0 (no covariance matrix).

**Audit:** Posteriors and applied `packet_id` list per thesis.

**Phase 3:** Calibrate LRs from historical SEC deltas; optional hierarchical model across agents.

---

### 3. Regime detection (`regime_detection.py`)

**Question:** Which macro/thematic label best describes the current environment for sizing and narrative?

**Labels:** `ai_risk_on`, `capex_skepticism`, `ipo_boom`, `rates_shock`, `governance_discount`, `supply_overhang`, `connectivity_growth`, `neutral`.

**Method (V0):** Score each label from normalized `RegimeFeatures`; primary = argmax; secondary if runner-up ≥ 85% of top score.

**Audit:** Full score vector stored in payload.

**Phase 3:** Hidden Markov or k-means on feature history; backtest regime persistence.

---

### 4. Factor exposure (`factor_exposure.py`)

**Question:** How does SPCX co-move with market, style, and AI-growth factors vs peers (e.g. NVDA)?

**Factors (default):** `MKT`, `SMB`, `HML`, `MTUM`, `AI_GROWTH`, `RATES`, `SPACE_INDUSTRIAL`.

**Peers (default):** NVDA, RKLB, ASTS, GOOGL, AMZN.

**Method (V0):** Single-factor OLS beta when return series provided; otherwise documented **prior stub** betas.

**Audit:** Mode `prior_stub` vs `ols_v0` recorded.

**Phase 3:** Rolling multi-factor regression, Newey-West standard errors, R².

---

### 5. Anomaly detection (`anomaly_detection.py`)

**Question:** Which watch metrics breached amber/red thresholds?

**Method (V0):** Deterministic comparators (`gt`, `lt`, `gte`, `lte`, `abs_change_pct`) on `MetricObservation` vs `MetricThreshold`.

**Seeded metrics:** IPO price vs $135 baseline, Anthropic run-rate ratio, AI capex/revenue, Musk voting %, Starship slip flag.

**Output:** `worst_level` ∈ {GREEN, AMBER, RED} and trigger list.

**Phase 3:** Thresholds owned by **metrics registry** version file; no hardcoding in code paths.

---

### 6. Portfolio risk budget (`portfolio_risk_budget.py`)

**Question:** Does a proposed book violate observation-sleeve limits?

**Policy (default):**

- **SPCX max position:** 1% (`max_position_pct = 0.01`).
- Thematic cap: 40% per bucket (`connectivity`, `space`, `ai_compute`, …).
- Non-SPCX single name: 5%.
- Minimum cash: 10%.

**Method (V0):** Sum-check weights; emit `BudgetViolation` with `block` vs `warn`.

**Phase 3:** Tie to OMS holdings and firm risk config overrides.

---

### 7. Forecast scoring (`forecast_scoring.py`)

**Question:** Which agents produce well-calibrated binary forecasts?

**Method (V0):**

- **Brier score:** \( BS = \frac{1}{N}\sum (p_i - y_i)^2 \) (lower is better).
- **Hit rate:** fraction where \(\mathbb{1}_{p \ge 0.5} = y\).

**Audit:** Per-agent scorecards + pool Brier.

**Phase 3:** Link `event_id` to metrics registry resolutions; proper scoring rules for continuous targets.

---

## Usage

```python
from plugin.models import run_bayesian_thesis, EvidencePacket

packets = [
    EvidencePacket(
        packet_id="sec-q1-starlink",
        thesis_key="connectivity_starlink",
        summary="Starlink 10.3M users Q1 2026",
        likelihood_ratio=1.15,
        source="sec_filing",
    ),
]
result = run_bayesian_thesis(packets)
print(result.payload["theses"]["connectivity_starlink"]["posterior"])
print(result.audit.to_dict())
```

---

## Versioning

- **V0:** Interfaces + pure Python math; optional numpy/pandas not required.
- **V1:** Vectorized estimators behind same `run()` contracts.
- **V2:** Live feeds + scheduled jobs (Workstream 3).

See [docs/MODELS.md](../../docs/MODELS.md) for integration with metrics registry and thesis engine.
