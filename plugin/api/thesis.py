"""Thesis API — ``POST /thesis/update``, ``GET /thesis/{asset}``.

Probabilities updated by statistical engine + evidence; LLM explains, does not set P().
"""

from __future__ import annotations

from typing import Any


def thesis_update(
    updates: list[dict[str, Any]],
    *,
    evidence_packet_id: str | None = None,
) -> dict[str, Any]:
    """POST /api/v1/spacx/thesis/update

    Apply Bayesian or rule-based deltas to :class:`ThesisState` records.

    Args:
        updates: List of partial ThesisState dicts (thesis_key, probability, ...).
        evidence_packet_id: Required sealed packet when changing probability (V0: optional).

    Returns:
        dict with ``states`` (full ThesisState list) and ``audit_receipt_id``.
    """
    return {
        "states": updates,
        "evidence_packet_id": evidence_packet_id,
        "audit_receipt_id": None,
    }


def get_thesis_state(asset: str = "SPCX") -> dict[str, Any]:
    """GET /api/v1/spacx/thesis/{asset}

    Return all thesis probabilities for an asset.

    Args:
        asset: Ticker symbol.

    Returns:
        dict with ``asset`` and ``theses`` (list of ThesisState).
    """
    return {"asset": asset, "theses": []}
