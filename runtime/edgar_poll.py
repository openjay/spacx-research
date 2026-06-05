"""Poll SEC EDGAR CIK 0001181412 for new filings; emit events."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from runtime.fwp_ingest import ingest_fwp
from runtime.persistence import emit_runtime_event, load_edgar_state, save_edgar_state, save_audit_receipt

CIK = "0001181412"
CIK_INT = "1181412"
SUBMISSIONS_URL = f"https://data.sec.gov/submissions/CIK{CIK}.json"
WATCH_FORMS = frozenset({"424B4", "10-Q", "10-K", "S-1", "S-1/A", "FWP", "8-K"})
P0_FORM = "424B4"

REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINES_PATH = REPO_ROOT / "plugin" / "metrics" / "baselines.json"

DEFAULT_USER_AGENT = os.environ.get(
    "SPACX_SEC_USER_AGENT",
    "SPACX-Research openjay/spacx (contact: research@openjay.dev)",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fetch_submissions(*, user_agent: str | None = None) -> dict[str, Any]:
    ua = user_agent or DEFAULT_USER_AGENT
    req = urllib.request.Request(
        SUBMISSIONS_URL,
        headers={"User-Agent": ua, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _normalize_recent(submissions: dict[str, Any]) -> list[dict[str, Any]]:
    recent = submissions.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accessions = recent.get("accessionNumber", [])
    filing_dates = recent.get("filingDate", [])
    primary_docs = recent.get("primaryDocument", [])
    out: list[dict[str, Any]] = []
    for i, form in enumerate(forms):
        if form not in WATCH_FORMS:
            continue
        accession = accessions[i] if i < len(accessions) else None
        out.append(
            {
                "form": form,
                "accession_number": accession,
                "filing_date": filing_dates[i] if i < len(filing_dates) else None,
                "primary_document": primary_docs[i] if i < len(primary_docs) else None,
                "cik": CIK,
            }
        )
    return out


def load_baseline_blockers() -> dict[str, bool]:
    if not BASELINES_PATH.is_file():
        return {
            "FINAL_PROSPECTUS_PENDING": True,
            "LOCKUP_DAY0_UNKNOWN": True,
            "FIRST_EARNINGS_PENDING": True,
        }
    with BASELINES_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    return dict(data.get("blockers", {}))


def derive_blocker_flags(filings: list[dict[str, Any]], baseline: dict[str, bool] | None = None) -> dict[str, bool]:
    """Wire runtime blockers to plugin baselines + live EDGAR feed."""
    blockers = dict(baseline or load_baseline_blockers())
    forms_present = {f["form"] for f in filings}
    has_424b4 = P0_FORM in forms_present
    has_10q = "10-Q" in forms_present

    blockers["FINAL_PROSPECTUS_PENDING"] = not has_424b4
    if has_424b4:
        blockers["LOCKUP_DAY0_UNKNOWN"] = False
    blockers["FIRST_EARNINGS_PENDING"] = not has_10q
    return blockers


def poll_edgar(*, persist: bool = True, user_agent: str | None = None) -> dict[str, Any]:
    """
    Poll EDGAR submissions JSON; diff vs last seen; emit filing events.

    Returns event envelope suitable for agent adapters and health checks.
    """
    checked_at = _utc_now()
    prior = load_edgar_state() if persist else None
    prior_accessions = set(prior.get("seen_accessions", [])) if prior else set()

    try:
        raw = _fetch_submissions(user_agent=user_agent)
        sec_cache_ok = True
        error = None
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "cik": CIK,
            "checked_at": checked_at,
            "sec_cache_ok": False,
            "error": str(exc),
            "status_424b4": "unknown",
            "blocker_flags": load_baseline_blockers(),
            "new_filings": [],
            "events": [],
        }

    filings = _normalize_recent(raw)
    seen_accessions = [f["accession_number"] for f in filings if f.get("accession_number")]
    new_filings = [f for f in filings if f.get("accession_number") and f["accession_number"] not in prior_accessions]

    has_424b4 = any(f["form"] == P0_FORM for f in filings)
    status_424b4 = "filed" if has_424b4 else "pending"
    blocker_flags = derive_blocker_flags(filings)

    events: list[dict[str, Any]] = []
    for filing in new_filings:
        evt = {
            "event": "filing.detected",
            "cik": CIK,
            "form": filing["form"],
            "accession_number": filing["accession_number"],
            "filing_date": filing.get("filing_date"),
            "detected_at": checked_at,
        }
        events.append(evt)
        if persist:
            emit_runtime_event("filing.detected", evt)

    for filing in new_filings:
        if filing["form"] == P0_FORM:
            p0 = {
                "event": "filing.p0_424b4",
                "cik": CIK,
                "accession_number": filing["accession_number"],
                "filing_date": filing.get("filing_date"),
                "detected_at": checked_at,
                "human_gate": "p0_424b4_review",
            }
            events.append(p0)
            if persist:
                emit_runtime_event("filing.p0_424b4", p0)

    for filing in new_filings:
        if filing["form"] == "FWP":
            ingest_result = ingest_fwp(filing, user_agent=user_agent, persist=persist)
            fwp_evt = {
                "event": "filing.fwp_ingested",
                "cik": CIK,
                "form": filing["form"],
                "accession_number": filing["accession_number"],
                "filing_date": filing.get("filing_date"),
                "detected_at": checked_at,
                "ingest_ok": ingest_result.get("ok", False),
                "sha256": ingest_result.get("sha256"),
                "packet_id": ingest_result.get("packet_id"),
                "cache_path": ingest_result.get("cache_path"),
                "error": ingest_result.get("error"),
            }
            events.append(fwp_evt)
            if persist:
                emit_runtime_event("filing.fwp_ingested", fwp_evt)

    state = {
        "cik": CIK,
        "checked_at": checked_at,
        "seen_accessions": seen_accessions,
        "filings_recent": filings[:50],
        "status_424b4": status_424b4,
        "blocker_flags": blocker_flags,
        "company_name": raw.get("name"),
    }
    if persist:
        save_edgar_state(state)
        save_audit_receipt(
            "edgar_poll",
            {
                "checked_at": checked_at,
                "new_count": len(new_filings),
                "status_424b4": status_424b4,
                "blocker_flags": blocker_flags,
            },
            agent_id="SECFilingAgent",
        )

    if not has_424b4 and persist:
        emit_runtime_event(
            "filing.424b4_pending",
            {
                "event": "filing.424b4_pending",
                "cik": CIK,
                "status": "pending",
                "message": "No Form 424B4 in EDGAR recent feed",
                "checked_at": checked_at,
                "blocker_flags": blocker_flags,
            },
        )

    return {
        "cik": CIK,
        "checked_at": checked_at,
        "sec_cache_ok": sec_cache_ok,
        "error": error,
        "status_424b4": status_424b4,
        "blocker_flags": blocker_flags,
        "new_filings": new_filings,
        "events": events,
        "filings_count": len(filings),
    }


if __name__ == "__main__":
    print(json.dumps(poll_edgar(), indent=2))
