"""Contract tests — API outputs and registry entries vs JSON Schema."""

from __future__ import annotations

import yaml

from plugin.api import risk, thesis
from plugin.contracts import validate_against_schema
from plugin.metrics.threshold_engine import _iter_metric_defs, load_registry
from plugin.models.bayesian_thesis import run_bayesian_thesis
from plugin.models.thesis_keys import LEGACY_THESIS_KEY_MAP, normalize_thesis_key


def test_risk_evaluate_matches_schema() -> None:
    state = risk.risk_evaluate("SPCX", portfolio_context={"cash_pct": 20})
    validate_against_schema(state, "RiskState")


def test_propose_action_matches_schema() -> None:
    proposal = risk.propose_action("SPCX", portfolio_context={"cash_pct": 20})
    validate_against_schema(proposal, "ActionProposal")


def test_get_thesis_state_matches_schema() -> None:
    payload = thesis.get_thesis_state("SPCX")
    assert payload["asset"] == "SPCX"
    assert len(payload["theses"]) == 6
    for row in payload["theses"]:
        validate_against_schema(row, "ThesisState")


def test_legacy_thesis_key_normalization() -> None:
    for legacy, canonical in LEGACY_THESIS_KEY_MAP.items():
        assert normalize_thesis_key(legacy) == canonical


def test_bayesian_thesis_schema_states() -> None:
    result = run_bayesian_thesis()
    for row in result.payload["thesis_states"]:
        validate_against_schema(row, "ThesisState")


def test_registry_metric_definitions() -> None:
    registry = load_registry()
    for metric_def in _iter_metric_defs(registry):
        amber = metric_def.get("amber_threshold")
        red = metric_def.get("red_threshold")
        assert amber is None or isinstance(amber, (int, float))
        assert red is None or isinstance(red, (int, float))
        validate_against_schema(metric_def, "MetricDefinition")
