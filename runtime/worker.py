"""SPACX V0 worker — poll scheduler tiers; dispatch stubs for eight agents."""

from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from runtime.edgar_poll import poll_edgar
from runtime.health import readiness
from runtime.packets import RiskAlertPacket, nap_from_blockers
from runtime.persistence import emit_runtime_event, save_metric_snapshot
from runtime.persistence import init_db

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEDULER_PATH = REPO_ROOT / "plugin" / "scheduler.yaml"

logger = logging.getLogger("spacx.runtime.worker")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_scheduler(path: Path | None = None) -> dict[str, Any]:
    path = path or SCHEDULER_PATH
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_tier(tier_id: str, tier: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    """Execute one scheduler tier (V0 stubs + live EDGAR on sec_1h)."""
    agents = tier.get("agents", [])
    started = _utc_now()
    result: dict[str, Any] = {
        "tier_id": tier_id,
        "started_at": started,
        "agents": agents,
        "status": "ok",
        "outputs": [],
    }

    if tier_id == "sec_1h":
        edgar = poll_edgar(persist=not dry_run)
        result["outputs"].append({"kind": "edgar_poll", "summary": edgar})
        if not dry_run and edgar.get("blocker_flags"):
            nap = nap_from_blockers(edgar["blocker_flags"])
            emit_runtime_event("packet.next_action", nap.to_dict())
            risk = RiskAlertPacket(
                overall_status="AMBER" if any(edgar["blocker_flags"].values()) else "GREEN",
                flags=[k for k, v in edgar["blocker_flags"].items() if v],
                reason=f"424B4 status: {edgar.get('status_424b4')}",
            )
            emit_runtime_event("packet.risk_alert", risk.to_dict())
    elif tier_id == "thesis_daily":
        result["outputs"].append(
            {
                "kind": "thesis_stub",
                "message": "Daily thesis draft requires human gate thesis_publish",
                "output": tier.get("output"),
            }
        )
    else:
        result["outputs"].append(
            {"kind": "tier_stub", "message": f"V0 no-op dispatch for {tier_id}", "cron": tier.get("cron") or tier.get("cron_default")}
        )

    if not dry_run:
        save_metric_snapshot(
            {
                "tier_id": tier_id,
                "as_of": started,
                "agents": agents,
                "readiness": readiness(refresh_edgar=False),
            }
        )

    result["finished_at"] = _utc_now()
    return result


def run_once(*, dry_run: bool = False, tiers: list[str] | None = None) -> dict[str, Any]:
    """Single worker pass: run selected tiers (default: sec_1h + evidence_6h stubs)."""
    init_db()
    sched = load_scheduler()
    all_tiers: dict[str, Any] = sched.get("tiers", {})
    default_order = ["sec_1h", "crypto_1_5m", "market_15m", "evidence_6h", "space_4h", "float_daily"]
    order = tiers or default_order

    run_log: list[dict[str, Any]] = []
    for tier_id in order:
        tier = all_tiers.get(tier_id)
        if not tier:
            logger.warning("Unknown tier %s — skip", tier_id)
            continue
        logger.info("Running tier %s (%s)", tier_id, tier.get("description", ""))
        run_log.append(run_tier(tier_id, tier, dry_run=dry_run))

    snap = readiness(refresh_edgar=False)
    envelope = {
        "worker": "spacx-runtime-v0",
        "mode": "once",
        "dry_run": dry_run,
        "started_at": run_log[0]["started_at"] if run_log else _utc_now(),
        "finished_at": _utc_now(),
        "tiers_run": [r["tier_id"] for r in run_log],
        "readiness": snap,
        "tier_results": run_log,
    }
    if not dry_run:
        emit_runtime_event("worker.pass_complete", envelope)
    return envelope


def run_loop(interval_seconds: int = 300) -> None:
    """Continuous loop — minimum floor interval between passes (V0)."""
    logger.info("Starting worker loop (interval=%ss)", interval_seconds)
    while True:
        try:
            run_once()
        except Exception:
            logger.exception("Worker pass failed")
        time.sleep(interval_seconds)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="SPACX V0 runtime worker")
    parser.add_argument("--once", action="store_true", help="Run one scheduler pass and exit")
    parser.add_argument("--dry-run", action="store_true", help="Do not persist events or snapshots")
    parser.add_argument("--tiers", nargs="*", help="Subset of tier ids (default: sec + stubs)")
    parser.add_argument("--loop", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=int, default=300, help="Loop sleep seconds")
    parser.add_argument("--json", action="store_true", help="Print pass envelope as JSON")
    args = parser.parse_args()

    if args.loop:
        run_loop(args.interval)
        return

    if not args.once:
        parser.error("V0 requires --once or --loop")
    envelope = run_once(dry_run=args.dry_run, tiers=args.tiers)
    if args.json:
        print(json.dumps(envelope, indent=2))
    else:
        print(json.dumps({"tiers_run": envelope["tiers_run"], "readiness": envelope["readiness"]}, indent=2))


if __name__ == "__main__":
    main()
