"""SPACX Intelligence Plugin — Python API stubs (V0).

Maps to REST routes in ``plugin/manifest.yaml``. Implementations are no-op or
pass-through stubs until Phase 2 services are wired.
"""

from . import alerts, evidence, ingest, metrics, risk, thesis

__all__ = [
    "alerts",
    "evidence",
    "ingest",
    "metrics",
    "risk",
    "thesis",
]
