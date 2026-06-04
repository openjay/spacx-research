"""Ingest API — ``POST /ingest/source``, ``POST /extract/events``.

V0 stubs return structured dicts matching JSON schemas; persistence is out of scope.
"""

from __future__ import annotations

from typing import Any


def ingest_source(source: dict[str, Any]) -> dict[str, Any]:
    """POST /api/v1/spacx/ingest/source

    Register a raw or normalized :class:`SourceRecord` for downstream extraction.

    Args:
        source: SourceRecord fields (source_id, source_type, uri, ingested_at, ...).

    Returns:
        dict with keys ``source_id``, ``status`` (``accepted`` | ``duplicate`` | ``rejected``),
        and optional ``receipt_id`` for AuditReceipt linkage.
    """
    source_id = source.get("source_id", "")
    return {
        "source_id": source_id,
        "status": "accepted" if source_id else "rejected",
        "receipt_id": None,
    }


def extract_events(
    source_id: str,
    *,
    event_types: list[str] | None = None,
) -> dict[str, Any]:
    """POST /api/v1/spacx/extract/events

    Parse an ingested source into structured market/SEC events for agents.

    Args:
        source_id: Stable id from :func:`ingest_source`.
        event_types: Optional filter, e.g. ``SEC_FILING_NEW``, ``METRIC_DELTA``.

    Returns:
        dict with ``source_id``, ``events`` (list of event objects), and ``extracted_at``.
    """
    return {
        "source_id": source_id,
        "events": [],
        "event_types_filter": event_types or [],
        "extracted_at": None,
    }
