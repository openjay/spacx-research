"""
Chain state monitors (V0 stubs) — stablecoin, treasury RWA, transfers, bridges, oracles.

No live RPC or wallet keys. Outputs align with ``ChainStateSnapshot.json``.
Compliance level 2; execution wallet gated at Phase W4.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Sequence

PRELAYER_VERSION = "0.1.0"
MONITOR_PHASE = "v0_stub"


@dataclass(frozen=True)
class StablecoinSupplyReading:
    """Circulating supply observation for a stablecoin issuer or on-chain aggregate."""

    asset_symbol: str
    chain_id: str
    supply_usd: float | None
    as_of: str
    source: str = "stub"
    deviation_pct: float | None = None
    notes: str = ""


@dataclass(frozen=True)
class TokenizedTreasuryAUM:
    """Tokenized T-bill / money-market fund AUM proxy."""

    instrument_id: str
    aum_usd: float | None
    holder_count: int | None
    as_of: str
    custodian: str | None = None
    notes: str = ""


@dataclass(frozen=True)
class RWATransferEvent:
    """Large or policy-relevant RWA token transfer (research signal only)."""

    tx_ref: str
    asset_id: str
    from_label: str
    to_label: str
    amount_usd: float | None
    as_of: str
    flagged: bool = False
    reason: str = ""


@dataclass(frozen=True)
class BridgeFlowReading:
    """Cross-chain bridge inflow/outflow aggregate."""

    bridge_id: str
    chain_in: str
    chain_out: str
    volume_24h_usd: float | None
    net_flow_24h_usd: float | None
    as_of: str
    anomaly: bool = False


@dataclass(frozen=True)
class OracleDeviationReading:
    """Oracle vs reference price deviation."""

    oracle_id: str
    feed_asset: str
    deviation_bps: float | None
    reference_source: str
    as_of: str
    breach: bool = False
    threshold_bps: float = 50.0


@dataclass
class ChainStateSnapshot:
    """Aggregate monitor output for OnchainRWAAgent and risk pre-layer."""

    snapshot_id: str
    captured_at: str
    stablecoins: list[StablecoinSupplyReading] = field(default_factory=list)
    treasury_aum: list[TokenizedTreasuryAUM] = field(default_factory=list)
    rwa_transfers: list[RWATransferEvent] = field(default_factory=list)
    bridge_flows: list[BridgeFlowReading] = field(default_factory=list)
    oracle_deviations: list[OracleDeviationReading] = field(default_factory=list)
    phase: str = MONITOR_PHASE
    data_gaps: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "captured_at": self.captured_at,
            "stablecoins": [vars(s) for s in self.stablecoins],
            "treasury_aum": [vars(t) for t in self.treasury_aum],
            "rwa_transfers": [vars(r) for r in self.rwa_transfers],
            "bridge_flows": [vars(b) for b in self.bridge_flows],
            "oracle_deviations": [vars(o) for o in self.oracle_deviations],
            "phase": self.phase,
            "data_gaps": list(self.data_gaps),
        }


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def monitor_stablecoin_supply(
    assets: Sequence[str] | None = None,
) -> list[StablecoinSupplyReading]:
    """Stub: returns placeholder rows; Phase 2 attaches chain/index feeds."""
    symbols = list(assets or ("USDC", "USDT"))
    as_of = _utc_now()
    return [
        StablecoinSupplyReading(
            asset_symbol=sym,
            chain_id="multi",
            supply_usd=None,
            as_of=as_of,
            notes="V0 stub — no RPC",
        )
        for sym in symbols
    ]


def monitor_tokenized_treasury_aum() -> list[TokenizedTreasuryAUM]:
    """Stub: tokenized treasury basket AUM monitors."""
    as_of = _utc_now()
    return [
        TokenizedTreasuryAUM(
            instrument_id="TBILL-RWA-AGG",
            aum_usd=None,
            holder_count=None,
            as_of=as_of,
            notes="V0 stub",
        )
    ]


def monitor_rwa_transfers() -> list[RWATransferEvent]:
    """Stub: no mempool/indexer in V0."""
    return []


def monitor_bridge_flows() -> list[BridgeFlowReading]:
    """Stub: bridge volume monitors."""
    as_of = _utc_now()
    return [
        BridgeFlowReading(
            bridge_id="generic-bridge",
            chain_in="ethereum",
            chain_out="unknown",
            volume_24h_usd=None,
            net_flow_24h_usd=None,
            as_of=as_of,
        )
    ]


def monitor_oracle_deviation(
    feeds: Sequence[str] | None = None,
) -> list[OracleDeviationReading]:
    """Stub: oracle deviation vs reference."""
    as_of = _utc_now()
    ids = list(feeds or ("chainlink-usdc-usd",))
    return [
        OracleDeviationReading(
            oracle_id=oid,
            feed_asset="USDC",
            deviation_bps=None,
            reference_source="stub",
            as_of=as_of,
        )
        for oid in ids
    ]


def capture_chain_state(snapshot_id: str | None = None) -> ChainStateSnapshot:
    """Run all stub monitors and return a ``ChainStateSnapshot``."""
    sid = snapshot_id or f"chain-{int(datetime.now(timezone.utc).timestamp())}"
    gaps = [
        "live_chain_rpc",
        "bridge_indexer",
        "rwa_transfer_indexer",
        "oracle_reference_feed",
    ]
    return ChainStateSnapshot(
        snapshot_id=sid,
        captured_at=_utc_now(),
        stablecoins=monitor_stablecoin_supply(),
        treasury_aum=monitor_tokenized_treasury_aum(),
        rwa_transfers=monitor_rwa_transfers(),
        bridge_flows=monitor_bridge_flows(),
        oracle_deviations=monitor_oracle_deviation(),
        data_gaps=gaps,
    )
