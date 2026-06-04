"""
Event study: abnormal return and volume around corporate / operational events.

Events: Form 424B4, earnings, lock-up releases, Starship milestones (Phase 1 seeds).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, Mapping, Sequence

from plugin.models._types import (
    AuditRecord,
    DataRequirement,
    ModelPhase,
    ModelResult,
    stable_hash,
)


EVENT_TYPES = frozenset(
    {
        "424B4",
        "earnings",
        "lock_up",
        "starship_milestone",
        "sec_amendment",
        "index_inclusion",
    }
)


@dataclass(frozen=True)
class EventWindow:
    """Estimation and event windows (trading days)."""

    event_date: date
    event_type: str
    estimation_start: date
    estimation_end: date
    event_start: date
    event_end: date
    est_days: int = 120
    pre_event_days: int = 5
    post_event_days: int = 20

    def __post_init__(self) -> None:
        if self.event_type not in EVENT_TYPES:
            raise ValueError(f"unknown event_type: {self.event_type}")


@dataclass(frozen=True)
class PriceObservation:
    trade_date: date
    close: float
    volume: float | None = None
    benchmark_close: float | None = None


@dataclass
class AbnormalReturnPoint:
    trade_date: date
    raw_return: float
    expected_return: float
    abnormal_return: float
    abnormal_volume_z: float | None


class EventStudyModel:
    """Market-model event study (V0: mean-adjusted returns when benchmark absent)."""

    MODEL_NAME = "event_study"
    VERSION = "0.1.0"

    PHASE3_REQUIREMENTS: tuple[DataRequirement, ...] = (
        DataRequirement(
            "spcx_daily_ohlcv",
            "market_data_provider",
            "daily",
            3,
            "SPCX adjusted close and volume from listing date.",
        ),
        DataRequirement(
            "peer_benchmark_basket",
            "market_data_provider",
            "daily",
            3,
            "Optional NVDA / mega-cap growth basket for beta-adjusted AR.",
        ),
        DataRequirement(
            "event_calendar",
            "metrics_registry",
            "event",
            3,
            "Dated 424B4, earnings, lock-up, Starship milestones.",
        ),
    )

    def build_window(
        self,
        event_date: date | str,
        event_type: str,
        *,
        est_days: int = 120,
        pre_event_days: int = 5,
        post_event_days: int = 20,
    ) -> EventWindow:
        ed = event_date if isinstance(event_date, date) else date.fromisoformat(str(event_date)[:10])
        est_end = ed - timedelta(days=1)
        est_start = est_end - timedelta(days=est_days * 2)  # calendar slack for trading days
        return EventWindow(
            event_date=ed,
            event_type=event_type,
            estimation_start=est_start,
            estimation_end=est_end,
            event_start=ed - timedelta(days=pre_event_days),
            event_end=ed + timedelta(days=post_event_days),
            est_days=est_days,
            pre_event_days=pre_event_days,
            post_event_days=post_event_days,
        )

    def _daily_returns(self, prices: Sequence[PriceObservation]) -> list[tuple[date, float]]:
        ordered = sorted(prices, key=lambda p: p.trade_date)
        out: list[tuple[date, float]] = []
        for i in range(1, len(ordered)):
            prev, cur = ordered[i - 1], ordered[i]
            if prev.close <= 0:
                continue
            out.append((cur.trade_date, (cur.close / prev.close) - 1.0))
        return out

    def _mean_expected_return(
        self, returns: Sequence[tuple[date, float]], est_start: date, est_end: date
    ) -> float:
        est = [r for d, r in returns if est_start <= d <= est_end]
        if not est:
            return 0.0
        return sum(est) / len(est)

    def _volume_z(
        self, volumes: Sequence[float], event_volume: float | None
    ) -> float | None:
        if event_volume is None or len(volumes) < 2:
            return None
        mean_v = sum(volumes) / len(volumes)
        var = sum((v - mean_v) ** 2 for v in volumes) / (len(volumes) - 1)
        if var <= 0:
            return None
        return (event_volume - mean_v) / (var**0.5)

    def run(
        self,
        window: EventWindow,
        prices: Sequence[PriceObservation],
        *,
        run_id: str | None = None,
    ) -> ModelResult:
        """
        Compute abnormal returns over the event window.

        V0: expected return = mean estimation-window return (market model stub).
        """
        returns = self._daily_returns(prices)
        mu = self._mean_expected_return(
            returns, window.estimation_start, window.estimation_end
        )

        ret_by_date = dict(returns)
        est_volumes = [
            p.volume
            for p in prices
            if p.volume is not None
            and window.estimation_start <= p.trade_date <= window.estimation_end
        ]
        est_volumes_f = [v for v in est_volumes if v is not None]

        points: list[AbnormalReturnPoint] = []
        car = 0.0
        for p in sorted(prices, key=lambda x: x.trade_date):
            if not (window.event_start <= p.trade_date <= window.event_end):
                continue
            raw = ret_by_date.get(p.trade_date)
            if raw is None:
                continue
            ar = raw - mu
            car += ar
            vol_z = self._volume_z(est_volumes_f, p.volume) if est_volumes_f else None
            points.append(
                AbnormalReturnPoint(
                    trade_date=p.trade_date,
                    raw_return=raw,
                    expected_return=mu,
                    abnormal_return=ar,
                    abnormal_volume_z=vol_z,
                )
            )

        ts = datetime.utcnow()
        rid = run_id or stable_hash([self.MODEL_NAME, window.event_type, str(window.event_date)])
        payload = {
            "event_type": window.event_type,
            "event_date": window.event_date.isoformat(),
            "expected_return_mu": mu,
            "cumulative_abnormal_return": car,
            "n_event_days": len(points),
            "abnormal_returns": [
                {
                    "trade_date": pt.trade_date.isoformat(),
                    "raw_return": pt.raw_return,
                    "expected_return": pt.expected_return,
                    "abnormal_return": pt.abnormal_return,
                    "abnormal_volume_z": pt.abnormal_volume_z,
                }
                for pt in points
            ],
        }
        gaps = list(self.PHASE3_REQUIREMENTS) if len(prices) < 3 else []

        audit = AuditRecord(
            model=self.MODEL_NAME,
            version=self.VERSION,
            run_id=rid,
            timestamp=ts,
            inputs_hash=stable_hash([str(len(prices)), window.event_type, str(window.event_date)]),
            parameters={
                "est_days": window.est_days,
                "pre_event_days": window.pre_event_days,
                "post_event_days": window.post_event_days,
            },
            outputs={"car": car, "n_event_days": len(points)},
        )
        return ModelResult(
            model_name=self.MODEL_NAME,
            phase=ModelPhase.V0,
            payload=payload,
            audit=audit,
            data_gaps=gaps,
        )


def run_event_study(
    event_date: date | str,
    event_type: str,
    prices: Sequence[PriceObservation] | None = None,
) -> ModelResult:
    """Convenience entrypoint with empty prices → documents Phase 3 gaps only."""
    model = EventStudyModel()
    window = model.build_window(event_date, event_type)
    return model.run(window, prices or [])
