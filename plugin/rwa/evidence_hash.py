"""
Evidence hashing — SHA-256 seals for packets, metrics, thesis, and risk proposals.

Integrates with ``EvidencePacket.json`` and ``AuditReceipt.json`` fields:
``hash``, ``sealed_at``, ``onchain_tx`` / ``onchain_anchor``. No wallet keys;
chain anchor is a documented placeholder until Phase W4+.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

PRELAYER_VERSION = "0.1.0"
CHAIN_ANCHOR_PLACEHOLDER = "pending_phase_w4"


@dataclass(frozen=True)
class SealedDigest:
    """Single sealed artifact with optional on-chain anchor placeholder."""

    artifact_type: str
    artifact_id: str
    content_hash: str
    sealed_at: str
    canonical_bytes_len: int
    onchain_anchor: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "artifact_id": self.artifact_id,
            "content_hash": self.content_hash,
            "sealed_at": self.sealed_at,
            "canonical_bytes_len": self.canonical_bytes_len,
            "onchain_anchor": self.onchain_anchor,
        }


def _canonical_json(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(payload: Mapping[str, Any]) -> tuple[str, int]:
    raw = _canonical_json(payload)
    digest = hashlib.sha256(raw).hexdigest()
    return digest, len(raw)


def _seal(
    artifact_type: str,
    artifact_id: str,
    body: Mapping[str, Any],
    *,
    anchor: bool = False,
) -> SealedDigest:
    content_hash, nbytes = sha256_hex(body)
    sealed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return SealedDigest(
        artifact_type=artifact_type,
        artifact_id=artifact_id,
        content_hash=content_hash,
        sealed_at=sealed_at,
        canonical_bytes_len=nbytes,
        onchain_anchor=CHAIN_ANCHOR_PLACEHOLDER if anchor else None,
    )


def seal_evidence_packet(
    packet: Mapping[str, Any],
    *,
    packet_id: str | None = None,
    anchor: bool = False,
) -> SealedDigest:
    """
    Seal an ``EvidencePacket``-shaped dict (pre- or post-claims).

    Caller may merge ``hash`` and ``sealed_at`` back into the packet before persistence.
    """
    pid = packet_id or str(packet.get("packet_id", "unknown"))
    return _seal("evidence_packet", pid, packet, anchor=anchor)


def seal_metric_snapshot(
    snapshot: Mapping[str, Any],
    *,
    metric_id: str | None = None,
) -> SealedDigest:
    """Seal a ``MetricSnapshot``-shaped dict."""
    mid = metric_id or str(snapshot.get("metric_id", "unknown"))
    return _seal("metric_snapshot", mid, snapshot)


def seal_thesis_state(
    thesis: Mapping[str, Any],
    *,
    asset: str = "SPCX",
) -> SealedDigest:
    """Seal thesis engine snapshot (posteriors + keys)."""
    return _seal("thesis_state", asset, thesis)


def seal_risk_proposal(
    proposal: Mapping[str, Any],
    *,
    proposal_id: str | None = None,
) -> SealedDigest:
    """Seal risk evaluation or ``ActionProposal`` body."""
    pid = proposal_id or str(proposal.get("proposal_id", "risk-proposal"))
    return _seal("risk_proposal", pid, proposal)


def audit_receipt_hashes(
    input_body: Mapping[str, Any],
    output_body: Mapping[str, Any],
) -> dict[str, str]:
    """
    Produce ``input_hash`` / ``output_hash`` for ``AuditReceipt`` linkage.

    Matches ingest and evidence API expectations without persisting receipts in V0.
    """
    in_hash, _ = sha256_hex(input_body)
    out_hash, _ = sha256_hex(output_body)
    return {"input_hash": in_hash, "output_hash": out_hash}


def apply_seal_to_evidence_packet(
    packet: dict[str, Any],
    *,
    anchor: bool = False,
) -> dict[str, Any]:
    """Return packet copy with ``hash``, ``sealed_at``, optional ``onchain_tx`` set."""
    sealed = seal_evidence_packet(packet, anchor=anchor)
    out = dict(packet)
    out["hash"] = sealed.content_hash
    out["sealed_at"] = sealed.sealed_at
    if anchor:
        out["onchain_tx"] = sealed.onchain_anchor
    return out
