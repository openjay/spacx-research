"""
Macro / thematic regime labels for SPCX monitoring.

V0: rule-based classifier on scalar feature vector; HMM/GMM in Phase 3.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from plugin.models._types import (
    AuditRecord,
    DataRequirement,
    ModelPhase,
    ModelResult,
    stable_hash,
)

REGIME_LABELS = frozenset(
    {
        "ai_risk_on",
        "capex_skepticism",
        "ipo_boom",
        "rates_shock",
        "governance_discount",
        "supply_overhang",
        "connectivity_growth",
        "neutral",
    }
)


@dataclass(frozen=True)
class RegimeFeatures:
    """
    Normalized features in roughly [-1, 1] or [0, 1].

    Phase 3: estimated from market + SEC metric feeds.
    """

    ai_sentiment: float = 0.0
    capex_intensity: float = 0.0  # high = skepticism trigger
    ipo_heat: float = 0.0
    rates_beta: float = 0.0
    governance_stress: float = 0.0
    float_pressure: float = 0.0
    starlink_growth: float = 0.0


@dataclass(frozen=True)
class RegimeClassification:
    primary: str
    secondary: str | None
    scores: dict[str, float]


class RegimeDetectionModel:
    MODEL_NAME = "regime_detection"
    VERSION = "0.1.0"

    PHASE3_REQUIREMENTS: tuple[DataRequirement, ...] = (
        DataRequirement(
            "macro_rates_proxy",
            "fred_or_vendor",
            "daily",
            3,
            "2Y/10Y moves, real yields for rates_shock.",
        ),
        DataRequirement(
            "ai_sector_breadth",
            "market_data_provider",
            "daily",
            3,
            "NVDA / hyperscaler basket momentum for ai_risk_on.",
        ),
        DataRequirement(
            "spcx_implied_vol_and_volume",
            "market_data_provider",
            "daily",
            3,
            "IPO-era liquidity and vol for ipo_boom / supply_overhang.",
        ),
    )

    def score_regimes(self, features: RegimeFeatures) -> dict[str, float]:
        """Heuristic scores — higher = stronger match (V0)."""
        f = features
        return {
            "ai_risk_on": max(0.0, f.ai_sentiment) * (1.0 - min(1.0, f.capex_intensity)),
            "capex_skepticism": min(1.0, f.capex_intensity) * (1.0 - max(0.0, f.ai_sentiment) * 0.5),
            "ipo_boom": min(1.0, f.ipo_heat),
            "rates_shock": min(1.0, abs(f.rates_beta)),
            "governance_discount": min(1.0, f.governance_stress),
            "supply_overhang": min(1.0, f.float_pressure),
            "connectivity_growth": max(0.0, f.starlink_growth),
            "neutral": 0.15,
        }

    def classify(self, features: RegimeFeatures) -> RegimeClassification:
        scores = self.score_regimes(features)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary, top = ranked[0]
        secondary = ranked[1][0] if len(ranked) > 1 and ranked[1][1] > top * 0.85 else None
        if top < 0.2:
            primary = "neutral"
            secondary = None
        return RegimeClassification(primary=primary, secondary=secondary, scores=scores)

    def run(
        self,
        features: RegimeFeatures | None = None,
        *,
        run_id: str | None = None,
    ) -> ModelResult:
        feats = features or RegimeFeatures()
        clf = self.classify(feats)
        ts = datetime.now(timezone.utc)
        rid = run_id or stable_hash([self.MODEL_NAME, clf.primary])
        audit = AuditRecord(
            model=self.MODEL_NAME,
            version=self.VERSION,
            run_id=rid,
            timestamp=ts,
            inputs_hash=stable_hash([str(feats)]),
            parameters={},
            outputs={"primary": clf.primary, "secondary": clf.secondary},
        )
        return ModelResult(
            model_name=self.MODEL_NAME,
            phase=ModelPhase.V0,
            payload={
                "primary_regime": clf.primary,
                "secondary_regime": clf.secondary,
                "scores": clf.scores,
                "labels": sorted(REGIME_LABELS),
            },
            audit=audit,
            data_gaps=list(self.PHASE3_REQUIREMENTS),
        )


def run_regime_detection(features: RegimeFeatures | None = None) -> ModelResult:
    return RegimeDetectionModel().run(features)
