"""
Policy wallet (V0) — ``ExecutionPolicy`` whitelist; on-chain actions blocked.

Compliance level 2: research and proposals only. Live execution wallet is
Phase W4 gated (see ``docs/COMPLIANCE.md``, ``docs/ARCHITECTURE.md``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, Sequence

PRELAYER_VERSION = "0.1.0"
V0_BLOCK_REASON = "compliance_level_2_execution_wallet_phase_w4"


class OnchainActionStatus(str, Enum):
    BLOCKED = "BLOCKED"
    PENDING_APPROVAL = "PENDING_APPROVAL"  # reserved W4+
    ALLOWED = "ALLOWED"  # reserved W5+


@dataclass
class ExecutionPolicy:
    """
    Whitelist and risk guards for future policy-bound execution (not active in V0).

    All checks are evaluated in ``propose_onchain_action`` but V0 always returns BLOCKED.
    """

    policy_id: str
    allowed_assets: list[str] = field(default_factory=list)
    allowed_chains: list[str] = field(default_factory=list)
    max_position_usd: float | None = None
    max_slippage_bps: float = 50.0
    max_daily_loss_usd: float | None = None
    oracle_guard_bps: float = 100.0
    kill_switch: bool = False
    compliance_level: int = 2
    notes: str = "V0 — monitor_only; no signing material"

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "allowed_assets": list(self.allowed_assets),
            "allowed_chains": list(self.allowed_chains),
            "max_position_usd": self.max_position_usd,
            "max_slippage_bps": self.max_slippage_bps,
            "max_daily_loss_usd": self.max_daily_loss_usd,
            "oracle_guard_bps": self.oracle_guard_bps,
            "kill_switch": self.kill_switch,
            "compliance_level": self.compliance_level,
            "notes": self.notes,
        }

    def validate_action_preflight(
        self,
        action: Mapping[str, Any],
    ) -> list[str]:
        """Return violation codes (for logging); does not authorize execution in V0."""
        violations: list[str] = []
        asset = str(action.get("asset", ""))
        chain = str(action.get("chain_id", ""))

        if self.kill_switch:
            violations.append("kill_switch_active")

        if self.allowed_assets and asset and asset not in self.allowed_assets:
            violations.append(f"asset_not_whitelisted:{asset}")

        if self.allowed_chains and chain and chain not in self.allowed_chains:
            violations.append(f"chain_not_whitelisted:{chain}")

        notional = action.get("notional_usd")
        if (
            self.max_position_usd is not None
            and notional is not None
            and float(notional) > self.max_position_usd
        ):
            violations.append("max_position_exceeded")

        slippage = action.get("slippage_bps")
        if slippage is not None and float(slippage) > self.max_slippage_bps:
            violations.append("slippage_exceeded")

        return violations


def default_monitor_only_policy() -> ExecutionPolicy:
    """Empty whitelist — consistent with rwa_prelayer_v0 monitor_only capability."""
    return ExecutionPolicy(
        policy_id="rwa-monitor-only-v0",
        allowed_assets=[],
        allowed_chains=[],
        max_position_usd=0.0,
        kill_switch=True,
        compliance_level=2,
    )


def propose_onchain_action(
    action: Mapping[str, Any],
    policy: ExecutionPolicy | None = None,
    *,
    actor: str = "OnchainRWAAgent",
) -> dict[str, Any]:
    """
    Propose an on-chain action for audit trail only.

    V0 always returns ``status: BLOCKED`` regardless of preflight (no wallet, level 2).
    """
    pol = policy or default_monitor_only_policy()
    violations = pol.validate_action_preflight(action)
    recorded_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    return {
        "status": OnchainActionStatus.BLOCKED.value,
        "reason": V0_BLOCK_REASON,
        "policy_id": pol.policy_id,
        "actor": actor,
        "action": dict(action),
        "preflight_violations": violations,
        "compliance_level": pol.compliance_level,
        "recorded_at": recorded_at,
        "execution_wallet": None,
        "phase": "w4_gated",
    }
