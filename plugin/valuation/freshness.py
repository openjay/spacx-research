"""Research packet freshness — downgrade expired C-tier external evidence."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

DEFAULT_FRESHNESS_DAYS: dict[str, int] = {
    "A": 365,
    "B": 90,
    "C": 30,
    "D": 7,
    "OBSERVATION": 3,
}

EXPIRED_C_TIER_WEIGHT = 0.35


def parse_as_of(value: str) -> date:
    """Parse ISO date or date-time string to date."""
    if "T" in value:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    return date.fromisoformat(value)


def _expiry_date(packet: dict[str, Any]) -> date | None:
    expires_at = packet.get("expires_at")
    if expires_at:
        return parse_as_of(str(expires_at))

    as_of_raw = packet.get("as_of")
    if not as_of_raw:
        return None

    tier = str(packet.get("tier", "C"))
    freshness_days = packet.get("freshness_days")
    if freshness_days is None:
        freshness_days = DEFAULT_FRESHNESS_DAYS.get(tier, 30)
    return parse_as_of(str(as_of_raw)) + timedelta(days=int(freshness_days))


def is_expired(packet: dict[str, Any], *, today: date | None = None) -> bool:
    """True when packet is past expires_at or as_of + freshness_days."""
    expiry = _expiry_date(packet)
    if expiry is None:
        return False
    ref = today or date.today()
    return ref > expiry


def effective_tier(packet: dict[str, Any], *, today: date | None = None) -> str:
    """Return tier; downgrade C-tier to D when expired."""
    tier = str(packet.get("tier", "C"))
    if tier == "A":
        return tier
    if tier == "C" and is_expired(packet, today=today):
        return "D"
    return tier


def freshness_weight(packet: dict[str, Any], *, today: date | None = None) -> float:
    """Weight multiplier for SOTP/thesis blending; C-tier decays when expired."""
    tier = str(packet.get("tier", "C"))
    if tier == "A":
        return 1.0
    if tier == "C" and is_expired(packet, today=today):
        return EXPIRED_C_TIER_WEIGHT
    if is_expired(packet, today=today):
        return EXPIRED_C_TIER_WEIGHT
    return 1.0
