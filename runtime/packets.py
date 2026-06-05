"""Agent adapter packets — ThesisUpdate, RiskAlert, NAP (Next Action Packet)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from plugin.valuation.export_snapshots import valuation_snapshot_refs

PacketKind = Literal["thesis_update", "risk_alert", "next_action"]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ThesisUpdatePacket:
    """Structured thesis delta for OpenClaw / Longter adapters."""

    asset: str = "SPCX"
    thesis_key: str = ""
    thesis: str = ""
    probability: float = 0.5
    status: str = "WATCH"
    last_update_reason: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    metric_snapshot_refs: list[str] = field(default_factory=valuation_snapshot_refs)
    packet_id: str = field(default_factory=lambda: str(uuid4()))
    emitted_at: str = field(default_factory=_utc_now)
    compliance_level: int = 2
    requires_human_gate: str | None = "thesis_publish"

    def to_dict(self) -> dict[str, Any]:
        body = asdict(self)
        body["packet_kind"] = "thesis_update"
        return body


@dataclass
class RiskAlertPacket:
    """Risk state change or blocker escalation for agents."""

    asset: str = "SPCX"
    overall_status: str = "AMBER"
    flags: list[str] = field(default_factory=list)
    metric_alerts: list[dict[str, Any]] = field(default_factory=list)
    blocked_actions: list[str] = field(default_factory=lambda: ["AUTO_EXECUTE", "LIVE_ORDER"])
    reason: str = ""
    packet_id: str = field(default_factory=lambda: str(uuid4()))
    emitted_at: str = field(default_factory=_utc_now)
    compliance_level: int = 2

    def to_dict(self) -> dict[str, Any]:
        body = asdict(self)
        body["packet_kind"] = "risk_alert"
        return body


@dataclass
class NextActionPacket:
    """NAP — proposed next step for human or agent (observe-only at V0)."""

    asset: str = "SPCX"
    action_type: str = "OBSERVE_ONLY"
    priority: Literal["P0", "P1", "P2"] = "P1"
    summary: str = ""
    rationale: str = ""
    blocked_by: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metric_snapshot_refs: list[str] = field(default_factory=valuation_snapshot_refs)
    target_agent: str | None = None
    requires_human_approval: bool = True
    packet_id: str = field(default_factory=lambda: str(uuid4()))
    emitted_at: str = field(default_factory=_utc_now)
    compliance_level: int = 2

    def to_dict(self) -> dict[str, Any]:
        body = asdict(self)
        body["packet_kind"] = "next_action"
        return body


def nap_from_blockers(blockers: dict[str, bool], *, reason: str = "") -> NextActionPacket:
    """Build a default NAP when Phase 2 blockers are active."""
    active = [k for k, v in blockers.items() if v]
    priority: Literal["P0", "P1", "P2"] = "P0" if "FINAL_PROSPECTUS_PENDING" in active else "P1"
    return NextActionPacket(
        action_type="OBSERVE_ONLY",
        priority=priority,
        summary="Maintain read-only watch; no execution paths",
        rationale=reason or "Phase 2 blockers active; compliance level 2",
        blocked_by=active,
        metric_snapshot_refs=valuation_snapshot_refs(),
        target_agent="SECFilingAgent" if "FINAL_PROSPECTUS_PENDING" in active else "EvidenceAuditorAgent",
    )
