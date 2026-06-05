"""Repository terminology guardrails for bilingual financial docs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = ("README.md", "docs", "workstreams", "plugin", "runtime")
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py"}
ALLOWLIST = {
    Path("docs/TERMINOLOGY.md"),
    Path("tests/test_terminology.py"),
}

FORBIDDEN_TERMS = {
    "绿鞋": "Use 超额配售选择权（greenshoe）.",
    "绿靴": "Use 超额配售选择权（greenshoe）.",
    "绿鞋股": "Use 超额配售选择权（greenshoe）对应股份.",
}


def _iter_text_files() -> list[Path]:
    paths: list[Path] = []
    for item in SCAN_DIRS:
        path = ROOT / item
        if path.is_file():
            if path.relative_to(ROOT) not in ALLOWLIST:
                paths.append(path)
            continue
        for child in path.rglob("*"):
            rel = child.relative_to(ROOT)
            if child.is_file() and child.suffix in TEXT_SUFFIXES and rel not in ALLOWLIST:
                paths.append(child)
    return paths


def test_forbidden_literal_finance_translations_absent() -> None:
    failures: list[str] = []
    for path in _iter_text_files():
        text = path.read_text(encoding="utf-8")
        for term, replacement in FORBIDDEN_TERMS.items():
            if term in text:
                rel = path.relative_to(ROOT)
                failures.append(f"{rel}: contains {term!r}; {replacement}")

    assert failures == []
