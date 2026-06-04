"""
Portfolio risk budget: position limits and thematic exposure caps.

SPCX observation sleeve default: 1% max position (user spec).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping, Sequence

from plugin.models._types import (
    AuditRecord,
    DataRequirement,
    ModelPhase,
    ModelResult,
    stable_hash,
)

THEMATIC_BUCKETS = frozenset(
    {
        "connectivity",
        "space",
        "ai_compute",
        "governance_hedge",
        "macro_hedge",
        "cash",
    }
)


@dataclass(frozen=True)
class RiskBudgetPolicy:
    max_position_pct: float = 0.01  # 1% observation default for SPCX
    max_thematic_pct: float = 0.40
    max_single_name_non_spcx: float = 0.05
    min_cash_pct: float = 0.10
    spcx_ticker: str = "SPCX"


@dataclass
class PositionLine:
    ticker: str
    weight_pct: float
    thematic: str

    def __post_init__(self) -> None:
        if self.thematic not in THEMATIC_BUCKETS:
            raise ValueError(f"unknown thematic: {self.thematic}")


@dataclass
class BudgetViolation:
    code: str
    severity: str
    message: str
    detail: dict[str, Any] = field(default_factory=dict)


class PortfolioRiskBudgetModel:
    MODEL_NAME = "portfolio_risk_budget"
    VERSION = "0.1.0"

    PHASE3_REQUIREMENTS: tuple[DataRequirement, ...] = (
        DataRequirement(
            "portfolio_holdings",
            "oms_or_research_book",
            "daily",
            3,
            "Live weights by ticker and sleeve.",
        ),
        DataRequirement(
            "nav_and_risk_limits",
            "risk_config",
            "daily",
            3,
            "Firm-wide limits overriding observation defaults.",
        ),
    )

    def check(
        self,
        positions: Sequence[PositionLine],
        policy: RiskBudgetPolicy | None = None,
    ) -> list[BudgetViolation]:
        pol = policy or RiskBudgetPolicy()
        violations: list[BudgetViolation] = []
        thematic: dict[str, float] = {t: 0.0 for t in THEMATIC_BUCKETS}

        for pos in positions:
            thematic[pos.thematic] = thematic.get(pos.thematic, 0.0) + pos.weight_pct
            if pos.ticker.upper() == pol.spcx_ticker and pos.weight_pct > pol.max_position_pct:
                violations.append(
                    BudgetViolation(
                        code="SPCX_POSITION_CAP",
                        severity="block",
                        message=f"SPCX weight {pos.weight_pct:.2%} exceeds cap {pol.max_position_pct:.2%}",
                        detail={"ticker": pos.ticker, "weight": pos.weight_pct},
                    )
                )
            if (
                pos.ticker.upper() != pol.spcx_ticker
                and pos.weight_pct > pol.max_single_name_non_spcx
            ):
                violations.append(
                    BudgetViolation(
                        code="SINGLE_NAME_CAP",
                        severity="warn",
                        message=f"{pos.ticker} weight exceeds non-SPCX cap",
                        detail={"ticker": pos.ticker, "weight": pos.weight_pct},
                    )
                )

        for bucket, w in thematic.items():
            if w > pol.max_thematic_pct:
                violations.append(
                    BudgetViolation(
                        code="THEMATIC_CAP",
                        severity="warn",
                        message=f"Thematic {bucket} at {w:.2%} exceeds {pol.max_thematic_pct:.2%}",
                        detail={"thematic": bucket, "weight": w},
                    )
                )

        cash_w = thematic.get("cash", 0.0)
        if cash_w < pol.min_cash_pct:
            violations.append(
                BudgetViolation(
                    code="MIN_CASH",
                    severity="warn",
                    message=f"Cash {cash_w:.2%} below minimum {pol.min_cash_pct:.2%}",
                    detail={"cash_weight": cash_w},
                )
            )
        return violations

    def run(
        self,
        positions: Sequence[PositionLine] | None = None,
        *,
        policy: RiskBudgetPolicy | None = None,
        run_id: str | None = None,
    ) -> ModelResult:
        pol = policy or RiskBudgetPolicy()
        pos = list(positions or [])
        violations = self.check(pos, pol)
        ok = len(violations) == 0

        ts = datetime.utcnow()
        rid = run_id or stable_hash([self.MODEL_NAME, str(ok)])
        audit = AuditRecord(
            model=self.MODEL_NAME,
            version=self.VERSION,
            run_id=rid,
            timestamp=ts,
            inputs_hash=stable_hash([p.ticker for p in pos]),
            parameters={
                "max_position_pct": pol.max_position_pct,
                "max_thematic_pct": pol.max_thematic_pct,
            },
            outputs={"ok": ok, "n_violations": len(violations)},
        )
        return ModelResult(
            model_name=self.MODEL_NAME,
            phase=ModelPhase.V0,
            payload={
                "ok": ok,
                "policy": {
                    "max_position_pct_spcx": pol.max_position_pct,
                    "max_thematic_pct": pol.max_thematic_pct,
                    "max_single_name_non_spcx": pol.max_single_name_non_spcx,
                    "min_cash_pct": pol.min_cash_pct,
                },
                "violations": [
                    {
                        "code": v.code,
                        "severity": v.severity,
                        "message": v.message,
                        "detail": v.detail,
                    }
                    for v in violations
                ],
                "thematic_buckets": sorted(THEMATIC_BUCKETS),
            },
            audit=audit,
            data_gaps=list(self.PHASE3_REQUIREMENTS) if not pos else [],
        )


def run_portfolio_risk_budget(
    positions: Sequence[PositionLine] | None = None,
    policy: RiskBudgetPolicy | None = None,
) -> ModelResult:
    return PortfolioRiskBudgetModel().run(positions, policy=policy)
