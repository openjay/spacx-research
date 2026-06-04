"""Thesis API — ``POST /thesis/update``, ``GET /thesis/{asset}``.

Probabilities updated by statistical engine + evidence; LLM explains, does not set P().
"""

from __future__ import annotations

from typing import Any

from plugin.api._time import utc_now_iso
from plugin.contracts import validate_against_schema
from plugin.models.bayesian_thesis import BayesianThesisModel, to_thesis_state_dict
from plugin.models.thesis_keys import THESIS_KEYS, normalize_thesis_key


def _default_theses(asset: str = "SPCX") -> list[dict[str, Any]]:
    ts = utc_now_iso()
    return [
        to_thesis_state_dict(
            asset=asset,
            thesis_key=key,
            probability=BayesianThesisModel.DEFAULT_PRIORS[key],
            last_updated_at=ts,
            last_update_reason="V0 default prior",
        )
        for key in sorted(THESIS_KEYS)
    ]


def _coerce_thesis_update(row: dict[str, Any], asset: str) -> dict[str, Any]:
    key = normalize_thesis_key(row["thesis_key"])
    probability = float(row.get("probability", BayesianThesisModel.DEFAULT_PRIORS[key]))
    return to_thesis_state_dict(
        asset=asset,
        thesis_key=key,
        probability=probability,
        last_updated_at=row.get("last_updated_at") or utc_now_iso(),
        evidence_refs=row.get("evidence_refs"),
        last_update_reason=row.get("last_update_reason"),
    )


def thesis_update(
    updates: list[dict[str, Any]],
    *,
    asset: str = "SPCX",
    evidence_packet_id: str | None = None,
) -> dict[str, Any]:
    """POST /api/v1/spacx/thesis/update

    Apply Bayesian or rule-based deltas to :class:`ThesisState` records.

    Args:
        updates: List of partial ThesisState dicts (thesis_key, probability, ...).
        asset: Ticker symbol for emitted records.
        evidence_packet_id: Required sealed packet when changing probability (V0: optional).

    Returns:
        dict with ``states`` (full ThesisState list) and ``audit_receipt_id``.
    """
    states = [_coerce_thesis_update(row, asset) for row in updates]
    for state in states:
        validate_against_schema(state, "ThesisState")
    return {
        "states": states,
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
    theses = _default_theses(asset)
    for state in theses:
        validate_against_schema(state, "ThesisState")
    return {"asset": asset, "theses": theses}
