"""Reverse DCF — back-solve revenue CAGR / margin given target enterprise value.

External stress cases (e.g. New Constructs ~$500B) are labeled EXTERNAL_REFERENCE
(C-tier); they do not override SEC A-tier segment financials.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import yaml

from plugin.valuation.sec_fy25 import FY25_REVENUE_MUSD

_VALUATION_DIR = Path(__file__).resolve().parent
_ANCHORS_PATH = _VALUATION_DIR / "price_anchors.yaml"

# New Constructs-style stress case — EXTERNAL_REFERENCE, not verified
EXTERNAL_REFERENCE_STRESS_CASES: list[dict[str, Any]] = [
    {
        "id": "new_constructs_bear",
        "provider": "New Constructs",
        "cfa_tier": "C",
        "evidence_grade": "C",
        "target_ev_usd_bn": 500.0,
        "source_note": "Third-party bear case cited in valuation-research workstream",
        "verified_model": False,
        "conflict_flags": ["EXTERNAL_DCF_NOT_VERIFIED", "BELOW_MORNINGSTAR_ANCHOR"],
    },
]


def _load_anchors() -> dict[str, Any]:
    with _ANCHORS_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def solve_required_cagr(
    target_ev_usd_bn: float,
    *,
    base_revenue_musd: float | None = None,
    terminal_ebitda_margin: float = 0.25,
    years: int = 10,
    discount_rate: float = 0.10,
    terminal_growth: float = 0.03,
    ebitda_to_ev_multiple: float = 12.0,
) -> dict[str, Any]:
    """Back-solve constant revenue CAGR needed to justify *target_ev_usd_bn*.

    Simplified Gordon-style terminal value on EBITDA at year *years*; for stress
    testing only — not a production DCF model.
    """
    revenue0 = base_revenue_musd or float(FY25_REVENUE_MUSD["consolidated"])
    target_ev = target_ev_usd_bn * 1_000.0  # USD millions

    def ev_at_cagr(cagr: float) -> float:
        rev = revenue0
        pv_fcf = 0.0
        for t in range(1, years + 1):
            rev *= 1.0 + cagr
            ebitda = rev * terminal_ebitda_margin
            pv_fcf += ebitda / ((1.0 + discount_rate) ** t)
        terminal_ebitda = rev * (1.0 + terminal_growth) * terminal_ebitda_margin
        terminal_value = terminal_ebitda * ebitda_to_ev_multiple
        pv_terminal = terminal_value / ((1.0 + discount_rate) ** years)
        return pv_fcf + pv_terminal

    lo, hi = -0.20, 0.80
    for _ in range(64):
        mid = (lo + hi) / 2.0
        if ev_at_cagr(mid) < target_ev:
            lo = mid
        else:
            hi = mid
    required_cagr = (lo + hi) / 2.0

    terminal_revenue = revenue0 * ((1.0 + required_cagr) ** years)
    return {
        "target_ev_usd_bn": target_ev_usd_bn,
        "base_revenue_musd": revenue0,
        "required_revenue_cagr": round(required_cagr, 4),
        "required_revenue_cagr_pct": round(required_cagr * 100.0, 2),
        "terminal_revenue_musd": round(terminal_revenue, 1),
        "terminal_ebitda_margin_assumed": terminal_ebitda_margin,
        "years": years,
        "discount_rate": discount_rate,
        "ebitda_to_ev_multiple": ebitda_to_ev_multiple,
        "sec_revenue_grade": "A",
        "model_tier": "INTERNAL_STRESS",
        "notes": "Reverse solve for illustration; margin and multiple are assumptions.",
    }


def reverse_dcf_stress(
    *,
    include_external_references: bool = True,
) -> dict[str, Any]:
    """Run reverse DCF against anchors and external C-tier stress cases."""
    anchors = _load_anchors().get("anchors", {})
    cases: list[dict[str, Any]] = []

    dcf_anchor = anchors.get("dcf_conservative_anchor", {})
    if dcf_anchor.get("enterprise_value_usd_bn"):
        row = solve_required_cagr(float(dcf_anchor["enterprise_value_usd_bn"]))
        row["anchor_id"] = "dcf_conservative_anchor"
        row["cfa_tier"] = dcf_anchor.get("cfa_tier", "C")
        row["evidence_grade"] = dcf_anchor.get("evidence_grade", "C")
        cases.append(row)

    ipo = anchors.get("ipo_issue_anchor", {})
    if ipo.get("enterprise_value_usd_bn"):
        row = solve_required_cagr(float(ipo["enterprise_value_usd_bn"]))
        row["anchor_id"] = "ipo_issue_anchor"
        row["cfa_tier"] = ipo.get("cfa_tier", "A")
        row["evidence_grade"] = ipo.get("evidence_grade", "A")
        cases.append(row)

    if include_external_references:
        for ext in EXTERNAL_REFERENCE_STRESS_CASES:
            row = solve_required_cagr(float(ext["target_ev_usd_bn"]))
            row.update(
                {
                    "anchor_id": ext["id"],
                    "cfa_tier": ext["cfa_tier"],
                    "evidence_grade": ext["evidence_grade"],
                    "source_type": "EXTERNAL_REFERENCE",
                    "provider": ext["provider"],
                    "verified_model": ext["verified_model"],
                    "conflict_flags": ext.get("conflict_flags", []),
                }
            )
            cases.append(row)

    return {
        "method": "reverse_dcf",
        "cases": cases,
        "disclaimer": "Stress testing only; external cases are C-tier and unverified.",
    }


def implied_margin_at_cagr(
    target_ev_usd_bn: float,
    revenue_cagr: float,
    *,
    base_revenue_musd: float | None = None,
    years: int = 10,
    discount_rate: float = 0.10,
    terminal_growth: float = 0.03,
    ebitda_to_ev_multiple: float = 12.0,
) -> dict[str, Any]:
    """Given fixed CAGR, back-solve terminal EBITDA margin to hit target EV."""
    revenue0 = base_revenue_musd or float(FY25_REVENUE_MUSD["consolidated"])
    target_ev = target_ev_usd_bn * 1_000.0

    def ev_at_margin(margin: float) -> float:
        rev = revenue0
        pv = 0.0
        for t in range(1, years + 1):
            rev *= 1.0 + revenue_cagr
            ebitda = rev * margin
            pv += ebitda / ((1.0 + discount_rate) ** t)
        terminal_rev = rev * (1.0 + terminal_growth)
        tv = terminal_rev * margin * ebitda_to_ev_multiple
        pv += tv / ((1.0 + discount_rate) ** years)
        return pv

    lo, hi = 0.0, 0.80
    for _ in range(64):
        mid = (lo + hi) / 2.0
        if ev_at_margin(mid) < target_ev:
            lo = mid
        else:
            hi = mid
    margin = (lo + hi) / 2.0
    if math.isnan(margin):
        margin = 0.0
    return {
        "target_ev_usd_bn": target_ev_usd_bn,
        "revenue_cagr": revenue_cagr,
        "required_terminal_ebitda_margin": round(margin, 4),
        "required_terminal_ebitda_margin_pct": round(margin * 100.0, 2),
    }
