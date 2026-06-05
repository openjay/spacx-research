"""Ingest SEC Form FWP filings into source cache and EvidencePacket JSON."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from plugin.rwa.evidence_hash import apply_seal_to_evidence_packet
from runtime.persistence import save_audit_receipt, save_evidence_seal

CIK = "0001181412"
CIK_INT = "1181412"
FWP_FORM = "FWP"
MAX_EXCERPT_CHARS = 4000

REPO_ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = REPO_ROOT / "workstreams" / "sec-evidence-phase1" / "cache"
FWP_CACHE_DIR = CACHE_ROOT / "fwp"
MANIFEST_PATH = CACHE_ROOT / "manifest.json"

RULE_433_DISCLAIMER = (
    "Free writing prospectus filed under SEC Rule 433. "
    "Not a final prospectus; not a substitute for Form 424B4. "
    "Excerpts only — no full reproduction in EvidencePacket."
)

DEFAULT_USER_AGENT = __import__("os").environ.get(
    "SPACX_SEC_USER_AGENT",
    "SPACX-Research openjay/spacx (contact: research@openjay.dev)",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def edgar_document_url(
    *,
    accession_number: str,
    primary_document: str,
    cik_int: str = CIK_INT,
) -> str:
    accession_path = accession_number.replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_path}/{primary_document}"


def _dated_cache_filename(filing: dict[str, Any]) -> str:
    filing_date = filing.get("filing_date") or "unknown-date"
    accession = filing.get("accession_number") or "unknown-accession"
    primary = filing.get("primary_document") or "document.htm"
    safe_primary = re.sub(r"[^\w.\-]", "_", primary)
    return f"{filing_date}_{accession}_{safe_primary}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _strip_html_excerpt(html: str, *, max_chars: int = MAX_EXCERPT_CHARS) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def load_manifest(*, manifest_path: Path | None = None) -> dict[str, Any]:
    path = manifest_path or MANIFEST_PATH
    if not path.is_file():
        return {"version": 1, "entries": []}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: dict[str, Any], *, manifest_path: Path | None = None) -> Path:
    path = manifest_path or MANIFEST_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    return path


def download_fwp_html(
    filing: dict[str, Any],
    *,
    user_agent: str | None = None,
    timeout: float = 30,
) -> bytes:
    primary = filing.get("primary_document")
    accession = filing.get("accession_number")
    if not primary or not accession:
        raise ValueError("FWP filing requires accession_number and primary_document")

    url = edgar_document_url(accession_number=accession, primary_document=primary)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": user_agent or DEFAULT_USER_AGENT, "Accept": "text/html,*/*"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def build_evidence_packet(
    filing: dict[str, Any],
    *,
    content_hash: str,
    excerpt: str | None = None,
    extracted_at: str | None = None,
) -> dict[str, Any]:
    accession = filing["accession_number"]
    filing_date = filing.get("filing_date") or "unknown"
    packet_id = f"fwp-{accession}"

    claims: list[dict[str, Any]] = [
        {
            "claim": "SEC Form FWP filed on EDGAR (Rule 433 offering communication)",
            "metric_id": "G_FWP_FILED",
            "value": 1,
            "unit": "filing",
            "period": filing_date,
            "citation": accession,
            "assertion": "occurrence",
        },
        {
            "claim": "Form 424B4 final prospectus still pending",
            "metric_id": "FINAL_PROSPECTUS_PENDING",
            "value": 1,
            "unit": "flag",
            "period": filing_date,
            "citation": accession,
            "assertion": "classification",
        },
    ]

    if excerpt:
        claims[0]["citation"] = f"{accession} | excerpt: {excerpt[:500]}"

    packet: dict[str, Any] = {
        "packet_id": packet_id,
        "source_id": accession,
        "source_type": "sec_edgar_fwp",
        "confidence": "A",
        "extracted_at": extracted_at or _utc_now(),
        "claims": claims,
        "tags": [
            "FWP",
            "Rule433",
            "offering_communication",
            "not_final_prospectus",
            RULE_433_DISCLAIMER,
            f"form:{FWP_FORM}",
            f"filed_at:{filing_date}",
            f"source_sha256:{content_hash}",
        ],
        "conflict_flags": [],
    }

    return apply_seal_to_evidence_packet(packet)


def ingest_fwp(
    filing: dict[str, Any],
    *,
    html_bytes: bytes | None = None,
    user_agent: str | None = None,
    persist: bool = True,
    cache_dir: Path | None = None,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    """
    Download FWP HTML, cache with SHA-256, emit sealed EvidencePacket.

    Returns ingest result with paths, hash, and packet body.
    """
    if filing.get("form") != FWP_FORM:
        raise ValueError(f"expected form {FWP_FORM}, got {filing.get('form')}")

    accession = filing.get("accession_number")
    if not accession:
        raise ValueError("FWP filing missing accession_number")

    ingested_at = _utc_now()
    cache_root = cache_dir or FWP_CACHE_DIR
    cache_root.mkdir(parents=True, exist_ok=True)

    if html_bytes is None:
        try:
            html_bytes = download_fwp_html(filing, user_agent=user_agent)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            return {
                "ok": False,
                "accession_number": accession,
                "error": str(exc),
                "ingested_at": ingested_at,
            }

    content_hash = sha256_bytes(html_bytes)
    cache_name = _dated_cache_filename(filing)
    cache_path = cache_root / cache_name
    cache_path.write_bytes(html_bytes)

    excerpt = _strip_html_excerpt(html_bytes.decode("utf-8", errors="replace"))
    packet = build_evidence_packet(filing, content_hash=content_hash, excerpt=excerpt, extracted_at=ingested_at)

    rel_cache_path = str(cache_path.relative_to(REPO_ROOT)) if cache_path.is_relative_to(REPO_ROOT) else str(cache_path)

    manifest = load_manifest(manifest_path=manifest_path)
    entries = [e for e in manifest.get("entries", []) if e.get("accession_number") != accession]
    entry = {
        "accession_number": accession,
        "form": FWP_FORM,
        "filing_date": filing.get("filing_date"),
        "primary_document": filing.get("primary_document"),
        "cik": filing.get("cik", CIK),
        "cache_path": rel_cache_path,
        "sha256": content_hash,
        "bytes": len(html_bytes),
        "ingested_at": ingested_at,
        "packet_id": packet["packet_id"],
        "evidence_hash": packet.get("hash"),
    }
    entries.append(entry)
    manifest["entries"] = entries
    save_manifest(manifest, manifest_path=manifest_path)

    if persist:
        save_evidence_seal(packet["packet_id"], packet)
        save_audit_receipt(
            "fwp_ingest",
            {
                "accession_number": accession,
                "cache_path": rel_cache_path,
                "sha256": content_hash,
                "packet_id": packet["packet_id"],
                "ingested_at": ingested_at,
            },
            agent_id="SECFilingAgent",
        )

    return {
        "ok": True,
        "accession_number": accession,
        "cache_path": rel_cache_path,
        "sha256": content_hash,
        "bytes": len(html_bytes),
        "packet": packet,
        "packet_id": packet["packet_id"],
        "ingested_at": ingested_at,
        "event_id": str(uuid4()),
    }
