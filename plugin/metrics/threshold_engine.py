"""Evaluate metric snapshots against registry.yaml thresholds (SEC Phase 1 baselines)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.yaml"
BASELINES_PATH = Path(__file__).resolve().parent / "baselines.json"


class Status(str, Enum):
    GREEN = "GREEN"
    AMBER = "AMBER"
    RED = "RED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


@dataclass
class MetricResult:
    metric_id: str
    status: Status
    value: Any
    reason: str | None = None


def load_registry(path: Path | None = None) -> dict[str, Any]:
    path = path or REGISTRY_PATH
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_baselines(path: Path | None = None) -> dict[str, Any]:
    path = path or BASELINES_PATH
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _compare(op: str, value: float, threshold: float) -> bool:
    if op == "lt":
        return value < threshold
    if op == "lte":
        return value <= threshold
    if op == "gt":
        return value > threshold
    if op == "gte":
        return value >= threshold
    if op == "eq":
        return value == threshold
    raise ValueError(f"Unsupported op: {op}")


def _qoq_growth(current: float, prior: float) -> float:
    if prior == 0:
        return float("inf") if current > 0 else 0.0
    return (current - prior) / prior


def _eval_threshold(
    threshold: dict[str, Any] | None,
    value: Any,
    *,
    prior_value: float | None = None,
    history: list[float] | None = None,
) -> tuple[bool, str | None]:
    if threshold is None:
        return False, None

    op = threshold.get("op")
    if op == "event":
        return False, None

    if op == "outside_pct_band":
        center = float(threshold["center"])
        pct = float(threshold["pct"]) / 100.0
        low, high = center * (1 - pct), center * (1 + pct)
        if value is None:
            return False, None
        v = float(value)
        if v < low or v > high:
            return True, f"outside ±{threshold['pct']}% of {center}"
        return False, None

    if op == "qoq_growth_lt":
        if prior_value is None:
            return False, None
        growth = _qoq_growth(float(value), float(prior_value))
        if growth < float(threshold["value"]):
            return True, f"QoQ growth {growth:.2%} < {threshold['value']:.0%}"
        return False, None

    if op == "delta_gt":
        if history is None or len(history) < 2:
            return False, None
        delta = abs(history[-1] - history[-2])
        if delta > float(threshold["value"]):
            return True, f"delta {delta:.2f} > {threshold['value']}"
        return False, None

    if op == "annualized_lt":
        # quarterly value annualized (×4) vs threshold
        if value is None:
            return False, None
        annualized = float(value) * 4
        if annualized < float(threshold["value"]):
            return True, f"annualized {annualized:.0f} < {threshold['value']}"
        return False, None

    if value is None:
        return False, None

    if op in ("lt", "lte", "gt", "gte", "eq"):
        triggered = _compare(op, float(value), float(threshold["value"]))
        if not triggered:
            return False, None
        cq = threshold.get("consecutive_quarters")
        if cq:
            if not history or len(history) < int(cq):
                return False, None
            t = float(threshold["value"])
            window = history[-int(cq) :]
            if not all(_compare(op, float(v), t) for v in window):
                return False, None
        return True, f"{op} {threshold['value']}"

    return False, None


def evaluate_metric(
    metric_def: dict[str, Any],
    snapshot: dict[str, Any],
    *,
    as_of: str | None = None,
) -> MetricResult:
    metric_id = metric_def["metric_id"]
    value = snapshot.get("values", {}).get(metric_id, snapshot.get(metric_id))
    prior = snapshot.get("prior", {}).get(metric_id)
    history = snapshot.get("history", {}).get(metric_id)

    if value is None and metric_def.get("red_threshold", {}) is None:
        return MetricResult(metric_id, Status.UNKNOWN, value, "no snapshot value")

    red = metric_def.get("red_threshold")
    amber = metric_def.get("amber_threshold")

    # boolean milestone red only after deadline (as_of), not on pre-milestone false
    if (
        red
        and red.get("op") == "eq"
        and red.get("value") is False
        and value is False
        and red.get("as_of")
    ):
        if not as_of or as_of < red["as_of"]:
            red = None

    red_hit, red_reason = _eval_threshold(red, value, prior_value=prior, history=history)
    if red_hit:
        return MetricResult(metric_id, Status.RED, value, red_reason)

    amber_hit, amber_reason = _eval_threshold(
        amber, value, prior_value=prior, history=history
    )
    if amber_hit:
        return MetricResult(metric_id, Status.AMBER, value, amber_reason)

    if value is None:
        return MetricResult(metric_id, Status.UNKNOWN, value, "no snapshot value")

    return MetricResult(metric_id, Status.GREEN, value, None)


def _iter_metric_defs(registry: dict[str, Any]) -> list[dict[str, Any]]:
    defs: list[dict[str, Any]] = []
    defs.extend(registry.get("watch_metrics", []))
    defs.extend(registry.get("governance_metrics", []))
    for fw in registry.get("flywheels", {}).values():
        defs.extend(fw.get("metrics", []))
    return defs


def evaluate_snapshot(
    snapshot: dict[str, Any],
    *,
    registry: dict[str, Any] | None = None,
    as_of: str | None = None,
    apply_blockers: bool = True,
) -> dict[str, Any]:
    registry = registry or load_registry()
    results: dict[str, MetricResult] = {}

    for metric_def in _iter_metric_defs(registry):
        results[metric_def["metric_id"]] = evaluate_metric(
            metric_def, snapshot, as_of=as_of
        )

    blockers: list[dict[str, Any]] = []
    if apply_blockers:
        active_flags = snapshot.get("blockers") or {}
        for b in registry.get("blockers", []):
            fid = b["flag_id"]
            if active_flags.get(fid, b.get("active", False)):
                blockers.append(
                    {
                        "flag_id": fid,
                        "status": Status.BLOCKED.value,
                        "description": b.get("description"),
                    }
                )

    counts = {s.value: 0 for s in Status}
    for r in results.values():
        counts[r.status.value] = counts.get(r.status.value, 0) + 1

    return {
        "asset": registry.get("asset", "SPCX"),
        "as_of": as_of or snapshot.get("as_of"),
        "blockers": blockers,
        "metrics": {
            mid: {
                "status": r.status.value,
                "value": r.value,
                "reason": r.reason,
            }
            for mid, r in results.items()
        },
        "summary": counts,
    }


def baseline_snapshot(baselines: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a snapshot from exported SEC baselines (Q1 2026)."""
    baselines = baselines or load_baselines()
    values: dict[str, Any] = {}
    for section in ("watch", "governance", "flywheel_starlink", "flywheel_ai", "flywheel_starship"):
        values.update(baselines.get(section, {}))
    return {
        "as_of": "2026-03-31",
        "values": values,
        "prior": {
            "W03_starlink_subscribers_m": 8.9,
            "F_SL01_starlink_subscribers_m": 8.9,
        },
        "blockers": baselines.get("blockers", {}),
    }


