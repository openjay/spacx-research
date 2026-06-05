"""Tests — valuation MetricSnapshot export and research freshness."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yaml

from plugin.valuation.export_snapshots import (
    build_export_payload,
    export_snapshots,
    snapshot_ref,
    valuation_snapshot_refs,
)
from plugin.valuation.freshness import (
    effective_tier,
    freshness_weight,
    is_expired,
)
from plugin.valuation.implied_multiples import valuation_metrics_at_price
from runtime.packets import NextActionPacket, ThesisUpdatePacket, nap_from_blockers

from tests.conftest import ROOT, validate_instance

ASSUMPTION_DIR = ROOT / "workstreams" / "valuation-research" / "assumptions"


def test_build_export_payload_has_six_snapshots() -> None:
    payload = build_export_payload(as_of="2026-06-05T12:00:00Z")
    assert len(payload["snapshots"]) == 6
    assert set(payload["anchors"]) == {
        "dcf_conservative_anchor",
        "ipo_issue_anchor",
        "fomo_trading_band",
    }
    assert payload["anchors"]["ipo_issue_anchor"]["cfa_tier"] == "A"
    assert payload["anchors"]["dcf_conservative_anchor"]["price_usd"] == 60.0
    assert payload["anchors"]["ipo_issue_anchor"]["price_usd"] == 135.0
    assert payload["anchors"]["fomo_trading_band"]["price_usd_low"] == 185.0


def test_export_snapshots_validate_against_schema(tmp_path: Path) -> None:
    out = tmp_path / "metric_snapshots.json"
    payload = export_snapshots(out, as_of="2026-06-05T12:00:00Z")
    assert out.is_file()
    for snapshot in payload["snapshots"]:
        validate_instance(snapshot, "MetricSnapshot.json")


def test_ipo_anchor_metrics_match_valuation_engine() -> None:
    payload = build_export_payload(as_of="2026-06-05T12:00:00Z")
    expected = valuation_metrics_at_price(135.0)
    by_id = {
        s["metric_id"]: s
        for s in payload["snapshots"]
        if s.get("period") == "IPO_issue_anchor_135"
    }
    assert by_id["IMPLIED_MARKET_CAP_USD"]["value"] == expected["IMPLIED_MARKET_CAP_USD"]
    assert by_id["EV_TO_REVENUE_FY25"]["value"] == expected["EV_TO_REVENUE_FY25"]
    assert by_id["EV_TO_ADJ_EBITDA_FY25"]["value"] == expected["EV_TO_ADJ_EBITDA_FY25"]
    assert by_id["PRICE_VS_DCF_ANCHOR_PCT"]["value"] == 125.0
    assert by_id["PRICE_VS_DCF_ANCHOR_PCT"]["status"] == "AMBER"


def test_dcf_anchor_multiples_period_tagged() -> None:
    payload = build_export_payload(as_of="2026-06-05T12:00:00Z")
    dcf = [s for s in payload["snapshots"] if s.get("period") == "DCF_conservative_anchor_60"]
    assert len(dcf) == 2
    ids = {s["metric_id"] for s in dcf}
    assert ids == {"EV_TO_REVENUE_FY25", "EV_TO_ADJ_EBITDA_FY25"}
    for snap in dcf:
        assert snap["evidence_refs"][-1] == "price_context:60.0"


def test_assumption_files_include_freshness_fields() -> None:
    for path in sorted(ASSUMPTION_DIR.glob("*.yaml")):
        packet = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert "as_of" in packet
        assert "freshness_days" in packet
        assert "expires_at" in packet
        validate_instance(packet, "ExternalResearchPacket.json")


def test_freshness_downgrades_expired_c_tier() -> None:
    packet = {
        "tier": "C",
        "as_of": "2026-01-01",
        "freshness_days": 30,
    }
    assert is_expired(packet, today=date(2026, 6, 5))
    assert effective_tier(packet, today=date(2026, 6, 5)) == "D"
    assert freshness_weight(packet, today=date(2026, 6, 5)) == 0.35


def test_freshness_a_tier_never_downgrades() -> None:
    packet = {"tier": "A", "as_of": "2020-01-01", "freshness_days": 1}
    assert effective_tier(packet, today=date(2026, 6, 5)) == "A"
    assert freshness_weight(packet, today=date(2026, 6, 5)) == 1.0


def test_packets_include_metric_snapshot_refs() -> None:
    refs = valuation_snapshot_refs()
    assert snapshot_ref("EV_TO_REVENUE_FY25", 135) in refs
    thesis = ThesisUpdatePacket()
    nap = NextActionPacket()
    assert thesis.metric_snapshot_refs == refs
    assert nap.metric_snapshot_refs == refs
    blocker_nap = nap_from_blockers({"FINAL_PROSPECTUS_PENDING": True})
    assert blocker_nap.metric_snapshot_refs == refs


def test_cli_writes_default_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "runtime" / "data" / "metric_snapshots.json"
    export_snapshots(out, as_of="2026-06-05T12:00:00Z")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["computed_by"] == "valuation_export_v1"
    assert len(data["snapshots"]) == 6
