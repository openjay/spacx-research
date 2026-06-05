"""Export valuation anchors as MetricSnapshot-compliant objects."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from plugin.api._time import utc_now_iso
from plugin.contracts import validate_against_schema
from plugin.metrics.threshold_engine import _iter_metric_defs, evaluate_metric, load_registry
from plugin.valuation.implied_multiples import (
    compute_implied_multiples,
    valuation_metrics_at_price,
)
from plugin.valuation.sec_fy25 import (
    FY25_ADJ_EBITDA_MUSD,
    FY25_REVENUE_MUSD,
    IPO_PRICE_USD,
    sec_balance_sheet,
)

_VALUATION_DIR = Path(__file__).resolve().parent
_ANCHORS_PATH = _VALUATION_DIR / "price_anchors.yaml"
_BANDS_PATH = _VALUATION_DIR / "scenario_bands.yaml"
_COMPUTED_BY = "valuation_export_v1"

_METRIC_UNITS: dict[str, str] = {
    "IMPLIED_MARKET_CAP_USD": "USD",
    "EV_TO_REVENUE_FY25": "ratio",
    "EV_TO_ADJ_EBITDA_FY25": "ratio",
    "PRICE_VS_DCF_ANCHOR_PCT": "percent",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _metric_def_by_id(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {m["metric_id"]: m for m in _iter_metric_defs(registry)}


def _snapshot_status(
    metric_id: str,
    value: float,
    *,
    registry: dict[str, Any],
) -> str:
    metric_defs = _metric_def_by_id(registry)
    metric_def = metric_defs.get(metric_id)
    if not metric_def:
        return "UNKNOWN"
    result = evaluate_metric(metric_def, {metric_id: value})
    return result.status.value


def _build_snapshot(
    metric_id: str,
    value: float,
    *,
    period: str,
    price_ctx: float,
    as_of: str,
    registry: dict[str, Any],
) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "asset": "SPCX",
        "value": value,
        "unit": _METRIC_UNITS[metric_id],
        "period": period,
        "as_of": as_of,
        "status": _snapshot_status(metric_id, value, registry=registry),
        "evidence_refs": [
            "plugin/valuation/price_anchors.yaml",
            "plugin/valuation/scenario_bands.yaml",
            "plugin/valuation/sec_fy25.py",
            f"price_context:{price_ctx}",
        ],
        "computed_by": _COMPUTED_BY,
    }


def _anchor_metadata(anchors_data: dict[str, Any]) -> dict[str, Any]:
    anchors = anchors_data.get("anchors", {})
    meta: dict[str, Any] = {}
    for key, anchor in anchors.items():
        tier = anchor.get("cfa_tier", anchor.get("evidence_grade", "UNKNOWN"))
        entry: dict[str, Any] = {
            "label": anchor.get("label", key),
            "cfa_tier": tier,
            "as_of": anchor.get("as_of"),
        }
        if "price_usd_per_share" in anchor:
            entry["price_usd"] = anchor["price_usd_per_share"]
        if "price_usd_per_share_low" in anchor:
            entry["price_usd_low"] = anchor["price_usd_per_share_low"]
            entry["price_usd_high"] = anchor["price_usd_per_share_high"]
        meta[key] = entry
    return meta


def build_export_payload(*, as_of: str | None = None) -> dict[str, Any]:
    """Build valuation MetricSnapshot export envelope."""
    anchors_data = _load_yaml(_ANCHORS_PATH)
    bands_data = _load_yaml(_BANDS_PATH)
    registry = load_registry()
    exported_at = as_of or utc_now_iso()

    dcf_anchor = anchors_data["anchors"]["dcf_conservative_anchor"]
    dcf_price = float(dcf_anchor["price_usd_per_share"])
    ipo_price = float(anchors_data["anchors"]["ipo_issue_anchor"]["price_usd_per_share"])

    metrics_135 = valuation_metrics_at_price(ipo_price)
    multiples_60 = compute_implied_multiples(dcf_price)

    snapshots: list[dict[str, Any]] = [
        _build_snapshot(
            "IMPLIED_MARKET_CAP_USD",
            metrics_135["IMPLIED_MARKET_CAP_USD"],
            period="IPO_issue_anchor_135",
            price_ctx=ipo_price,
            as_of=exported_at,
            registry=registry,
        ),
        _build_snapshot(
            "EV_TO_REVENUE_FY25",
            metrics_135["EV_TO_REVENUE_FY25"],
            period="IPO_issue_anchor_135",
            price_ctx=ipo_price,
            as_of=exported_at,
            registry=registry,
        ),
        _build_snapshot(
            "EV_TO_ADJ_EBITDA_FY25",
            metrics_135["EV_TO_ADJ_EBITDA_FY25"],
            period="IPO_issue_anchor_135",
            price_ctx=ipo_price,
            as_of=exported_at,
            registry=registry,
        ),
        _build_snapshot(
            "EV_TO_REVENUE_FY25",
            multiples_60["ev_to_revenue_fy25"],
            period="DCF_conservative_anchor_60",
            price_ctx=dcf_price,
            as_of=exported_at,
            registry=registry,
        ),
        _build_snapshot(
            "EV_TO_ADJ_EBITDA_FY25",
            multiples_60["ev_to_adj_ebitda_fy25"],
            period="DCF_conservative_anchor_60",
            price_ctx=dcf_price,
            as_of=exported_at,
            registry=registry,
        ),
        _build_snapshot(
            "PRICE_VS_DCF_ANCHOR_PCT",
            metrics_135["PRICE_VS_DCF_ANCHOR_PCT"],
            period="IPO_issue_anchor_135",
            price_ctx=ipo_price,
            as_of=exported_at,
            registry=registry,
        ),
    ]

    bs = sec_balance_sheet()
    return {
        "exported_at": exported_at,
        "computed_by": _COMPUTED_BY,
        "anchors": _anchor_metadata(anchors_data),
        "scenario_bands": bands_data.get("scenarios", {}),
        "sec_fy25": {
            "consolidated_revenue_musd": FY25_REVENUE_MUSD["consolidated"],
            "consolidated_adj_ebitda_musd": FY25_ADJ_EBITDA_MUSD["consolidated"],
            "ipo_price_usd": IPO_PRICE_USD,
            "shares_outstanding": bs["shares_outstanding"],
            "evidence_grade": bs["evidence_grade"],
            "sec_citation": bs["sec_citation"],
        },
        "snapshots": snapshots,
    }


def validate_export(payload: dict[str, Any]) -> None:
    """Validate each snapshot against MetricSnapshot.json."""
    for snapshot in payload["snapshots"]:
        validate_against_schema(snapshot, "MetricSnapshot.json")


def export_snapshots(out_path: Path, *, as_of: str | None = None) -> dict[str, Any]:
    """Build, validate, and write valuation metric snapshots."""
    payload = build_export_payload(as_of=as_of)
    validate_export(payload)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    return payload


def snapshot_ref(metric_id: str, price_ctx: float | str) -> str:
    """Stable reference id for NAP/ThesisUpdate packets."""
    if isinstance(price_ctx, float) and price_ctx.is_integer():
        price_ctx = int(price_ctx)
    return f"metric_snapshot:{metric_id}@{price_ctx}"


def valuation_snapshot_refs(*, ipo_price: float = 135.0, dcf_price: float = 60.0) -> list[str]:
    """Default valuation snapshot refs for adapter packets."""
    return [
        snapshot_ref("IMPLIED_MARKET_CAP_USD", ipo_price),
        snapshot_ref("EV_TO_REVENUE_FY25", ipo_price),
        snapshot_ref("EV_TO_ADJ_EBITDA_FY25", ipo_price),
        snapshot_ref("EV_TO_REVENUE_FY25", dcf_price),
        snapshot_ref("EV_TO_ADJ_EBITDA_FY25", dcf_price),
        snapshot_ref("PRICE_VS_DCF_ANCHOR_PCT", ipo_price),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export valuation MetricSnapshots")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runtime/data/metric_snapshots.json"),
        help="Output JSON path (default: runtime/data/metric_snapshots.json)",
    )
    args = parser.parse_args(argv)
    export_snapshots(args.out)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
