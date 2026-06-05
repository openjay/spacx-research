"""SOTP 4-layer calculator — segment weights from SEC FY2025 revenue/EBITDA."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from plugin.valuation.sec_fy25 import FY25_ADJ_EBITDA_MUSD, FY25_REVENUE_MUSD

_VALUATION_DIR = Path(__file__).resolve().parent
_SCENARIOS_PATH = _VALUATION_DIR / "scenario_bands.yaml"

LAYER_SEGMENTS = ("connectivity", "space", "ai")


def compute_sotp_weights(
    *,
    ai_probability_haircut: float = 0.35,
    include_otm_layer: bool = True,
    otm_weight_pct: float = 5.0,
) -> dict[str, Any]:
    """Compute revenue- and EBITDA-based SOTP weights from SEC FY2025 actuals.

    Args:
        ai_probability_haircut: Probability weight on AI layer (0–1).
        include_otm_layer: Reserve weight for orbital/Mars OTM option.
        otm_weight_pct: Percent of total EV attributed to OTM layer when enabled.
    """
    haircut = max(0.0, min(1.0, ai_probability_haircut))
    rev = {k: float(FY25_REVENUE_MUSD[k]) for k in LAYER_SEGMENTS}
    ebitda = {k: float(FY25_ADJ_EBITDA_MUSD[k]) for k in LAYER_SEGMENTS}

    total_rev = sum(rev.values())
    total_ebitda_pos = sum(max(0.0, ebitda[k]) for k in LAYER_SEGMENTS)

    rev_weights = {k: rev[k] / total_rev for k in LAYER_SEGMENTS}
    ebitda_weights = {
        k: (max(0.0, ebitda[k]) / total_ebitda_pos if total_ebitda_pos else 0.0)
        for k in LAYER_SEGMENTS
    }

    # AI layer discounted on both revenue and positive-EBITDA views
    rev_weights["ai"] *= haircut
    ebitda_weights["ai"] *= haircut

    # Renormalize core layers
    core_rev = sum(rev_weights[k] for k in LAYER_SEGMENTS)
    core_ebitda = sum(ebitda_weights[k] for k in LAYER_SEGMENTS)
    for k in LAYER_SEGMENTS:
        rev_weights[k] /= core_rev if core_rev else 1.0
        ebitda_weights[k] /= core_ebitda if core_ebitda else 1.0

    otm_pct = otm_weight_pct / 100.0 if include_otm_layer else 0.0
    scale = 1.0 - otm_pct
    for k in LAYER_SEGMENTS:
        rev_weights[k] *= scale
        ebitda_weights[k] *= scale

    layers = [
        {
            "layer_id": "starlink_base",
            "segment": "Connectivity",
            "sec_fy25_revenue_musd": rev["connectivity"],
            "sec_fy25_adj_ebitda_musd": ebitda["connectivity"],
            "revenue_weight_pct": round(rev_weights["connectivity"] * 100.0, 2),
            "ebitda_weight_pct": round(ebitda_weights["connectivity"] * 100.0, 2),
        },
        {
            "layer_id": "launch_option",
            "segment": "Space",
            "sec_fy25_revenue_musd": rev["space"],
            "sec_fy25_adj_ebitda_musd": ebitda["space"],
            "revenue_weight_pct": round(rev_weights["space"] * 100.0, 2),
            "ebitda_weight_pct": round(ebitda_weights["space"] * 100.0, 2),
        },
        {
            "layer_id": "ai_discounted",
            "segment": "AI",
            "sec_fy25_revenue_musd": rev["ai"],
            "sec_fy25_adj_ebitda_musd": ebitda["ai"],
            "ai_probability_haircut": haircut,
            "revenue_weight_pct": round(rev_weights["ai"] * 100.0, 2),
            "ebitda_weight_pct": round(ebitda_weights["ai"] * 100.0, 2),
        },
    ]
    if include_otm_layer:
        layers.append(
            {
                "layer_id": "orbital_mars_otm",
                "segment": "Corporate",
                "evidence_grade": "D",
                "revenue_weight_pct": round(otm_pct * 100.0, 2),
                "ebitda_weight_pct": round(otm_pct * 100.0, 2),
            }
        )

    return {
        "method": "sotp_4_layer",
        "sec_period": "FY2025",
        "evidence_grade": "A",
        "sec_citation": "05-master-evidence-tables.md Table 2",
        "ai_probability_haircut": haircut,
        "layers": layers,
        "consolidated_revenue_musd": float(FY25_REVENUE_MUSD["consolidated"]),
        "consolidated_adj_ebitda_musd": float(FY25_ADJ_EBITDA_MUSD["consolidated"]),
    }


def allocate_ev_to_layers(
    enterprise_value_usd_bn: float,
    *,
    ai_probability_haircut: float = 0.35,
) -> dict[str, Any]:
    """Map a target EV across SOTP layers using SEC-informed weights."""
    weights = compute_sotp_weights(ai_probability_haircut=ai_probability_haircut)
    ev_musd = enterprise_value_usd_bn * 1_000.0
    allocation = []
    for layer in weights["layers"]:
        pct = layer.get("revenue_weight_pct", 0.0) / 100.0
        allocation.append(
            {
                "layer_id": layer["layer_id"],
                "ev_usd_mn": round(ev_musd * pct, 1),
                "weight_pct": layer.get("revenue_weight_pct", 0.0),
            }
        )
    return {
        "enterprise_value_usd_bn": enterprise_value_usd_bn,
        "allocation": allocation,
        "weights": weights,
    }


def sotp_summary() -> dict[str, Any]:
    """Default SOTP summary plus scenario band cross-reference."""
    weights = compute_sotp_weights()
    scenarios: dict[str, Any] = {}
    if _SCENARIOS_PATH.is_file():
        with _SCENARIOS_PATH.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        scenarios = data.get("scenarios", {})
    return {"weights": weights, "scenario_bands": scenarios}
