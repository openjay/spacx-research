"""
Settlement abstraction — JSON-serializable ``SettlementProfile`` for RWA instruments.

Normalizes trading hours, settlement cadence, redemption windows, transfer rules,
custodian, and legal claim type for cross-venue comparison (no execution in V0).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass
class SettlementProfile:
    """
    Canonical settlement metadata for an RWA or tokenized fund line.

    Example JSON shape::

        {
          "instrument_id": "TBILL-ONCHAIN-A",
          "trading_hours": "24x7",
          "settlement": "T+0 on-chain / T+1 off-chain",
          "redemption_window": "daily 09:00-17:00 ET",
          "transfer_restriction": "accredited_only",
          "custodian": "Example Trust Co",
          "legal_claim": "beneficial_interest_in_underlying_pool"
        }
    """

    instrument_id: str
    trading_hours: str
    settlement: str
    redemption_window: str
    transfer_restriction: str
    custodian: str
    legal_claim: str
    jurisdiction: str | None = None
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}

    def to_json(self, *, indent: int | None = None) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, indent=indent)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SettlementProfile:
        known = {
            "instrument_id",
            "trading_hours",
            "settlement",
            "redemption_window",
            "transfer_restriction",
            "custodian",
            "legal_claim",
            "jurisdiction",
            "notes",
        }
        kwargs = {k: data[k] for k in known if k in data}
        required = (
            "instrument_id",
            "trading_hours",
            "settlement",
            "redemption_window",
            "transfer_restriction",
            "custodian",
            "legal_claim",
        )
        missing = [k for k in required if k not in kwargs]
        if missing:
            raise ValueError(f"SettlementProfile missing fields: {missing}")
        return cls(**kwargs)  # type: ignore[arg-type]


def default_spcx_adjacent_profile() -> SettlementProfile:
    """V0 placeholder profile for research-side RWA comparison."""
    return SettlementProfile(
        instrument_id="RWA-RESEARCH-DEFAULT",
        trading_hours="24x7 (crypto venues) / RTH (traditional)",
        settlement="variable by venue",
        redemption_window="issuer-defined; verify prospectus",
        transfer_restriction="jurisdiction_and_whitelist",
        custodian="TBD — verify offering docs",
        legal_claim="contractual — not grade A without SEC excerpt",
        jurisdiction="US",
        notes="V0 stub — no custody or legal verification",
    )
