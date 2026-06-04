"""Canonical thesis keys — must match ``schemas/ThesisState.json``."""

from __future__ import annotations

# Schema enum (source of truth)
THESIS_KEYS = frozenset(
    {
        "STARLINK_CASHFLOW_STRONG",
        "AI_HIGH_QUALITY_REVENUE",
        "STARSHIP_COST_CURVE",
        "LOCKUP_OVERWHELMS_DEMAND",
        "GOVERNANCE_DISCOUNT_EXPANDS",
        "VALUATION_REASONABLE",
    }
)

# Legacy V0 keys → schema keys (for migrating evidence packets / docs)
LEGACY_THESIS_KEY_MAP: dict[str, str] = {
    "connectivity_starlink": "STARLINK_CASHFLOW_STRONG",
    "space_starship_execution": "STARSHIP_COST_CURVE",
    "ai_capex_monetization": "AI_HIGH_QUALITY_REVENUE",
    "governance_control": "GOVERNANCE_DISCOUNT_EXPANDS",
    "supply_lockup_float": "LOCKUP_OVERWHELMS_DEMAND",
}

THESIS_DESCRIPTIONS: dict[str, str] = {
    "STARLINK_CASHFLOW_STRONG": (
        "Starlink scale, ARPU, and Connectivity segment cash generation are sustainable."
    ),
    "AI_HIGH_QUALITY_REVENUE": (
        "AI segment revenue quality and capex monetization (e.g. Anthropic) justify investment."
    ),
    "STARSHIP_COST_CURVE": (
        "Starship execution and launch cadence improve space segment economics."
    ),
    "LOCKUP_OVERWHELMS_DEMAND": (
        "Staged lock-up releases overwhelm post-IPO demand and float absorption."
    ),
    "GOVERNANCE_DISCOUNT_EXPANDS": (
        "Controlled-company governance and related-party risk widen valuation discount."
    ),
    "VALUATION_REASONABLE": (
        "Offered valuation is reasonable versus peers and sum-of-parts anchors."
    ),
}


def normalize_thesis_key(key: str) -> str:
    """Accept legacy snake_case keys; return schema enum value."""
    if key in THESIS_KEYS:
        return key
    mapped = LEGACY_THESIS_KEY_MAP.get(key)
    if mapped:
        return mapped
    raise ValueError(f"unknown thesis_key: {key}")


def probability_to_status(probability: float) -> str:
    if probability >= 0.65:
        return "BULL"
    if probability <= 0.35:
        return "BEAR"
    if 0.45 <= probability <= 0.55:
        return "WATCH"
    return "BASE"
