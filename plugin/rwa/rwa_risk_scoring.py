"""
RWA risk scoring (V0) — multi-dimensional 0–100 scores with explainable flags.

Beyond TVL
----------
Total value locked (TVL) alone is a poor RWA risk signal: it ignores redemption
friction, legal claim enforceability, custody concentration, oracle integrity,
and transfer restrictions. This module scores **structural** RWA risks that can
deteriorate while TVL appears stable (e.g. gated redemptions, oracle drift,
secondary-market depth collapse). Downstream ``anomaly_detection`` and
``portfolio_risk_budget`` consume aggregate scores as tightening signals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from plugin.rwa.chain_state_monitor import ChainStateSnapshot, capture_chain_state

PRELAYER_VERSION = "0.1.0"

# Score dimensions (0 = worst risk, 100 = best / lowest structural risk)
RISK_DIMENSIONS = (
    "liquidity",
    "concentration",
    "redemption",
    "custody",
    "legal_rights",
    "oracle_risk",
    "secondary_depth",
    "transfer_restriction",
)


@dataclass(frozen=True)
class DimensionScore:
    dimension: str
    score: int  # 0–100
    weight: float = 1.0
    flags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.dimension not in RISK_DIMENSIONS:
            raise ValueError(f"unknown dimension: {self.dimension}")
        if not 0 <= self.score <= 100:
            raise ValueError("score must be in [0, 100]")


@dataclass
class RWARiskScore:
    """Schema-aligned RWA risk output for agents and risk engine."""

    asset_id: str
    composite_score: int
    dimensions: list[DimensionScore]
    explain_flags: list[str] = field(default_factory=list)
    scored_at: str = ""
    phase: str = "v0_stub"
    beyond_tvl_note: str = (
        "Composite score weights structural dimensions; high TVL does not imply high score."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "composite_score": self.composite_score,
            "dimensions": [
                {
                    "dimension": d.dimension,
                    "score": d.score,
                    "weight": d.weight,
                    "flags": list(d.flags),
                }
                for d in self.dimensions
            ],
            "explain_flags": list(self.explain_flags),
            "scored_at": self.scored_at,
            "phase": self.phase,
            "beyond_tvl_note": self.beyond_tvl_note,
        }


def _default_dimension_scores() -> list[DimensionScore]:
    """Neutral V0 placeholder: 50 on each axis with stub flags."""
    stub_flags = ("v0_no_live_data", "beyond_tvl_required")
    return [
        DimensionScore(dim, 50, 1.0, stub_flags) for dim in RISK_DIMENSIONS
    ]


def _weighted_composite(dimensions: Sequence[DimensionScore]) -> int:
    if not dimensions:
        return 0
    total_w = sum(d.weight for d in dimensions)
    if total_w <= 0:
        return 0
    raw = sum(d.score * d.weight for d in dimensions) / total_w
    return int(round(raw))


def score_from_chain_snapshot(
    asset_id: str,
    snapshot: ChainStateSnapshot | None = None,
    *,
    overrides: Mapping[str, int] | None = None,
) -> RWARiskScore:
    """
    Derive dimension scores from chain snapshot (V0: mostly defaults + gap flags).

    Phase 2+ maps oracle breaches → ``oracle_risk``, bridge anomalies → ``liquidity``, etc.
    """
    snap = snapshot or capture_chain_state()
    dims = _default_dimension_scores()
    flags: list[str] = ["beyond_tvl: do not use TVL as sole risk proxy"]

    if snap.data_gaps:
        flags.append(f"data_gaps:{len(snap.data_gaps)}")

    for reading in snap.oracle_deviations:
        if reading.breach:
            flags.append(f"oracle_breach:{reading.oracle_id}")

    if overrides:
        dim_map = {d.dimension: d for d in dims}
        updated: list[DimensionScore] = []
        for dim in RISK_DIMENSIONS:
            base = dim_map[dim]
            score = overrides.get(dim, base.score)
            updated.append(
                DimensionScore(dim, max(0, min(100, score)), base.weight, base.flags)
            )
        dims = updated

    explain = list(dict.fromkeys(flags + [f for d in dims for f in d.flags]))
    scored_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    composite = _weighted_composite(dims)

    return RWARiskScore(
        asset_id=asset_id,
        composite_score=composite,
        dimensions=dims,
        explain_flags=explain,
        scored_at=scored_at,
    )


def run_rwa_risk_scoring(
    asset_id: str = "RWA-AGG",
    snapshot: ChainStateSnapshot | None = None,
) -> RWARiskScore:
    """Convenience entry for OnchainRWAAgent scheduler."""
    return score_from_chain_snapshot(asset_id, snapshot)
