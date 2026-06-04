"""
Anomaly detection: metric threshold breaches → AMBER / RED triggers.

Aligns with Phase 1 twelve watch metrics and Track C thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Sequence

from plugin.models._types import (
    AlertLevel,
    AuditRecord,
    DataRequirement,
    ModelPhase,
    ModelResult,
    stable_hash,
)


class Comparator(str, Enum):
    GT = "gt"
    LT = "lt"
    GTE = "gte"
    LTE = "lte"
    ABS_CHANGE_PCT = "abs_change_pct"


@dataclass(frozen=True)
class MetricThreshold:
    metric_id: str
    amber: float | None = None
    red: float | None = None
    comparator: Comparator = Comparator.GT
    unit: str = ""
    description: str = ""


@dataclass(frozen=True)
class MetricObservation:
    metric_id: str
    value: float
    as_of: str
    baseline: float | None = None


@dataclass
class AnomalyTrigger:
    metric_id: str
    level: AlertLevel
    observed: float
    threshold: float
    message: str


# Phase 1 seed thresholds (subset; extend via metrics registry)
DEFAULT_THRESHOLDS: tuple[MetricThreshold, ...] = (
    MetricThreshold(
        "ipo_price_vs_baseline",
        amber=0.05,
        red=0.10,
        comparator=Comparator.ABS_CHANGE_PCT,
        unit="pct",
        description="424B4 price vs $135 S-1/A baseline",
    ),
    MetricThreshold(
        "anthropic_revenue_vs_run_rate",
        amber=0.85,
        red=0.70,
        comparator=Comparator.LT,
        unit="ratio",
        description="Recognized / $1.25B/mo run-rate",
    ),
    MetricThreshold(
        "ai_capex_to_revenue",
        amber=8.0,
        red=10.0,
        comparator=Comparator.GT,
        unit="x",
        description="AI capex / revenue (Q1 2026 baseline ~9.4x)",
    ),
    MetricThreshold(
        "musk_voting_power",
        amber=0.80,
        red=0.85,
        comparator=Comparator.GT,
        unit="pct",
        description="Musk voting % (~82.4% at IPO)",
    ),
    MetricThreshold(
        "starship_milestone_slip",
        amber=1,
        red=1,
        comparator=Comparator.GTE,
        unit="flag",
        description="No orbit milestone by YE2026 → red",
    ),
)


class AnomalyDetectionModel:
    MODEL_NAME = "anomaly_detection"
    VERSION = "0.1.0"

    PHASE3_REQUIREMENTS: tuple[DataRequirement, ...] = (
        DataRequirement(
            "metrics_registry_snapshot",
            "metrics_registry",
            "daily",
            3,
            "Current values for 12 CFA watch metrics.",
        ),
        DataRequirement(
            "threshold_policy_version",
            "config",
            "on_change",
            3,
            "Versioned amber/red thresholds per metric_id.",
        ),
    )

    def _compare(self, comp: Comparator, value: float, threshold: float, baseline: float | None) -> bool:
        if comp == Comparator.ABS_CHANGE_PCT:
            if baseline is None or baseline == 0:
                return False
            return abs((value - baseline) / baseline) >= threshold
        if comp == Comparator.GT:
            return value > threshold
        if comp == Comparator.GTE:
            return value >= threshold
        if comp == Comparator.LT:
            return value < threshold
        if comp == Comparator.LTE:
            return value <= threshold
        return False

    def evaluate(
        self,
        observations: Sequence[MetricObservation],
        thresholds: Sequence[MetricThreshold] | None = None,
    ) -> list[AnomalyTrigger]:
        rules = {t.metric_id: t for t in (thresholds or DEFAULT_THRESHOLDS)}
        obs_map = {o.metric_id: o for o in observations}
        triggers: list[AnomalyTrigger] = []

        for mid, rule in rules.items():
            obs = obs_map.get(mid)
            if obs is None:
                continue
            for level_name, bound in (("red", rule.red), ("amber", rule.amber)):
                if bound is None:
                    continue
                if self._compare(rule.comparator, obs.value, bound, obs.baseline):
                    level = AlertLevel.RED if level_name == "red" else AlertLevel.AMBER
                    triggers.append(
                        AnomalyTrigger(
                            metric_id=mid,
                            level=level,
                            observed=obs.value,
                            threshold=bound,
                            message=f"{mid}: {obs.value} breached {level_name} ({bound})",
                        )
                    )
                    break
        return triggers

    def run(
        self,
        observations: Sequence[MetricObservation] | None = None,
        *,
        thresholds: Sequence[MetricThreshold] | None = None,
        run_id: str | None = None,
    ) -> ModelResult:
        obs = list(observations or [])
        triggers = self.evaluate(obs, thresholds)
        worst: Literal["GREEN", "AMBER", "RED"] = "GREEN"
        if any(t.level == AlertLevel.RED for t in triggers):
            worst = "RED"
        elif triggers:
            worst = "AMBER"

        ts = datetime.utcnow()
        rid = run_id or stable_hash([self.MODEL_NAME, worst, str(len(triggers))])
        audit = AuditRecord(
            model=self.MODEL_NAME,
            version=self.VERSION,
            run_id=rid,
            timestamp=ts,
            inputs_hash=stable_hash([o.metric_id for o in obs]),
            parameters={"n_rules": len(thresholds or DEFAULT_THRESHOLDS)},
            outputs={"worst_level": worst, "n_triggers": len(triggers)},
        )
        return ModelResult(
            model_name=self.MODEL_NAME,
            phase=ModelPhase.V0,
            payload={
                "worst_level": worst,
                "triggers": [
                    {
                        "metric_id": t.metric_id,
                        "level": t.level.value,
                        "observed": t.observed,
                        "threshold": t.threshold,
                        "message": t.message,
                    }
                    for t in triggers
                ],
                "default_threshold_metric_ids": [t.metric_id for t in DEFAULT_THRESHOLDS],
            },
            audit=audit,
            data_gaps=list(self.PHASE3_REQUIREMENTS) if not obs else [],
        )


def run_anomaly_detection(
    observations: Sequence[MetricObservation] | None = None,
) -> ModelResult:
    return AnomalyDetectionModel().run(observations)
