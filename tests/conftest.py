"""Shared paths and schema helpers for SPACX contract tests."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "plugin" / "schemas"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"

_FORMAT_CHECKER = Draft202012Validator.FORMAT_CHECKER


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate_instance(instance: object, schema_name: str) -> None:
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema, format_checker=_FORMAT_CHECKER)
    validator.validate(instance)


def load_fixture(name: str) -> dict | list:
    path = FIXTURE_DIR / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)
