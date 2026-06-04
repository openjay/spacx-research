"""RWA prelayer stubs — policy wallet blocked, evidence hashing."""

from __future__ import annotations

import re

from plugin.rwa.evidence_hash import seal_evidence_packet, sha256_hex
from plugin.rwa.policy_wallet import OnchainActionStatus, propose_onchain_action

_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


def test_propose_onchain_action_is_blocked() -> None:
    out = propose_onchain_action({"asset": "SPCX", "chain_id": "ethereum", "notional_usd": 100})
    assert out["status"] == OnchainActionStatus.BLOCKED.value
    assert out["execution_wallet"] is None


def test_evidence_hash_produces_sha256_hex() -> None:
    packet = {"packet_id": "pkt-test", "claims": [{"text": "demo"}]}
    digest, nbytes = sha256_hex(packet)
    assert _SHA256_RE.match(digest)
    assert nbytes > 0

    sealed = seal_evidence_packet(packet, packet_id="pkt-test")
    assert sealed.content_hash == digest
    assert _SHA256_RE.match(sealed.content_hash)
