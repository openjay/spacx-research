"""FWP ingest — mock event → EvidencePacket schema validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from runtime.fwp_ingest import (
    build_evidence_packet,
    ingest_fwp,
    load_manifest,
    sha256_bytes,
)
from tests.conftest import validate_instance

SAMPLE_HTML = b"""<html><body><h1>SpaceX Free Writing Prospectus</h1>
<p>Rule 433 offering communication. Not a final prospectus.</p></body></html>"""

MOCK_FILING = {
    "form": "FWP",
    "accession_number": "0001628280-26-040610",
    "filing_date": "2026-06-04",
    "primary_document": "spacexfwp.htm",
    "cik": "0001181412",
}


def test_sha256_bytes_deterministic() -> None:
    assert sha256_bytes(SAMPLE_HTML) == sha256_bytes(SAMPLE_HTML)
    assert len(sha256_bytes(SAMPLE_HTML)) == 64


def test_build_evidence_packet_validates_against_schema() -> None:
    content_hash = sha256_bytes(SAMPLE_HTML)
    packet = build_evidence_packet(
        MOCK_FILING,
        content_hash=content_hash,
        excerpt="SpaceX Free Writing Prospectus Rule 433",
        extracted_at="2026-06-05T12:00:00+00:00",
    )
    validate_instance(packet, "EvidencePacket.json")
    assert packet["confidence"] == "A"
    assert packet["source_id"] == MOCK_FILING["accession_number"]
    assert any(c["metric_id"] == "G_FWP_FILED" for c in packet["claims"])
    assert any(c["metric_id"] == "FINAL_PROSPECTUS_PENDING" for c in packet["claims"])
    assert packet.get("hash")
    assert "Rule 433" in " ".join(packet.get("tags", []))


def test_ingest_fwp_writes_cache_and_manifest(tmp_path: Path) -> None:
    cache_dir = tmp_path / "fwp"
    manifest_path = tmp_path / "manifest.json"

    result = ingest_fwp(
        MOCK_FILING,
        html_bytes=SAMPLE_HTML,
        persist=False,
        cache_dir=cache_dir,
        manifest_path=manifest_path,
    )

    assert result["ok"] is True
    assert result["sha256"] == sha256_bytes(SAMPLE_HTML)
    assert result["packet_id"] == f"fwp-{MOCK_FILING['accession_number']}"

    cache_file = cache_dir / "2026-06-04_0001628280-26-040610_spacexfwp.htm"
    assert cache_file.is_file()
    assert cache_file.read_bytes() == SAMPLE_HTML

    manifest = load_manifest(manifest_path=manifest_path)
    assert len(manifest["entries"]) == 1
    assert manifest["entries"][0]["sha256"] == result["sha256"]
    assert manifest["entries"][0]["packet_id"] == result["packet_id"]

    validate_instance(result["packet"], "EvidencePacket.json")


def test_ingest_fwp_rejects_non_fwp_form() -> None:
    with pytest.raises(ValueError, match="expected form FWP"):
        ingest_fwp({"form": "10-K", "accession_number": "x"}, html_bytes=SAMPLE_HTML, persist=False)


def test_ingest_fwp_idempotent_manifest_replace(tmp_path: Path) -> None:
    cache_dir = tmp_path / "fwp"
    manifest_path = tmp_path / "manifest.json"

    ingest_fwp(
        MOCK_FILING,
        html_bytes=SAMPLE_HTML,
        persist=False,
        cache_dir=cache_dir,
        manifest_path=manifest_path,
    )
    ingest_fwp(
        MOCK_FILING,
        html_bytes=SAMPLE_HTML + b" ",
        persist=False,
        cache_dir=cache_dir,
        manifest_path=manifest_path,
    )

    manifest = load_manifest(manifest_path=manifest_path)
    assert len(manifest["entries"]) == 1
    assert manifest["entries"][0]["bytes"] == len(SAMPLE_HTML) + 1
