"""
Bayesian thesis updater: P(thesis | evidence packets).

Five thesis keys (Phase 1 / Track D synthesis):
  - connectivity_starlink
  - space_starship_execution
  - ai_capex_monetization
  - governance_control
  - supply_lockup_float
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence

from plugin.models._types import (
    AuditRecord,
    DataRequirement,
    ModelPhase,
    ModelResult,
    stable_hash,
)

# Canonical thesis keys referenced by thesis engine (V0)
THESIS_KEYS = frozenset(
    {
        "connectivity_starlink",
        "space_starship_execution",
        "ai_capex_monetization",
        "governance_control",
        "supply_lockup_float",
    }
)


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
        if self.thesis_key not in THESIS_KEYS:
            raise ValueError(f"unknown thesis_key: {self.thesis_key}")
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


class BayesianThesisModel:
    """Sequential log-odds update (V0); full MCMC deferred to Phase 3."""

    MODEL_NAME = "bayesian_thesis"
    VERSION = "0.1.0"

    DEFAULT_PRIORS: dict[str, float] = {
        "connectivity_starlink": 0.55,
        "space_starship_execution": 0.45,
        "ai_capex_monetization": 0.40,
        "governance_control": 0.35,
        "supply_lockup_float": 0.50,
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
        if thesis_key not in THESIS_KEYS:
            raise ValueError(f"unknown thesis_key: {thesis_key}")
        p0 = prior if prior is not None else self.DEFAULT_PRIORS[thesis_key]
        lo = self._prob_to_log_odds(p0)
        applied: list[str] = []
        for pkt in packets:
            if pkt.thesis_key != thesis_key:
                continue
            lr_eff = pkt.likelihood_ratio**pkt.confidence
            lo += math.log(lr_eff)
            applied.append(pkt.packet_id)
        post = self._log_odds_to_prob(lo)
        return ThesisState(
            thesis_key=thesis_key,
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
    ) -> ModelResult:
        """Update all five theses from a batch of evidence packets."""
        priors = dict(priors or {})
        states: dict[str, Any] = {}
        for key in sorted(THESIS_KEYS):
            state = self.update(key, priors.get(key), packets)
            states[key] = {
                "prior": state.prior,
                "posterior": state.posterior,
                "log_odds": state.log_odds,
                "packets_applied": state.packets_applied,
                "delta": state.posterior - state.prior,
            }

        ts = datetime.utcnow()
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
            payload={"theses": states, "thesis_keys": sorted(THESIS_KEYS)},
            audit=audit,
            data_gaps=list(self.PHASE3_REQUIREMENTS) if not packets else [],
        )


def run_bayesian_thesis(packets: Sequence[EvidencePacket] | None = None) -> ModelResult:
    return BayesianThesisModel().run(packets or [])
