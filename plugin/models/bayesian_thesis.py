"""
Bayesian thesis updater: P(thesis | evidence packets).

Six canonical thesis keys per ``schemas/ThesisState.json``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from plugin.models._types import (
    AuditRecord,
    DataRequirement,
    ModelPhase,
    ModelResult,
    stable_hash,
)
from plugin.models.thesis_keys import (
    THESIS_DESCRIPTIONS,
    THESIS_KEYS,
    normalize_thesis_key,
    probability_to_status,
)

# Re-export for ``plugin.models`` package consumers
__all__ = [
    "THESIS_KEYS",
    "BayesianThesisModel",
    "EvidencePacket",
    "ThesisState",
    "run_bayesian_thesis",
    "to_thesis_state_dict",
]


@dataclass(frozen=True)
class EvidencePacket:
    """
    Agent- or human-submitted evidence with likelihood weights.

    likelihood_ratio > 1 supports thesis; < 1 weighs against.
    """

    packet_id: str
    thesis_key: str
    summary: str
    likelihood_ratio: float
    source: str = "sec_filing"
    confidence: float = 1.0  # 0–1 dampener on log-LR

    def __post_init__(self) -> None:
        object.__setattr__(self, "thesis_key", normalize_thesis_key(self.thesis_key))
        if self.likelihood_ratio <= 0:
            raise ValueError("likelihood_ratio must be positive")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")


@dataclass
class ThesisState:
    thesis_key: str
    prior: float
    posterior: float
    log_odds: float
    packets_applied: list[str]


def to_thesis_state_dict(
    *,
    asset: str = "SPCX",
    thesis_key: str,
    probability: float,
    last_updated_at: str | None = None,
    evidence_refs: list[str] | None = None,
    last_update_reason: str | None = None,
) -> dict[str, Any]:
    """Build a ``ThesisState.json``-compatible record."""
    key = normalize_thesis_key(thesis_key)
    return {
        "asset": asset,
        "thesis_key": key,
        "thesis": THESIS_DESCRIPTIONS[key],
        "probability": float(probability),
        "status": probability_to_status(float(probability)),
        "last_updated_at": last_updated_at
        or datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "evidence_refs": list(evidence_refs or []),
        **({"last_update_reason": last_update_reason} if last_update_reason else {}),
        "model_version": "bayesian_thesis_v0",
    }


class BayesianThesisModel:
    """Sequential log-odds update (V0); full MCMC deferred to Phase 3."""

    MODEL_NAME = "bayesian_thesis"
    VERSION = "0.1.0"

    DEFAULT_PRIORS: dict[str, float] = {
        "STARLINK_CASHFLOW_STRONG": 0.55,
        "STARSHIP_COST_CURVE": 0.45,
        "AI_HIGH_QUALITY_REVENUE": 0.40,
        "GOVERNANCE_DISCOUNT_EXPANDS": 0.35,
        "LOCKUP_OVERWHELMS_DEMAND": 0.50,
        "VALUATION_REASONABLE": 0.45,
    }

    PHASE3_REQUIREMENTS: tuple[DataRequirement, ...] = (
        DataRequirement(
            "structured_evidence_packets",
            "thesis_engine",
            "on_demand",
            3,
            "Parsed SEC deltas, earnings KPIs, agent summaries with citations.",
        ),
        DataRequirement(
            "calibrated_likelihood_table",
            "research_calibration",
            "quarterly",
            3,
            "Historical hit rates per evidence type → LR priors.",
        ),
    )

    @staticmethod
    def _prob_to_log_odds(p: float) -> float:
        p = min(max(p, 1e-6), 1.0 - 1e-6)
        return math.log(p / (1.0 - p))

    @staticmethod
    def _log_odds_to_prob(lo: float) -> float:
        return 1.0 / (1.0 + math.exp(-lo))

    def update(
        self,
        thesis_key: str,
        prior: float | None,
        packets: Sequence[EvidencePacket],
    ) -> ThesisState:
        key = normalize_thesis_key(thesis_key)
        p0 = prior if prior is not None else self.DEFAULT_PRIORS[key]
        lo = self._prob_to_log_odds(p0)
        applied: list[str] = []
        for pkt in packets:
            if pkt.thesis_key != key:
                continue
            lr_eff = pkt.likelihood_ratio**pkt.confidence
            lo += math.log(lr_eff)
            applied.append(pkt.packet_id)
        post = self._log_odds_to_prob(lo)
        return ThesisState(
            thesis_key=key,
            prior=p0,
            posterior=post,
            log_odds=lo,
            packets_applied=applied,
        )

    def run(
        self,
        packets: Sequence[EvidencePacket],
        *,
        priors: Mapping[str, float] | None = None,
        run_id: str | None = None,
        asset: str = "SPCX",
    ) -> ModelResult:
        """Update all six theses from a batch of evidence packets."""
        priors = {normalize_thesis_key(k): v for k, v in dict(priors or {}).items()}
        states: dict[str, Any] = {}
        schema_states: list[dict[str, Any]] = []
        for key in sorted(THESIS_KEYS):
            state = self.update(key, priors.get(key), packets)
            states[key] = {
                "prior": state.prior,
                "posterior": state.posterior,
                "log_odds": state.log_odds,
                "packets_applied": state.packets_applied,
                "delta": state.posterior - state.prior,
            }
            schema_states.append(
                to_thesis_state_dict(
                    asset=asset,
                    thesis_key=key,
                    probability=state.posterior,
                    evidence_refs=state.packets_applied,
                    last_update_reason="bayesian_thesis_v0 update",
                )
            )

        ts = datetime.now(timezone.utc)
        rid = run_id or stable_hash([self.MODEL_NAME, str(len(packets))])
        audit = AuditRecord(
            model=self.MODEL_NAME,
            version=self.VERSION,
            run_id=rid,
            timestamp=ts,
            inputs_hash=stable_hash([p.packet_id for p in packets]),
            parameters={"n_packets": len(packets)},
            outputs={k: states[k]["posterior"] for k in states},
            notes="V0: independent thesis updates; no cross-thesis covariance.",
        )
        return ModelResult(
            model_name=self.MODEL_NAME,
            phase=ModelPhase.V0,
            payload={
                "theses": states,
                "thesis_keys": sorted(THESIS_KEYS),
                "thesis_states": schema_states,
            },
            audit=audit,
            data_gaps=list(self.PHASE3_REQUIREMENTS) if not packets else [],
        )


def run_bayesian_thesis(packets: Sequence[EvidencePacket] | None = None) -> ModelResult:
    return BayesianThesisModel().run(packets or [])
