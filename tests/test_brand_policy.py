"""Brand and affiliation disclaimer guardrails."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

FULL_DISCLAIMER = (
    "Not affiliated with Space Exploration Technologies Corp. (SpaceX), xAI, "
    "Anthropic, Nasdaq, Goldman Sachs, Morningstar, or the SEC."
)


def test_root_and_manifest_use_full_non_affiliation_disclaimer() -> None:
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    manifest = (ROOT / "plugin" / "manifest.yaml").read_text(encoding="utf-8")

    manifest_flat = re.sub(r"\s+", " ", manifest)

    assert FULL_DISCLAIMER in root_readme
    assert FULL_DISCLAIMER in manifest_flat
    assert "Not investment advice" in manifest
    for name in (
        "Space Exploration Technologies Corp. (SpaceX)",
        "xAI",
        "Anthropic",
        "Nasdaq",
        "Goldman Sachs",
        "Morningstar",
        "SEC",
    ):
        assert name in manifest_flat


def test_agent_readmes_use_full_brand_footer() -> None:
    agent_readmes = sorted((ROOT / "plugin" / "agents").glob("*/README.md"))
    assert agent_readmes

    for path in agent_readmes:
        text = path.read_text(encoding="utf-8")
        assert FULL_DISCLAIMER in text, path
        assert "not investment advice" in text.lower(), path
        assert "BRAND_USAGE_POLICY" in text, path


def test_spacx_research_suffix_adopted() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    manifest = (ROOT / "plugin" / "manifest.yaml").read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    github = (ROOT / "GITHUB.md").read_text(encoding="utf-8")

    assert readme.startswith("# SPACX-Research\n")
    assert "SPACX-Research" in readme
    assert "spacx-research-intelligence" in readme
    assert "openjay/spacx-research" in readme
    assert "git clone git@github.com:openjay/spacx-research.git" in readme

    assert 'id: spacx-research-intelligence' in manifest
    assert "SPACX-Research Autonomous Market Intelligence" in manifest
    assert "openjay/spacx-research" in manifest

    assert 'name = "spacx-research"' in pyproject

    assert "https://github.com/openjay/spacx-research" in github
    assert "SPACX-Research" in github

    brand_policy = (ROOT / "docs" / "BRAND_USAGE_POLICY.md").read_text(encoding="utf-8")
    assert "## Required naming (marketing and titles)" in brand_policy
    assert "Bare **SPACX**" in brand_policy

    audit = (ROOT / "docs" / "TRADEMARK_BRAND_AUDIT.md").read_text(encoding="utf-8")
    assert "## Suffix adoption" in audit
