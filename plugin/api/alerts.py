"""Alerts API — ``POST /alert/dispatch``.

Dispatches AMBER/RED alerts to agents and human supervisors; no trading side effects.
"""

from __future__ import annotations

from typing import Any


def alert_dispatch(
    alerts: list[dict[str, Any]],
    *,
    channel: str = "agent_bus",
) -> dict[str, Any]:
    """POST /api/v1/spacx/alert/dispatch

    Publish metric, thesis, or risk alerts.

    Args:
        alerts: Each item should include ``severity`` (AMBER|RED), ``code``, ``message``,
            ``asset``, and optional ``metric_id`` / ``thesis_key``.
        channel: Delivery surface (``agent_bus``, ``webhook``, ``log``).

    Returns:
        dict with ``dispatched`` count and ``alert_ids``.
    """
    return {
        "dispatched": len(alerts),
        "alert_ids": [],
        "channel": channel,
    }


def get_risk_alerts(asset: str = "SPCX") -> list[dict[str, Any]]:
    """Agent helper — list open risk/metric alerts for an asset.

    Args:
        asset: Ticker symbol.

    Returns:
        List of alert dicts (empty stub in V0).
    """
    return []
