"""
Forecast scoring: Brier score and hit rate per agent predictions.

V0: binary and binned probability forecasts without external deps.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Sequence

from plugin.models._types import (
    AuditRecord,
    DataRequirement,
    ModelPhase,
    ModelResult,
    stable_hash,
)


@dataclass(frozen=True)
class AgentForecast:
    agent_id: str
    forecast_id: str
    event_id: str
    probability: float  # P(event)
    outcome: bool | None = None  # resolved after event
    brier_weight: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("probability must be in [0, 1]")


@dataclass
class AgentScorecard:
    agent_id: str
    n_resolved: int
    hit_rate: float
    brier_score: float
    forecasts: list[str]


class ForecastScoringModel:
    MODEL_NAME = "forecast_scoring"
    VERSION = "0.1.0"

    PHASE3_REQUIREMENTS: tuple[DataRequirement, ...] = (
        DataRequirement(
            "resolved_event_outcomes",
            "metrics_registry",
            "event",
            3,
            "Ground truth for forecast event_ids.",
        ),
        DataRequirement(
            "agent_forecast_log",
            "thesis_engine",
            "on_demand",
            3,
            "Immutable log of agent predictions with timestamps.",
        ),
    )

    @staticmethod
    def brier(probability: float, outcome: bool) -> float:
        y = 1.0 if outcome else 0.0
        return (probability - y) ** 2

    def score_agent(self, forecasts: Sequence[AgentForecast], agent_id: str) -> AgentScorecard:
        resolved = [f for f in forecasts if f.agent_id == agent_id and f.outcome is not None]
        if not resolved:
            return AgentScorecard(
                agent_id=agent_id,
                n_resolved=0,
                hit_rate=0.0,
                brier_score=0.0,
                forecasts=[],
            )
        hits = 0
        brier_sum = 0.0
        weight_sum = 0.0
        ids: list[str] = []
        for f in resolved:
            assert f.outcome is not None
            pred_positive = f.probability >= 0.5
            if pred_positive == f.outcome:
                hits += 1
            w = f.brier_weight
            brier_sum += self.brier(f.probability, f.outcome) * w
            weight_sum += w
            ids.append(f.forecast_id)
        n = len(resolved)
        return AgentScorecard(
            agent_id=agent_id,
            n_resolved=n,
            hit_rate=hits / n,
            brier_score=brier_sum / weight_sum if weight_sum else 0.0,
            forecasts=ids,
        )

    def run(
        self,
        forecasts: Sequence[AgentForecast] | None = None,
        *,
        run_id: str | None = None,
    ) -> ModelResult:
        fc = list(forecasts or [])
        agents = sorted({f.agent_id for f in fc})
        scorecards: dict[str, Any] = {}
        for aid in agents:
            sc = self.score_agent(fc, aid)
            scorecards[aid] = {
                "n_resolved": sc.n_resolved,
                "hit_rate": sc.hit_rate,
                "brier_score": sc.brier_score,
                "forecast_ids": sc.forecasts,
            }

        # Pool Brier across all resolved
        resolved_all = [f for f in fc if f.outcome is not None]
        pool_brier = (
            sum(self.brier(f.probability, f.outcome) for f in resolved_all) / len(resolved_all)
            if resolved_all
            else None
        )

        ts = datetime.now(timezone.utc)
        rid = run_id or stable_hash([self.MODEL_NAME, str(len(fc))])
        audit = AuditRecord(
            model=self.MODEL_NAME,
            version=self.VERSION,
            run_id=rid,
            timestamp=ts,
            inputs_hash=stable_hash([f.forecast_id for f in fc]),
            parameters={"n_forecasts": len(fc)},
            outputs={"pool_brier": pool_brier, "agents": agents},
        )
        return ModelResult(
            model_name=self.MODEL_NAME,
            phase=ModelPhase.V0,
            payload={
                "scorecards": scorecards,
                "pool_brier": pool_brier,
                "n_unresolved": sum(1 for f in fc if f.outcome is None),
            },
            audit=audit,
            data_gaps=list(self.PHASE3_REQUIREMENTS) if not resolved_all else [],
        )


def run_forecast_scoring(forecasts: Sequence[AgentForecast] | None = None) -> ModelResult:
    return ForecastScoringModel().run(forecasts)