def sample_evaluations() -> dict[str, Any]:
    """Run baseline (GREEN) and stressed (AMBER/RED) sample evaluations."""
    registry = load_registry()
    baselines = load_baselines()

    green = evaluate_snapshot(baseline_snapshot(baselines), registry=registry)

    amber_snapshot = {
        "as_of": "2026-06-30",
        "values": {
            **baseline_snapshot(baselines)["values"],
            "W03_starlink_subscribers_m": 10.5,
            "F_SL01_starlink_subscribers_m": 10.5,
            "W04_starlink_arpu_usd_mo": 58,
            "F_SL02_starlink_arpu_usd_mo": 58,
            "W08_ai_capex_to_revenue_ratio": 10.5,
            "F_AI05_ai_capex_to_revenue_ratio": 10.5,
        },
        "prior": {
            "W03_starlink_subscribers_m": 10.3,
            "F_SL01_starlink_subscribers_m": 10.3,
            "W04_starlink_arpu_usd_mo": 61,
            "F_SL02_starlink_arpu_usd_mo": 61,
        },
        "history": {
            "W04_starlink_arpu_usd_mo": [59.0, 58.0],
            "F_SL02_starlink_arpu_usd_mo": [59.0, 58.0],
            "W08_ai_capex_to_revenue_ratio": [10.2, 10.5],
            "F_AI05_ai_capex_to_revenue_ratio": [10.2, 10.5],
        },
        "blockers": {
            "FINAL_PROSPECTUS_PENDING": False,
            "LOCKUP_DAY0_UNKNOWN": False,
            "FIRST_EARNINGS_PENDING": True,
        },
    }
    stressed = evaluate_snapshot(amber_snapshot, registry=registry)

    return {"baseline_q1_2026": green, "stressed_q2_2026": stressed}


def metric_count(registry: dict[str, Any] | None = None) -> dict[str, int]:
    registry = registry or load_registry()
    watch = len(registry.get("watch_metrics", []))
    gov = len(registry.get("governance_metrics", []))
    fly = sum(
        len(fw.get("metrics", [])) for fw in registry.get("flywheels", {}).values()
    )
    return {
        "watch": watch,
        "governance": gov,
        "flywheel": fly,
        "total_scored": watch + gov + fly,
        "blockers": len(registry.get("blockers", [])),
    }


if __name__ == "__main__":
    counts = metric_count()
    samples = sample_evaluations()
    print(json.dumps({"metric_count": counts, "samples": samples}, indent=2))
