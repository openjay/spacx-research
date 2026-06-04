"""Metrics API — ``POST /metrics/update``, ``GET /metrics/{asset}/{metric_id}``.

LLM must not override hard metrics; formulas live in ``plugin/metrics/registry.yaml``.
"""

from __future__ import annotations

from typing import Any


def metrics_update(
    snapshots: list[dict[str, Any]],
    *,
    recompute_status: bool = True,
) -> dict[str, Any]:
    """POST /api/v1/spacx/metrics/update

    Upsert one or more :class:`MetricSnapshot` rows and optionally run threshold engine.

    Args:
        snapshots: List of MetricSnapshot-compatible dicts.
        recompute_status: When True, set GREEN/AMBER/RED from registry thresholds.

    Returns:
        dict with ``updated`` count, ``snapshots`` (with status), and ``alerts_raised``.
    """
    out = []
    for s in snapshots:
        row = dict(s)
        if recompute_status and "status" not in row:
            row["status"] = "UNKNOWN"
        out.append(row)
    return {"updated": len(out), "snapshots": out, "alerts_raised": []}


def get_metric(asset: str, metric_id: str) -> dict[str, Any]:
    """GET /api/v1/spacx/metrics/{asset}/{metric_id}

    Agent helper — fetch latest :class:`MetricSnapshot` for a watch metric.

    Args:
        asset: e.g. ``SPCX``.
        metric_id: e.g. ``AI_CAPEX_REVENUE``, ``STARLINK_SUBSCRIBERS``.

    Returns:
        MetricSnapshot dict or empty stub with ``status``: ``UNKNOWN``.
    """
    return {
        "metric_id": metric_id,
        "asset": asset,
        "value": None,
        "unit": None,
        "as_of": None,
        "status": "UNKNOWN",
        "evidence_refs": [],
    }
