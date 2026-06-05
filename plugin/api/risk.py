"""Risk API — ``POST /risk/evaluate``, ``POST /action/propose``.

Risk engine constrains all agents; compliance_level 2 blocks execution paths.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any

from plugin.api._time import utc_now_iso
from plugin.contracts import validate_against_schema
from plugin.valuation.risk_gate import should_observe_only

_PHASE1_BLOCKERS = (
    "FINAL_PROSPECTUS_PENDING",
    "LOCKUP_DAY0_UNKNOWN",
    "FIRST_EARNINGS_PENDING",
)


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
    _ = portfolio_context  # Phase 3: portfolio overlay on limits
    result: dict[str, Any] = {
        "asset": asset,
        "overall_status": "AMBER",
        "evaluated_at": utc_now_iso(),
        "flags": list(_PHASE1_BLOCKERS),
        "limits": {
            "max_position_pct": 1.0,
            "observation_cap_pct": 1.0,
        },
        "metric_alerts": [],
        "blocked_actions": ["AUTO_EXECUTE", "LIVE_ORDER"],
    }
    validate_against_schema(result, "RiskState")
    return result


def propose_action(
    asset: str = "SPCX",
    *,
    portfolio_context: dict[str, Any] | None = None,
    proposal_type: str = "OBSERVE_ONLY",
    market_price_usd: float | None = None,
) -> dict[str, Any]:
    """POST /api/v1/spacx/action/propose

    Generate an :class:`ActionProposal` after risk evaluation (no execution).

    Args:
        asset: Ticker symbol.
        portfolio_context: Portfolio snapshot for risk budget model.
        proposal_type: Default observe-only until Phase 2 blockers clear.
        market_price_usd: Optional observed price for valuation gate (2× DCF anchor).

    Returns:
        ActionProposal dict.
    """
    risk = risk_evaluate(asset, portfolio_context=portfolio_context)
    created_at = utc_now_iso()
    ctx_hash = None
    if portfolio_context is not None:
        payload = json.dumps(portfolio_context, sort_keys=True, default=str)
        ctx_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]

    price = market_price_usd
    if price is None and portfolio_context is not None:
        raw = portfolio_context.get("spcx_price_usd") or portfolio_context.get(
            "market_price_usd"
        )
        if raw is not None:
            price = float(raw)

    valuation_gate = should_observe_only(price, active_blockers=set(risk["flags"]))
    effective_type = proposal_type
    reason = "424B4 pending; first earnings not available; compliance_level 2"
    if valuation_gate["observe_only"]:
        effective_type = "OBSERVE_ONLY"
        gate_reason = valuation_gate.get("reason") or "valuation gate"
        reason = f"{reason}; {gate_reason}"

    result: dict[str, Any] = {
        "proposal_id": str(uuid.uuid4()),
        "asset": asset,
        "proposal_type": effective_type,
        "reason": reason,
        "max_position_pct": risk["limits"].get("observation_cap_pct", 1.0),
        "blocked_by": list(risk["flags"]),
        "risk_state": risk["overall_status"],
        "evidence_refs": [],
        "requires_human_approval": True,
        "compliance_level": 2,
        "created_at": created_at,
    }
    if ctx_hash:
        result["portfolio_context_hash"] = ctx_hash

    validate_against_schema(result, "ActionProposal")
    return result


def generate_action_proposal(
    asset: str,
    portfolio_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Agent SDK alias for :func:`propose_action`."""
    return propose_action(asset, portfolio_context=portfolio_context)
