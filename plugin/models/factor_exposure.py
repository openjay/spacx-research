"""
Factor exposure: placeholder betas for SPCX vs peer set (NVDA, etc.).

V0: OLS stub on aligned return series; full Barra-style factors in Phase 3.
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

DEFAULT_FACTORS = (
    "MKT",
    "SMB",
    "HML",
    "MTUM",
    "AI_GROWTH",  # NVDA + hyperscaler proxy
    "RATES",
    "SPACE_INDUSTRIAL",
)

DEFAULT_PEERS = ("NVDA", "RKLB", "ASTS", "GOOGL", "AMZN")


@dataclass(frozen=True)
class ReturnSeries:
    ticker: str
    dates: tuple[str, ...]
    returns: tuple[float, ...]


@dataclass
class FactorBeta:
    factor: str
    beta: float
    t_stat: float | None = None


class FactorExposureModel:
    MODEL_NAME = "factor_exposure"
    VERSION = "0.1.0"

    PHASE3_REQUIREMENTS: tuple[DataRequirement, ...] = (
        DataRequirement(
            "spcx_daily_returns",
            "market_data_provider",
            "daily",
            3,
            "Adjusted total returns for SPCX post-listing.",
        ),
        DataRequirement(
            "factor_return_series",
            "vendor_or_internal",
            "daily",
            3,
            "Fama-French + custom AI_GROWTH basket.",
        ),
        DataRequirement(
            "peer_returns",
            "market_data_provider",
            "daily",
            3,
            f"Peer tickers: {', '.join(DEFAULT_PEERS)}.",
        ),
    )

    def _ols_beta(self, y: Sequence[float], x: Sequence[float]) -> float:
        n = min(len(y), len(x))
        if n < 5:
            return 0.0
        yv = list(y[:n])
        xv = list(x[:n])
        mx = sum(xv) / n
        my = sum(yv) / n
        cov = sum((xv[i] - mx) * (yv[i] - my) for i in range(n))
        var = sum((xv[i] - mx) ** 2 for i in range(n))
        if var <= 1e-12:
            return 0.0
        return cov / var

    def estimate(
        self,
        target: ReturnSeries,
        factors: dict[str, ReturnSeries],
    ) -> list[FactorBeta]:
        betas: list[FactorBeta] = []
        for name, fac in factors.items():
            b = self._ols_beta(target.returns, fac.returns)
            betas.append(FactorBeta(factor=name, beta=b))
        return betas

    def run(
        self,
        target: ReturnSeries | None = None,
        factors: dict[str, ReturnSeries] | None = None,
        *,
        run_id: str | None = None,
    ) -> ModelResult:
        """Return placeholder betas when data absent."""
        ts = datetime.now(timezone.utc)
        if target is None or factors is None or len(target.returns) < 5:
            placeholder = {f: 0.0 for f in DEFAULT_FACTORS}
            placeholder["AI_GROWTH"] = 0.85  # documented prior for SPCX–AI linkage
            placeholder["MKT"] = 1.10
            payload: dict[str, Any] = {
                "ticker": "SPCX",
                "betas": placeholder,
                "peers": list(DEFAULT_PEERS),
                "mode": "prior_stub",
                "r_squared": None,
            }
            gaps = list(self.PHASE3_REQUIREMENTS)
        else:
            betas = self.estimate(target, factors)
            payload = {
                "ticker": target.ticker,
                "betas": {b.factor: b.beta for b in betas},
                "peers": list(DEFAULT_PEERS),
                "mode": "ols_v0",
                "r_squared": None,
            }
            gaps = []

        rid = run_id or stable_hash([self.MODEL_NAME, payload.get("mode", "")])
        audit = AuditRecord(
            model=self.MODEL_NAME,
            version=self.VERSION,
            run_id=rid,
            timestamp=ts,
            inputs_hash=stable_hash([payload.get("ticker", "SPCX")]),
            parameters={"factors": list(DEFAULT_FACTORS)},
            outputs={"betas": payload["betas"]},
            notes="V0 stub; replace with rolling OLS + Newey-West in Phase 3.",
        )
        return ModelResult(
            model_name=self.MODEL_NAME,
            phase=ModelPhase.V0,
            payload=payload,
            audit=audit,
            data_gaps=gaps,
        )


def run_factor_exposure(
    target: ReturnSeries | None = None,
    factors: dict[str, ReturnSeries] | None = None,
) -> ModelResult:
    return FactorExposureModel().run(target, factors)
