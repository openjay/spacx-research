"""Risk API — ``POST /risk/evaluate``, ``POST /action/propose``.

Risk engine constrains all agents; compliance_level 2 blocks execution paths.
"""

from __future__ import annotations

from typing import Any


def risk_evaluate(
    asset: str = "SPCX",
    *,
    portfolio_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """POST /api/v1/spacx/risk/evaluate

    Compute :class:`RiskState` from metrics, thesis, blockers, and portfolio overlay.

    Args:
        asset: Primary symbol.
        portfolio_context: Optional holdings (NIO, NVDA, VOO, cash, crypto, ...).

    Returns:
        RiskState dict (overall_status, flags, limits, blocked_actions).
    """
    flags = [
        "FINAL_PROSPECTUS_PENDING",
        "LOCKUP_DAY0_UNKNOWN",
        "FIRST_EARNINGS_PENDING",
    ]
    return {
        "asset": asset,
        "overall_status": "AMBER",
        "evaluated_at": None,
        "flags": flags,
        "limits": {
            "max_position_pct": 1.0,
            "observation_cap_pct": 1.0,
        },
        "metric_alerts": [],
        "blocked_actions": ["AUTO_EXECUTE", "LIVE_ORDER"],
        "portfolio_context_received": portfolio_context is not None,
    }


def propose_action(
    asset: str = "SPCX",
    *,
    portfolio_context: dict[str, Any] | None = None,
    proposal_type: str = "OBSERVE_ONLY",
) -> dict[str, Any]:
    """POST /api/v1/spacx/action/propose

    Generate an :class:`ActionProposal` after risk evaluation (no execution).

    Args:
        asset: Ticker symbol.
        portfolio_context: Portfolio snapshot for risk budget model.
        proposal_type: Default observe-only until Phase 2 blockers clear.

    Returns:
        ActionProposal dict.
    """
    risk = risk_evaluate(asset, portfolio_context=portfolio_context)
    return {
        "proposal_id": None,
        "asset": asset,
        "proposal_type": proposal_type,
        "reason": "424B4 pending; first earnings not available; compliance_level 2",
        "max_position_pct": risk["limits"].get("observation_cap_pct", 1.0),
        "blocked_by": risk["flags"],
        "risk_state": risk["overall_status"],
        "evidence_refs": [],
        "requires_human_approval": True,
        "compliance_level": 2,
        "created_at": None,
    }


def generate_action_proposal(
    asset: str,
    portfolio_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Agent SDK alias for :func:`propose_action`."""
    return propose_action(asset, portfolio_context=portfolio_context)
