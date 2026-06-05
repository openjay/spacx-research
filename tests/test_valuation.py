"""Smoke tests — valuation layer, schemas, and OBSERVE_ONLY gate."""

from __future__ import annotations

from pathlib import Path

import yaml

from plugin.api.risk import propose_action
from plugin.valuation.implied_multiples import (
    compute_implied_multiples,
    price_vs_dcf_anchor_pct,
    valuation_metrics_at_price,
)
from plugin.valuation.reverse_dcf import reverse_dcf_stress, solve_required_cagr
from plugin.valuation.risk_gate import should_observe_only
from plugin.valuation.sotp_calculator import compute_sotp_weights, sotp_summary

from tests.conftest import ROOT, validate_instance

SCHEMA_DIR = ROOT / "plugin" / "schemas"
VALUATION_DIR = ROOT / "plugin" / "valuation"


def test_price_anchors_yaml_loads_three_anchors() -> None:
    path = VALUATION_DIR / "price_anchors.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    anchors = data["anchors"]
    assert "dcf_conservative_anchor" in anchors
    assert "ipo_issue_anchor" in anchors
    assert "fomo_trading_band" in anchors
    assert anchors["dcf_conservative_anchor"]["cfa_tier"] == "C"
    assert anchors["ipo_issue_anchor"]["evidence_grade"] == "A"
    assert anchors["fomo_trading_band"]["fundamental_claim"] is False


def test_scenario_bands_yaml_has_four_scenarios() -> None:
    path = VALUATION_DIR / "scenario_bands.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    scenarios = data["scenarios"]
    assert set(scenarios) >= {"conservative", "base", "bull", "ipo_bull"}
    assert scenarios["conservative"]["ev_usd_bn_low"] == 500


def test_sotp_weights_sum_near_one_hundred() -> None:
    out = compute_sotp_weights(ai_probability_haircut=0.35)
    total = sum(layer["revenue_weight_pct"] for layer in out["layers"])
    assert 99.0 <= total <= 101.0
    assert out["evidence_grade"] == "A"


def test_implied_multiples_at_ipo_price() -> None:
    out = compute_implied_multiples(135.0)
    assert out["ev_to_revenue_fy25"] is not None
    assert out["ev_to_revenue_fy25"] > 50
    assert out["ev_to_adj_ebitda_fy25"] is not None
    metrics = valuation_metrics_at_price(135.0)
    assert metrics["IMPLIED_MARKET_CAP_USD"] > 1.7e12


def test_price_vs_dcf_anchor_pct_at_ipo() -> None:
    out = price_vs_dcf_anchor_pct(135.0)
    assert out["price_vs_dcf_anchor_pct"] == 125.0


def test_reverse_dcf_stress_includes_external_reference() -> None:
    out = reverse_dcf_stress()
    ids = {c["anchor_id"] for c in out["cases"]}
    assert "new_constructs_bear" in ids
    assert "ipo_issue_anchor" in ids
    nc = next(c for c in out["cases"] if c["anchor_id"] == "new_constructs_bear")
    assert nc["source_type"] == "EXTERNAL_REFERENCE"
    assert nc["required_revenue_cagr"] > 0


def test_solve_required_cagr_monotonic() -> None:
    low = solve_required_cagr(500.0)
    high = solve_required_cagr(1750.0)
    assert high["required_revenue_cagr"] > low["required_revenue_cagr"]


def test_sotp_summary_includes_scenarios() -> None:
    out = sotp_summary()
    assert "weights" in out
    assert "conservative" in out["scenario_bands"]


def test_external_research_packet_schema() -> None:
    sample = {
        "packet_id": "ext-morningstar-001",
        "source": "Morningstar via Reuters",
        "tier": "C",
        "conflict_flags": ["EXTERNAL_DCF_NOT_VERIFIED"],
        "fair_value_usd": 780_000_000_000,
        "fair_value_basis": "enterprise_value",
        "implied_price": 60.0,
        "assumptions": ["Third-party DCF; not verified against SEC filings"],
        "as_of": "2026-06-01",
        "verified_model": False,
    }
    validate_instance(sample, "ExternalResearchPacket.json")


def test_external_research_assumption_files_match_schema() -> None:
    assumption_dir = ROOT / "workstreams" / "valuation-research" / "assumptions"
    for path in sorted(assumption_dir.glob("*.yaml")):
        packet = yaml.safe_load(path.read_text(encoding="utf-8"))
        validate_instance(packet, "ExternalResearchPacket.json")


def test_evidence_packet_accepts_conflict_flags() -> None:
    sample = {
        "packet_id": "pkt-val-001",
        "source_id": "sec-s1a2",
        "source_type": "SEC_EDGAR",
        "confidence": "A",
        "extracted_at": "2026-06-03T12:00:00Z",
        "conflict_flags": ["FINAL_PROSPECTUS_PENDING"],
        "claims": [
            {
                "claim": "Expected IPO price",
                "metric_id": "W01_ipo_price_usd",
                "value": 135.0,
                "unit": "USD",
                "period": "post_ipo",
            }
        ],
    }
    validate_instance(sample, "EvidencePacket.json")


def test_observe_only_when_price_above_2x_dcf_anchor() -> None:
    gate = should_observe_only(150.0, active_blockers={"FINAL_PROSPECTUS_PENDING", "FIRST_EARNINGS_PENDING"})
    assert gate["observe_only"] is True
    assert gate["proposal_type"] == "OBSERVE_ONLY"
    below = should_observe_only(100.0, active_blockers={"FINAL_PROSPECTUS_PENDING"})
    assert below["observe_only"] is False


def test_propose_action_valuation_gate() -> None:
    out = propose_action(
        "SPCX",
        portfolio_context={"spcx_price_usd": 200.0},
        proposal_type="WATCHLIST_ADD",
    )
    assert out["proposal_type"] == "OBSERVE_ONLY"
    assert "DCF conservative anchor" in out["reason"] or "2x" in out["reason"]
    validate_instance(out, "ActionProposal.json")


def test_valuation_agent_files_exist() -> None:
    agent_dir = ROOT / "plugin" / "agents" / "ValuationAnalystAgent"
    assert (agent_dir / "agent.yaml").is_file()
    assert (agent_dir / "README.md").is_file()
    text = (agent_dir / "agent.yaml").read_text(encoding="utf-8")
    assert "override_sec_segment_totals" in text
    assert "auto_trade" in text
