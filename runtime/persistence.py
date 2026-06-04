"""V0 persistence — SQLite store for evidence seals, audit receipts, metric snapshots."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RUNTIME_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = RUNTIME_DIR / "data" / "spacx_v0.db"
DEFAULT_JSONL_DIR = RUNTIME_DIR / "data" / "jsonl"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path | None = None) -> Path:
    """Create tables if missing; return resolved db path."""
    path = db_path or DEFAULT_DB_PATH
    with _connect(path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS evidence_seals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                packet_id TEXT NOT NULL,
                hash TEXT,
                payload_json TEXT NOT NULL,
                sealed_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_type TEXT NOT NULL,
                agent_id TEXT,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS metric_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset TEXT NOT NULL DEFAULT 'SPCX',
                snapshot_json TEXT NOT NULL,
                captured_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS edgar_state (
                key TEXT PRIMARY KEY,
                value_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS runtime_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                emitted_at TEXT NOT NULL
            );
            """
        )
        conn.commit()
    return path


def append_jsonl(record_type: str, payload: dict[str, Any], *, base_dir: Path | None = None) -> Path:
    """Mirror key records to JSONL for agent tailing (optional V0 path)."""
    base = base_dir or DEFAULT_JSONL_DIR
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{record_type}.jsonl"
    line = json.dumps({"record_type": record_type, "emitted_at": _utc_now(), **payload}, default=str)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return path


def save_evidence_seal(packet_id: str, payload: dict[str, Any], *, db_path: Path | None = None) -> int:
    init_db(db_path)
    with _connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO evidence_seals (packet_id, hash, payload_json, sealed_at) VALUES (?, ?, ?, ?)",
            (packet_id, payload.get("hash"), json.dumps(payload), _utc_now()),
        )
        conn.commit()
        row_id = int(cur.lastrowid)
    append_jsonl("evidence_seal", {"packet_id": packet_id, "row_id": row_id, **payload})
    return row_id


def save_audit_receipt(
    receipt_type: str,
    payload: dict[str, Any],
    *,
    agent_id: str | None = None,
    db_path: Path | None = None,
) -> int:
    init_db(db_path)
    with _connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO audit_receipts (receipt_type, agent_id, payload_json, created_at) VALUES (?, ?, ?, ?)",
            (receipt_type, agent_id, json.dumps(payload), _utc_now()),
        )
        conn.commit()
        row_id = int(cur.lastrowid)
    append_jsonl("audit_receipt", {"receipt_type": receipt_type, "agent_id": agent_id, "row_id": row_id, **payload})
    return row_id


def save_metric_snapshot(snapshot: dict[str, Any], *, asset: str = "SPCX", db_path: Path | None = None) -> int:
    init_db(db_path)
    with _connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO metric_snapshots (asset, snapshot_json, captured_at) VALUES (?, ?, ?)",
            (asset, json.dumps(snapshot), _utc_now()),
        )
        conn.commit()
        row_id = int(cur.lastrowid)
    append_jsonl("metric_snapshot", {"asset": asset, "row_id": row_id, **snapshot})
    return row_id


def save_edgar_state(state: dict[str, Any], *, db_path: Path | None = None) -> None:
    init_db(db_path)
    with _connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO edgar_state (key, value_json, updated_at) VALUES ('last', ?, ?)
            ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at
            """,
            (json.dumps(state), _utc_now()),
        )
        conn.commit()


def load_edgar_state(*, db_path: Path | None = None) -> dict[str, Any] | None:
    init_db(db_path)
    with _connect(db_path) as conn:
        row = conn.execute("SELECT value_json FROM edgar_state WHERE key = 'last'").fetchone()
    if not row:
        return None
    return json.loads(row["value_json"])


def emit_runtime_event(event_type: str, payload: dict[str, Any], *, db_path: Path | None = None) -> int:
    init_db(db_path)
    with _connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO runtime_events (event_type, payload_json, emitted_at) VALUES (?, ?, ?)",
            (event_type, json.dumps(payload), _utc_now()),
        )
        conn.commit()
        row_id = int(cur.lastrowid)
    append_jsonl("runtime_event", {"event_type": event_type, "row_id": row_id, **payload})
    return row_id


def recent_events(limit: int = 20, *, db_path: Path | None = None) -> list[dict[str, Any]]:
    init_db(db_path)
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT event_type, payload_json, emitted_at FROM runtime_events ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {"event_type": r["event_type"], "emitted_at": r["emitted_at"], **json.loads(r["payload_json"])}
        for r in rows
    ]
