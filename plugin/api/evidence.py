"""Evidence API — ``POST /evidence/seal``, ``POST /report/generate``.

Evidence grading: A (SEC/regulator/exchange) > B (IR) > C (tier-1 news) > D (social).
"""

from __future__ import annotations

from typing import Any


def seal_evidence(packet_id: str, packet: dict[str, Any] | None = None) -> dict[str, Any]:
    """POST /api/v1/spacx/evidence/seal

    Compute canonical hash and seal an :class:`EvidencePacket` (optional on-chain anchor).

    Args:
        packet_id: Existing packet id or id to assign when ``packet`` is provided.
        packet: Full EvidencePacket body; if omitted, loads by ``packet_id`` (stub: no-op load).

    Returns:
        dict with ``packet_id``, ``hash``, ``sealed_at``, optional ``onchain_tx``.
    """
    body = packet or {}
    return {
        "packet_id": packet_id or body.get("packet_id"),
        "hash": body.get("hash"),
        "sealed_at": body.get("sealed_at"),
        "onchain_tx": None,
        "status": "sealed_stub",
    }


def generate_report(
    asset: str = "SPCX",
    *,
    report_type: str = "daily_thesis",
    as_of: str | None = None,
) -> dict[str, Any]:
    """POST /api/v1/spacx/report/generate

    Build a human/agent-readable report from current metrics, thesis, and risk state.

    Args:
        asset: Ticker symbol (default SPCX).
        report_type: ``daily_thesis`` | ``event_brief`` | ``risk_alert_digest``.
        as_of: ISO-8601 timestamp for report snapshot.

    Returns:
        dict with ``report_id``, ``markdown``, ``evidence_refs``, ``generated_at``.
    """
    return {
        "asset": asset,
        "report_type": report_type,
        "report_id": None,
        "markdown": "",
        "evidence_refs": [],
        "generated_at": as_of,
    }
