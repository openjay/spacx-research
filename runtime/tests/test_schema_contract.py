"""Schema contract gate — used by runtime.health.schema_contract_ok."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from runtime.edgar_poll import _normalize_recent

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = REPO_ROOT / "plugin" / "schemas"

REQUIRED = (
    "EvidencePacket.json",
    "MetricSnapshot.json",
    "ThesisState.json",
    "RiskState.json",
    "ActionProposal.json",
    "AuditReceipt.json",
)


class TestSchemaContract(unittest.TestCase):
    def test_required_schemas_exist_and_parse(self) -> None:
        for name in REQUIRED:
            path = SCHEMAS_DIR / name
            self.assertTrue(path.is_file(), f"missing schema: {name}")
            json.loads(path.read_text(encoding="utf-8"))

    def test_edgar_recent_normalizes_fwp_without_clearing_424b4_gate(self) -> None:
        submissions = {
            "filings": {
                "recent": {
                    "form": ["FWP", "S-1/A", "D"],
                    "accessionNumber": [
                        "0001628280-26-040610",
                        "0001628280-26-040364",
                        "0001181412-22-000003",
                    ],
                    "filingDate": ["2026-06-04", "2026-06-03", "2022-08-05"],
                    "primaryDocument": [
                        "spacexfwp.htm",
                        "spaceexplorationtechnologib.htm",
                        "primary_doc.xml",
                    ],
                }
            }
        }

        forms = [row["form"] for row in _normalize_recent(submissions)]

        self.assertEqual(forms, ["FWP", "S-1/A"])


if __name__ == "__main__":
    unittest.main()
