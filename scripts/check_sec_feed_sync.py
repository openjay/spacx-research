#!/usr/bin/env python3
"""SEC EDGAR feed vs docs/LISTING_STATUS.md sync gate.

Fetches recent filings for CIK 0001181412 from the SEC submissions JSON API,
compares watched forms against YAML frontmatter in ``docs/LISTING_STATUS.md``,
and fails when documentation is behind the live feed.

Watched forms: S-1, S-1/A, 424B4, FWP, 10-Q, 8-K.

Environment
-----------
SPACX_SEC_USER_AGENT
    Contact-bearing User-Agent string required by SEC EDGAR fair-access policy.
    Example: ``SPACX-Research openjay/spacx (contact: you@example.com)``

    **GitHub Actions:** set repository secret ``SPACX_SEC_USER_AGENT``. The
    ``sec-feed-sync`` CI job is skipped when that secret is unset (local forks and
    contributors without the secret still get green CI).

Exit codes
----------
0 — feed matches documented listing status (summary JSON on stdout)
1 — drift detected (summary JSON on stdout includes ``failures``)
2 — configuration or runtime error

Usage
-----
::

    # Local check (default User-Agent from SPACX_SEC_USER_AGENT or built-in)
    python scripts/check_sec_feed_sync.py

    # CI-style: exit 0 with skip summary when User-Agent env is empty
    python scripts/check_sec_feed_sync.py --require-user-agent

    # Custom listing status path
    python scripts/check_sec_feed_sync.py --listing-status docs/LISTING_STATUS.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

CIK = "0001181412"
SUBMISSIONS_URL = f"https://data.sec.gov/submissions/CIK{CIK}.json"
WATCH_FORMS = frozenset({"S-1", "S-1/A", "424B4", "FWP", "10-Q", "8-K"})
DEFAULT_USER_AGENT = "SPACX-Research openjay/spacx (contact: research@openjay.dev)"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LISTING_STATUS = REPO_ROOT / "docs" / "LISTING_STATUS.md"


@dataclass
class ListingStatusDoc:
    last_sec_check_date: date | None = None
    form_424b4_status: str = "pending"
    form_424b4_update_flag: bool = False
    latest_known_filings: list[dict[str, Any]] = field(default_factory=list)
    body_text: str = ""


def _parse_date(value: str | date | None) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def parse_listing_status(path: Path) -> ListingStatusDoc:
    text = path.read_text(encoding="utf-8")
    meta: dict[str, Any] = {}
    body = text

    if text.startswith("---"):
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if match:
            meta = yaml.safe_load(match.group(1)) or {}
            body = text[match.end() :]

    latest = meta.get("latest_known_filings") or meta.get("latest_filing") or []
    if isinstance(latest, dict):
        latest = [latest]

    return ListingStatusDoc(
        last_sec_check_date=_parse_date(meta.get("last_sec_check_date")),
        form_424b4_status=str(meta.get("form_424b4_status", "pending")).lower(),
        form_424b4_update_flag=bool(meta.get("form_424b4_update_flag", False)),
        latest_known_filings=list(latest),
        body_text=body,
    )


def fetch_submissions(*, user_agent: str) -> dict[str, Any]:
    req = urllib.request.Request(
        SUBMISSIONS_URL,
        headers={"User-Agent": user_agent, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalize_recent(submissions: dict[str, Any]) -> list[dict[str, Any]]:
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


def _known_accessions(doc: ListingStatusDoc) -> set[str]:
    known: set[str] = set()
    for row in doc.latest_known_filings:
        accession = row.get("accession_number")
        if accession:
            known.add(str(accession))
    return known


def _body_says_424b4_pending(body: str) -> bool:
    return bool(re.search(r"424B4.*\*\*Not filed\*\*", body, re.IGNORECASE | re.DOTALL))


def evaluate_sync(
    feed_filings: list[dict[str, Any]],
    doc: ListingStatusDoc,
) -> tuple[bool, list[dict[str, Any]]]:
    """Return (passed, failures)."""
    failures: list[dict[str, Any]] = []
    known = _known_accessions(doc)

    undocumented = [
        f
        for f in feed_filings
        if f.get("accession_number") and f["accession_number"] not in known
    ]
    if undocumented:
        failures.append(
            {
                "code": "undocumented_filings",
                "message": "EDGAR feed has watched filings not recorded in latest_known_filings",
                "filings": undocumented,
            }
        )

    if doc.last_sec_check_date:
        newer_than_check = [
            f
            for f in undocumented
            if f.get("filing_date")
            and _parse_date(f["filing_date"])
            and _parse_date(f["filing_date"]) > doc.last_sec_check_date
        ]
        if newer_than_check:
            failures.append(
                {
                    "code": "newer_than_last_sec_check_date",
                    "message": (
                        "Filing dates exceed last_sec_check_date "
                        f"({doc.last_sec_check_date.isoformat()})"
                    ),
                    "filings": newer_than_check,
                }
            )

    has_424b4 = any(f["form"] == "424B4" for f in feed_filings)
    pending_in_frontmatter = doc.form_424b4_status == "pending"
    pending_in_body = _body_says_424b4_pending(doc.body_text)
    if has_424b4 and pending_in_frontmatter and not doc.form_424b4_update_flag:
        failures.append(
            {
                "code": "424b4_filed_doc_pending",
                "message": (
                    "Form 424B4 appears on EDGAR feed but LISTING_STATUS still "
                    "documents 424B4 as pending without form_424b4_update_flag"
                ),
                "form_424b4_status": doc.form_424b4_status,
                "body_still_pending": pending_in_body,
            }
        )

    return (len(failures) == 0, failures)


def build_summary(
    *,
    status: str,
    failures: list[dict[str, Any]],
    feed_filings: list[dict[str, Any]] | None = None,
    doc: ListingStatusDoc | None = None,
    error: str | None = None,
    skipped: bool = False,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "status": status,
        "cik": CIK,
        "watched_forms": sorted(WATCH_FORMS),
        "failures": failures,
    }
    if skipped:
        summary["skipped"] = True
        summary["skip_reason"] = (
            "SPACX_SEC_USER_AGENT not set; "
            "configure repository secret SPACX_SEC_USER_AGENT to enable this gate"
        )
    if error:
        summary["error"] = error
    if feed_filings is not None:
        summary["feed_filings_count"] = len(feed_filings)
        summary["feed_filings"] = feed_filings[:20]
    if doc is not None:
        summary["documented"] = {
            "last_sec_check_date": (
                doc.last_sec_check_date.isoformat() if doc.last_sec_check_date else None
            ),
            "form_424b4_status": doc.form_424b4_status,
            "form_424b4_update_flag": doc.form_424b4_update_flag,
            "latest_known_filings_count": len(doc.latest_known_filings),
        }
    return summary


def run_check(
    *,
    listing_status_path: Path,
    user_agent: str | None,
    require_user_agent: bool,
) -> tuple[int, dict[str, Any]]:
    ua = (user_agent or os.environ.get("SPACX_SEC_USER_AGENT") or "").strip()
    if not ua:
        if require_user_agent:
            summary = build_summary(status="skipped", failures=[], skipped=True)
            return 0, summary
        ua = DEFAULT_USER_AGENT

    if not listing_status_path.is_file():
        summary = build_summary(
            status="error",
            failures=[],
            error=f"listing status file not found: {listing_status_path}",
        )
        return 2, summary

    doc = parse_listing_status(listing_status_path)

    try:
        raw = fetch_submissions(user_agent=ua)
        feed_filings = normalize_recent(raw)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        summary = build_summary(
            status="error",
            feed_filings=None,
            doc=doc,
            failures=[],
            error=str(exc),
        )
        return 2, summary

    passed, failures = evaluate_sync(feed_filings, doc)
    summary = build_summary(
        status="pass" if passed else "fail",
        feed_filings=feed_filings,
        doc=doc,
        failures=failures,
    )
    return (0 if passed else 1), summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare SEC EDGAR feed to docs/LISTING_STATUS.md frontmatter.",
    )
    parser.add_argument(
        "--listing-status",
        type=Path,
        default=DEFAULT_LISTING_STATUS,
        help=f"Path to LISTING_STATUS.md (default: {DEFAULT_LISTING_STATUS})",
    )
    parser.add_argument(
        "--require-user-agent",
        action="store_true",
        help="Exit 0 with skip summary when SPACX_SEC_USER_AGENT is unset (CI pattern).",
    )
    parser.add_argument(
        "--user-agent",
        default=None,
        help="Override User-Agent (else SPACX_SEC_USER_AGENT env or built-in default).",
    )
    args = parser.parse_args(argv)

    code, summary = run_check(
        listing_status_path=args.listing_status,
        user_agent=args.user_agent,
        require_user_agent=args.require_user_agent,
    )
    print(json.dumps(summary, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
