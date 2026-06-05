"""Implied EV/Revenue and EV/EBITDA at arbitrary price using SEC cash/debt."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from plugin.valuation.sec_fy25 import (
    FY25_ADJ_EBITDA_MUSD,
    FY25_REVENUE_MUSD,
    POST_IPO_TOTAL_SHARES,
    sec_balance_sheet,
)

_VALUATION_DIR = Path(__file__).resolve().parent
_ANCHORS_PATH = _VALUATION_DIR / "price_anchors.yaml"


def implied_market_cap_usd(price_usd: float, shares: int | float | None = None) -> float:
    """Market cap in USD at *price_usd* per share."""
    n = float(shares if shares is not None else POST_IPO_TOTAL_SHARES)
    return price_usd * n


def enterprise_value_usd(
    price_usd: float,
    *,
    shares: int | float | None = None,
    pro_forma_cash: bool = False,
) -> dict[str, Any]:
    """EV = market cap + debt - cash (SEC filing inputs)."""
    bs = sec_balance_sheet(pro_forma_cash=pro_forma_cash)
    mcap = implied_market_cap_usd(price_usd, shares)
    cash = bs["cash_musd"] * 1_000_000.0
    debt = bs["debt_musd"] * 1_000_000.0
    ev = mcap + debt - cash
    return {
        "price_usd": price_usd,
        "market_cap_usd": mcap,
        "enterprise_value_usd": ev,
        "cash_usd": cash,
        "debt_usd": debt,
        "shares_outstanding": bs["shares_outstanding"],
        "pro_forma_cash": pro_forma_cash,
        "sec_citation": bs["sec_citation"],
        "evidence_grade": "A",
    }


def compute_implied_multiples(
    price_usd: float,
    *,
    shares: int | float | None = None,
    pro_forma_cash: bool = False,
) -> dict[str, Any]:
    """EV/Revenue and EV/Adj. EBITDA at *price_usd* using FY2025 SEC actuals."""
    ev_block = enterprise_value_usd(price_usd, shares=shares, pro_forma_cash=pro_forma_cash)
    ev = ev_block["enterprise_value_usd"]
    rev = FY25_REVENUE_MUSD["consolidated"] * 1_000_000.0
    ebitda = FY25_ADJ_EBITDA_MUSD["consolidated"] * 1_000_000.0
    ev_to_rev = ev / rev if rev else None
    ev_to_ebitda = ev / ebitda if ebitda else None
    return {
        **ev_block,
        "fy25_revenue_usd": rev,
        "fy25_adj_ebitda_usd": ebitda,
        "ev_to_revenue_fy25": round(ev_to_rev, 2) if ev_to_rev is not None else None,
        "ev_to_adj_ebitda_fy25": round(ev_to_ebitda, 2) if ev_to_ebitda is not None else None,
        "period": "FY2025",
    }


def price_vs_dcf_anchor_pct(
    price_usd: float,
    anchors_path: Path | None = None,
) -> dict[str, Any]:
    """Percent premium/discount vs dcf_conservative_anchor from price_anchors.yaml."""
    path = anchors_path or _ANCHORS_PATH
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    anchor = data.get("anchors", {}).get("dcf_conservative_anchor", {})
    ref = float(anchor.get("price_usd_per_share", 60.0))
    pct = ((price_usd - ref) / ref) * 100.0 if ref else 0.0
    return {
        "price_usd": price_usd,
        "dcf_anchor_price_usd": ref,
        "price_vs_dcf_anchor_pct": round(pct, 2),
        "anchor_cfa_tier": anchor.get("cfa_tier", "C"),
        "anchor_verified_model": anchor.get("verified_model", False),
        "conflict_flags": anchor.get("conflict_flags", []),
    }


def valuation_metrics_at_price(
    price_usd: float,
    *,
    pro_forma_cash: bool = False,
) -> dict[str, Any]:
    """Bundle registry-facing valuation metrics for a given price."""
    multiples = compute_implied_multiples(price_usd, pro_forma_cash=pro_forma_cash)
    anchor_cmp = price_vs_dcf_anchor_pct(price_usd)
    return {
        "IMPLIED_MARKET_CAP_USD": multiples["market_cap_usd"],
        "EV_TO_REVENUE_FY25": multiples["ev_to_revenue_fy25"],
        "EV_TO_ADJ_EBITDA_FY25": multiples["ev_to_adj_ebitda_fy25"],
        "PRICE_VS_DCF_ANCHOR_PCT": anchor_cmp["price_vs_dcf_anchor_pct"],
        "detail": {"multiples": multiples, "anchor_comparison": anchor_cmp},
    }
