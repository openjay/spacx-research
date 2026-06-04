"""Smoke tests — each run_* entrypoint returns ModelResult."""

from __future__ import annotations

from datetime import date

from plugin.models import (
    ModelResult,
    run_anomaly_detection,
    run_bayesian_thesis,
    run_event_study,
    run_factor_exposure,
    run_forecast_scoring,
    run_portfolio_risk_budget,
    run_regime_detection,
)
from plugin.models._types import ModelResult as ModelResultType


def test_run_bayesian_thesis_returns_model_result() -> None:
    result = run_bayesian_thesis()
    assert isinstance(result, ModelResultType)
    assert result.model_name


def test_run_event_study_returns_model_result() -> None:
    result = run_event_study("2026-03-15", "424B4")
    assert isinstance(result, ModelResult)
    assert result.audit.model


def test_run_regime_detection_returns_model_result() -> None:
    result = run_regime_detection()
    assert isinstance(result, ModelResult)


def test_run_factor_exposure_returns_model_result() -> None:
    result = run_factor_exposure()
    assert isinstance(result, ModelResult)


def test_run_anomaly_detection_returns_model_result() -> None:
    result = run_anomaly_detection()
    assert isinstance(result, ModelResult)


def test_run_portfolio_risk_budget_returns_model_result() -> None:
    result = run_portfolio_risk_budget()
    assert isinstance(result, ModelResult)


def test_run_forecast_scoring_returns_model_result() -> None:
    result = run_forecast_scoring()
    assert isinstance(result, ModelResult)
