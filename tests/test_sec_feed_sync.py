"""Unit tests for SEC feed vs LISTING_STATUS sync gate (no network)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from scripts.check_sec_feed_sync import (
    ListingStatusDoc,
    _body_says_424b4_pending,
    evaluate_sync,
    normalize_recent,
    parse_listing_status,
    run_check,
)

FIXTURE_SUBMISSIONS = {
    "filings": {
        "recent": {
            "form": ["FWP", "S-1/A", "424B4", "D", "8-K"],
            "accessionNumber": [
                "0001628280-26-040874",
                "0001628280-26-040364",
                "0001628280-26-099999",
                "0001181412-22-000003",
                "0001628280-26-041111",
            ],
            "filingDate": [
                "2026-06-04",
                "2026-06-03",
                "2026-06-05",
                "2022-08-05",
                "2026-06-05",
            ],
            "primaryDocument": [
                "spacexukfwp.htm",
                "spaceexplorationtechnologib.htm",
                "spacex424b4.htm",
                "primary_doc.xml",
                "spacex8k.htm",
            ],
        }
    }
}

SYNCED_FRONTMATTER = """---
last_sec_check_date: "2026-06-04"
form_424b4_status: pending
latest_known_filings:
  - form: FWP
    filing_date: "2026-06-04"
    accession_number: "0001628280-26-040874"
  - form: FWP
    filing_date: "2026-06-04"
    accession_number: "0001628280-26-040610"
  - form: S-1/A
    filing_date: "2026-06-03"
    accession_number: "0001628280-26-040364"
---

# SPCX listing status

| **Form 424B4 (final prospectus)** | **Not filed** |
"""

STALE_FRONTMATTER = """---
last_sec_check_date: "2026-06-03"
form_424b4_status: pending
latest_known_filings:
  - form: S-1/A
    filing_date: "2026-06-03"
    accession_number: "0001628280-26-040364"
---

# SPCX listing status

| **Form 424B4 (final prospectus)** | **Not filed** |
"""

FILING_424B4_FRONTMATTER = """---
last_sec_check_date: "2026-06-04"
form_424b4_status: pending
latest_known_filings:
  - form: FWP
    filing_date: "2026-06-04"
    accession_number: "0001628280-26-040874"
---

# SPCX listing status

| **Form 424B4 (final prospectus)** | **Not filed** |
"""


def _write_listing(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "LISTING_STATUS.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_normalize_recent_filters_watched_forms() -> None:
    rows = normalize_recent(FIXTURE_SUBMISSIONS)
    forms = [row["form"] for row in rows]
    assert forms == ["FWP", "S-1/A", "424B4", "8-K"]


def test_parse_listing_status_reads_frontmatter(tmp_path: Path) -> None:
    path = _write_listing(tmp_path, SYNCED_FRONTMATTER)
    doc = parse_listing_status(path)
    assert doc.last_sec_check_date == date(2026, 6, 4)
    assert doc.form_424b4_status == "pending"
    assert len(doc.latest_known_filings) == 3
    assert _body_says_424b4_pending(doc.body_text)


def test_evaluate_sync_passes_when_feed_matches_doc(tmp_path: Path) -> None:
    feed = normalize_recent(FIXTURE_SUBMISSIONS)[:2]
    doc = parse_listing_status(_write_listing(tmp_path, SYNCED_FRONTMATTER))
    passed, failures = evaluate_sync(feed, doc)
    assert passed is True
    assert failures == []


def test_evaluate_sync_fails_on_undocumented_filings(tmp_path: Path) -> None:
    feed = normalize_recent(FIXTURE_SUBMISSIONS)
    doc = parse_listing_status(_write_listing(tmp_path, STALE_FRONTMATTER))
    passed, failures = evaluate_sync(feed, doc)
    assert passed is False
    codes = {f["code"] for f in failures}
    assert "undocumented_filings" in codes
    assert "newer_than_last_sec_check_date" in codes


def test_evaluate_sync_fails_when_424b4_on_feed_but_doc_pending(tmp_path: Path) -> None:
    feed = [f for f in normalize_recent(FIXTURE_SUBMISSIONS) if f["form"] == "424B4"]
    doc = parse_listing_status(_write_listing(tmp_path, FILING_424B4_FRONTMATTER))
    passed, failures = evaluate_sync(feed, doc)
    assert passed is False
    assert any(f["code"] == "424b4_filed_doc_pending" for f in failures)


def test_evaluate_sync_passes_424b4_when_update_flag_set(tmp_path: Path) -> None:
    text = """---
last_sec_check_date: "2026-06-05"
form_424b4_status: pending
form_424b4_update_flag: true
latest_known_filings:
  - form: 424B4
    filing_date: "2026-06-05"
    accession_number: "0001628280-26-099999"
---

# SPCX listing status

| **Form 424B4 (final prospectus)** | **Not filed** |
"""
    feed = [f for f in normalize_recent(FIXTURE_SUBMISSIONS) if f["form"] == "424B4"]
    doc = parse_listing_status(_write_listing(tmp_path, text))
    passed, failures = evaluate_sync(feed, doc)
    assert passed is True
    assert failures == []


def test_run_check_skips_without_user_agent_when_required(tmp_path: Path) -> None:
    listing = _write_listing(tmp_path, SYNCED_FRONTMATTER)
    code, summary = run_check(
        listing_status_path=listing,
        user_agent="",
        require_user_agent=True,
    )
    assert code == 0
    assert summary["status"] == "skipped"
    assert summary["skipped"] is True


def test_repo_listing_status_parses() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "docs" / "LISTING_STATUS.md"
    doc = parse_listing_status(path)
    assert doc.last_sec_check_date is not None
    assert len(doc.latest_known_filings) >= 2
