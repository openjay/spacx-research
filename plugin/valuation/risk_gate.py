"""Valuation-driven action gates — OBSERVE_ONLY when price exceeds DCF anchor band."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_VALUATION_DIR = Path(__file__).resolve().parent
_ANCHORS_PATH = _VALUATION_DIR / "price_anchors.yaml"

_PHASE1_BLOCKERS = frozenset(
    {"FINAL_PROSPECTUS_PENDING", "FIRST_EARNINGS_PENDING", "LOCKUP_DAY0_UNKNOWN"}
)


def load_dcf_anchor_price(anchors_path: Path | None = None) -> float:
    path = anchors_path or _ANCHORS_PATH
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return float(
        data.get("anchors", {})
        .get("dcf_conservative_anchor", {})
        .get("price_usd_per_share", 60.0)
    )


def should_observe_only(
    price_usd: float | None,
    *,
    active_blockers: set[str] | frozenset[str] | None = None,
    dcf_multiple_threshold: float = 2.0,
) -> dict[str, Any]:
    """Return True when price > threshold × DCF conservative anchor without 424B4 + earnings.

    Default: OBSERVE_ONLY if price > 2× ~$60/sh ($120) while FINAL_PROSPECTUS_PENDING
    or FIRST_EARNINGS_PENDING remain active.
    """
    blockers = active_blockers if active_blockers is not None else _PHASE1_BLOCKERS
    anchor = load_dcf_anchor_price()
    threshold_price = anchor * dcf_multiple_threshold
    gate_blockers = blockers & _PHASE1_BLOCKERS

    triggered = False
    reason_parts: list[str] = []

    if price_usd is not None and price_usd > threshold_price:
        if gate_blockers:
            triggered = True
            reason_parts.append(
                f"price ${price_usd:.2f} > {dcf_multiple_threshold:.0f}x "
                f"DCF conservative anchor (${anchor:.2f} → ${threshold_price:.2f})"
            )
            if "FINAL_PROSPECTUS_PENDING" in gate_blockers:
                reason_parts.append("424B4 not filed")
            if "FIRST_EARNINGS_PENDING" in gate_blockers:
                reason_parts.append("first earnings not available")

    return {
        "observe_only": triggered,
        "proposal_type": "OBSERVE_ONLY" if triggered else None,
        "price_usd": price_usd,
        "dcf_anchor_price_usd": anchor,
        "threshold_price_usd": threshold_price,
        "dcf_multiple_threshold": dcf_multiple_threshold,
        "active_gate_blockers": sorted(gate_blockers),
        "reason": "; ".join(reason_parts) if reason_parts else None,
        "valuation_tier": "C",
    }
