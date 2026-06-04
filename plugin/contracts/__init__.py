"""JSON Schema contract validation for plugin API outputs."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator

_SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"


@lru_cache(maxsize=32)
def _load_schema(schema_name: str) -> dict[str, Any]:
    name = schema_name if schema_name.endswith(".json") else f"{schema_name}.json"
    path = _SCHEMA_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"schema not found: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=32)
def _validator(schema_name: str) -> Draft202012Validator:
    schema = _load_schema(schema_name)
    return Draft202012Validator(schema)


def validate_against_schema(obj: Any, schema_name: str) -> None:
    """Raise :class:`jsonschema.ValidationError` if *obj* does not match *schema_name*."""
    _validator(schema_name).validate(obj)


def is_valid(obj: Any, schema_name: str) -> bool:
    try:
        validate_against_schema(obj, schema_name)
    except jsonschema.ValidationError:
        return False
    return True


def contract_probe_ok() -> bool:
    """Registry, risk, and thesis API outputs validate against JSON Schema."""
    try:
        from plugin.api import risk, thesis
        from plugin.metrics.threshold_engine import _iter_metric_defs, load_registry

        validate_against_schema(
            risk.risk_evaluate("SPCX", portfolio_context={"cash_pct": 20}),
            "RiskState",
        )
        validate_against_schema(
            risk.propose_action("SPCX", portfolio_context={"cash_pct": 20}),
            "ActionProposal",
        )
        payload = thesis.get_thesis_state("SPCX")
        for row in payload["theses"]:
            validate_against_schema(row, "ThesisState")
        registry = load_registry()
        for metric_def in _iter_metric_defs(registry):
            validate_against_schema(metric_def, "MetricDefinition")
    except Exception:
        return False
    return True
