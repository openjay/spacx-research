"""Readiness gates for V0 runtime — CLI and programmatic ``readiness()``."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from plugin.contracts import contract_probe_ok
from runtime.edgar_poll import BASELINES_PATH, REPO_ROOT, load_baseline_blockers, poll_edgar
from runtime.persistence import init_db, load_edgar_state

SCHEMAS_DIR = REPO_ROOT / "plugin" / "schemas"
CONTRACT_FLAG = REPO_ROOT / "runtime" / ".schema_contract_ok"
REQUIRED_SCHEMAS = (
    "EvidencePacket.json",
    "MetricSnapshot.json",
    "ThesisState.json",
    "RiskState.json",
    "ActionProposal.json",
    "AuditReceipt.json",
)


def check_schema_contract(*, write_flag: bool = True) -> bool:
    """Validate required JSON schemas exist and parse; optionally write flag file."""
    ok = True
    for name in REQUIRED_SCHEMAS:
        path = SCHEMAS_DIR / name
        if not path.is_file():
            ok = False
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            ok = False
    ok = ok and contract_probe_ok()
    if write_flag:
        CONTRACT_FLAG.parent.mkdir(parents=True, exist_ok=True)
        if ok:
            CONTRACT_FLAG.write_text(
                json.dumps({"ok": True, "schemas": list(REQUIRED_SCHEMAS), "probe": True}),
                encoding="utf-8",
            )
        elif CONTRACT_FLAG.is_file():
            CONTRACT_FLAG.unlink()
    return ok


def readiness(*, refresh_edgar: bool = False) -> dict[str, Any]:
    """
    Return readiness snapshot for Longter/OpenClaw consumption.

    Fields:
        sec_cache_ok: last EDGAR poll succeeded (or fresh poll when refresh_edgar)
        blocker_flags: FINAL_PROSPECTUS_PENDING, LOCKUP_DAY0_UNKNOWN, FIRST_EARNINGS_PENDING
        last_edgar_check: ISO timestamp from persisted state or live poll
        schema_contract_ok: plugin/schemas contract present and valid JSON
        ready: all gates green for observation worker (not trading)
    """
    init_db()
    schema_contract_ok = check_schema_contract(write_flag=False)

    edgar_state = load_edgar_state()
    sec_cache_ok = False
    last_edgar_check = None
    blocker_flags = load_baseline_blockers()

    if refresh_edgar:
        result = poll_edgar(persist=True)
        sec_cache_ok = result.get("sec_cache_ok", False)
        last_edgar_check = result.get("checked_at")
        blocker_flags = result.get("blocker_flags", blocker_flags)
    elif edgar_state:
        sec_cache_ok = True
        last_edgar_check = edgar_state.get("checked_at")
        blocker_flags = edgar_state.get("blocker_flags", blocker_flags)
    else:
        blocker_flags = load_baseline_blockers()
        if BASELINES_PATH.is_file():
            sec_cache_ok = True

    gates = {
        "sec_cache_ok": sec_cache_ok,
        "schema_contract_ok": schema_contract_ok,
        "blockers_clear": not any(blocker_flags.values()),
    }
    ready = gates["sec_cache_ok"] and gates["schema_contract_ok"]

    return {
        "version": "0.1.0",
        "asset": "SPCX",
        "compliance_level": 2,
        "sec_cache_ok": sec_cache_ok,
        "blocker_flags": blocker_flags,
        "last_edgar_check": last_edgar_check,
        "schema_contract_ok": schema_contract_ok,
        "gates": gates,
        "ready": ready,
        "observation_only": True,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="SPACX runtime readiness")
    parser.add_argument("--refresh-edgar", action="store_true", help="Run live EDGAR poll before check")
    parser.add_argument("--write-contract-flag", action="store_true", help="Refresh .schema_contract_ok")
    args = parser.parse_args()
    if args.write_contract_flag:
        check_schema_contract(write_flag=True)
    print(json.dumps(readiness(refresh_edgar=args.refresh_edgar), indent=2))


if __name__ == "__main__":
    main()
