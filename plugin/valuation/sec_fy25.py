"""SEC FY2025 segment and balance-sheet inputs (A-tier).

Source: workstreams/sec-evidence-phase1/audit/05-master-evidence-tables.md
"""

from __future__ import annotations

from typing import Any

# USD millions unless noted
FY25_REVENUE_MUSD: dict[str, float] = {
    "space": 4_086,
    "connectivity": 11_387,
    "ai": 3_201,
    "consolidated": 18_674,
}

FY25_ADJ_EBITDA_MUSD: dict[str, float] = {
    "space": 653,
    "connectivity": 7_168,
    "ai": -1_237,
    "consolidated": 6_584,
}

# Shares and capital structure (post-IPO, S-1/A #2)
POST_IPO_TOTAL_SHARES = 13_075_865_175
POST_IPO_CLASS_A_SHARES = 7_380_196_910
IPO_PRICE_USD = 135.0

# Liquidity / debt (Mar 31, 2026 actual + filing terms)
CASH_ACTUAL_MUSD = 15_852
CASH_PRO_FORMA_POST_IPO_MUSD = 90_305
BRIDGE_LOAN_MUSD = 20_000
REVOLVING_FACILITY_MUSD = 5_000


def sec_balance_sheet(*, pro_forma_cash: bool = False) -> dict[str, Any]:
    """Return cash and debt figures for EV math."""
    return {
        "cash_musd": CASH_PRO_FORMA_POST_IPO_MUSD if pro_forma_cash else CASH_ACTUAL_MUSD,
        "debt_musd": BRIDGE_LOAN_MUSD,
        "debt_detail": {
            "bridge_loan_musd": BRIDGE_LOAN_MUSD,
            "revolving_facility_musd": REVOLVING_FACILITY_MUSD,
        },
        "shares_outstanding": POST_IPO_TOTAL_SHARES,
        "sec_citation": "05-master-evidence-tables.md Tables 1–3",
        "evidence_grade": "A",
    }
