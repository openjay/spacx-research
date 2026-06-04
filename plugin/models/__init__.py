"""
SPACX statistical models (V0).

Auditable interfaces for event studies, thesis updating, regimes, factors,
anomalies, portfolio risk budgets, and forecast scoring.
"""

from plugin.models._types import AlertLevel, AuditRecord, DataRequirement, ModelPhase, ModelResult
from plugin.models.anomaly_detection import (
    AnomalyDetectionModel,
    DEFAULT_THRESHOLDS,
    MetricObservation,
    MetricThreshold,
    run_anomaly_detection,
)
from plugin.models.bayesian_thesis import (
    THESIS_KEYS,
    BayesianThesisModel,
    EvidencePacket,
    ThesisState,
    run_bayesian_thesis,
)
from plugin.models.event_study import (
    EVENT_TYPES,
    AbnormalReturnPoint,
    EventStudyModel,
    EventWindow,
    PriceObservation,
    run_event_study,
)
from plugin.models.factor_exposure import (
    DEFAULT_FACTORS,
    DEFAULT_PEERS,
    FactorBeta,
    FactorExposureModel,
    ReturnSeries,
    run_factor_exposure,
)
from plugin.models.forecast_scoring import (
    AgentForecast,
    AgentScorecard,
    ForecastScoringModel,
    run_forecast_scoring,
)
from plugin.models.portfolio_risk_budget import (
    BudgetViolation,
    PortfolioRiskBudgetModel,
    PositionLine,
    RiskBudgetPolicy,
    THEMATIC_BUCKETS,
    run_portfolio_risk_budget,
)
from plugin.models.regime_detection import (
    REGIME_LABELS,
    RegimeClassification,
    RegimeDetectionModel,
    RegimeFeatures,
    run_regime_detection,
)

__all__ = [
    "AlertLevel",
    "AuditRecord",
    "DataRequirement",
    "ModelPhase",
    "ModelResult",
    "EVENT_TYPES",
    "THESIS_KEYS",
    "REGIME_LABELS",
    "DEFAULT_FACTORS",
    "DEFAULT_PEERS",
    "DEFAULT_THRESHOLDS",
    "THEMATIC_BUCKETS",
    "EventStudyModel",
    "EventWindow",
    "PriceObservation",
    "AbnormalReturnPoint",
    "run_event_study",
    "BayesianThesisModel",
    "EvidencePacket",
    "ThesisState",
    "run_bayesian_thesis",
    "RegimeDetectionModel",
    "RegimeFeatures",
    "RegimeClassification",
    "run_regime_detection",
    "FactorExposureModel",
    "ReturnSeries",
    "FactorBeta",
    "run_factor_exposure",
    "AnomalyDetectionModel",
    "MetricThreshold",
    "MetricObservation",
    "run_anomaly_detection",
    "PortfolioRiskBudgetModel",
    "RiskBudgetPolicy",
    "PositionLine",
    "BudgetViolation",
    "run_portfolio_risk_budget",
    "ForecastScoringModel",
    "AgentForecast",
    "AgentScorecard",
    "run_forecast_scoring",
]
