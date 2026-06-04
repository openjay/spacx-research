"""Shared types for SPACX statistical models (V0)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any, Mapping, Sequence


class AlertLevel(str, Enum):
    """Monitoring severity aligned with CFA watch thresholds."""

    GREEN = "GREEN"
    AMBER = "AMBER"
    RED = "RED"


class ModelPhase(str, Enum):
    """Implementation maturity; V0 = interfaces + stub math."""

    V0 = "v0"
    V1 = "v1"  # numpy/pandas optional
    V2 = "v2"  # live market + SEC feeds


@dataclass(frozen=True)
class AuditRecord:
    """Immutable line in an auditable model run."""

    model: str
    version: str
    run_id: str
    timestamp: datetime
    inputs_hash: str
    parameters: Mapping[str, Any]
    outputs: Mapping[str, Any]
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "version": self.version,
            "run_id": self.run_id,
            "timestamp": self.timestamp.isoformat(),
            "inputs_hash": self.inputs_hash,
            "parameters": dict(self.parameters),
            "outputs": dict(self.outputs),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class DataRequirement:
    """Phase 3+ input contract documented in V0."""

    name: str
    source: str
    frequency: str
    required_from_phase: int = 3
    description: str = ""


@dataclass
class ModelResult:
    """Standard return envelope for all models."""

    model_name: str
    phase: ModelPhase
    payload: dict[str, Any]
    audit: AuditRecord
    data_gaps: list[DataRequirement] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_name": self.model_name,
            "phase": self.phase.value,
            "payload": self.payload,
            "audit": self.audit.to_dict(),
            "data_gaps": [
                {
                    "name": g.name,
                    "source": g.source,
                    "frequency": g.frequency,
                    "required_from_phase": g.required_from_phase,
                    "description": g.description,
                }
                for g in self.data_gaps
            ],
        }


def stable_hash(parts: Sequence[str]) -> str:
    """Deterministic short hash for audit trails (V0, non-crypto)."""
    acc = 0
    for p in parts:
        for ch in p:
            acc = (acc * 31 + ord(ch)) & 0xFFFFFFFF
    return format(acc, "08x")


def parse_iso_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(value[:10])
