"""Contract tests — API outputs validate against plugin/schemas/*.json."""

from __future__ import annotations

from plugin.api.metrics import metrics_update
from plugin.api.risk import propose_action, risk_evaluate
from plugin.api.thesis import thesis_update

from tests.conftest import load_fixture, validate_instance


def test_risk_evaluate_matches_risk_state_schema() -> None:
    out = risk_evaluate("SPCX", portfolio_context={"cash_pct": 20})
    validate_instance(out, "RiskState.json")


def test_propose_action_matches_action_proposal_schema() -> None:
    out = propose_action("SPCX", portfolio_context={"cash_pct": 20})
    validate_instance(out, "ActionProposal.json")


def test_thesis_update_states_match_thesis_state_schema() -> None:
    sample = load_fixture("thesis_state_sample.json")
    out = thesis_update([sample], evidence_packet_id="pkt-demo-001")
    for state in out["states"]:
        validate_instance(state, "ThesisState.json")


def test_metrics_update_snapshots_match_metric_snapshot_schema() -> None:
    sample = load_fixture("metric_snapshot_sample.json")
    out = metrics_update([sample], recompute_status=False)
    for snapshot in out["snapshots"]:
        validate_instance(snapshot, "MetricSnapshot.json")
