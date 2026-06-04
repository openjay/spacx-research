"""Threshold engine — registry load and sample evaluation."""

from __future__ import annotations

from plugin.metrics.threshold_engine import (
    Status,
    evaluate_snapshot,
    load_registry,
    metric_count,
    sample_evaluations,
)


def test_registry_loads_with_watch_metrics() -> None:
    registry = load_registry()
    assert registry["asset"] == "SPCX"
    assert len(registry.get("watch_metrics", [])) > 0
    counts = metric_count(registry)
    assert counts["total_scored"] > 0
    assert counts["blockers"] >= 1


def test_sample_evaluation_baseline_is_mostly_green() -> None:
    samples = sample_evaluations()
    baseline = samples["baseline_q1_2026"]
    assert baseline["asset"] == "SPCX"
    summary = baseline["summary"]
    assert summary.get(Status.GREEN.value, 0) > 0


def test_stressed_snapshot_triggers_amber_or_blockers() -> None:
    samples = sample_evaluations()
    stressed = samples["stressed_q2_2026"]
    summary = stressed["summary"]
    amber_or_red = summary.get(Status.AMBER.value, 0) + summary.get(Status.RED.value, 0)
    blockers = stressed.get("blockers", [])
    assert amber_or_red > 0 or len(blockers) > 0


def test_evaluate_snapshot_unknown_without_values() -> None:
    registry = load_registry()
    out = evaluate_snapshot({"values": {}}, registry=registry)
    assert Status.UNKNOWN.value in out["summary"]
