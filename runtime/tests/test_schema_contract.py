"""Schema contract gate — used by runtime.health.schema_contract_ok."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
