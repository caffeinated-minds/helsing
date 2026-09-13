#!/usr/bin/env python3
"""Validate the generated Helsing VS Code theme and its source contract."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from generator.generate import build_vscode_context  # noqa: E402


HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
THEME_FILE = ROOT / "themes/vscode/themes/helsing-color-theme.json"
CONTRACT_FILE = ROOT / "checks/generated/helsing-vscode-token-contract.json"


def iter_hex_colors(value, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from iter_hex_colors(item, (*path, str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_hex_colors(item, (*path, str(index)))
    elif isinstance(value, str) and HEX_COLOR.fullmatch(value):
        yield path, value.upper()


context = build_vscode_context()
theme = json.loads(THEME_FILE.read_text(encoding="utf-8"))
contract = json.loads(CONTRACT_FILE.read_text(encoding="utf-8"))
failures: list[str] = []

if theme.get("$schema") != "vscode://schemas/color-theme":
    failures.append("generated theme has the wrong or missing schema")
if theme.get("name") != context["vscode"]["metadata"]["name"]:
    failures.append("generated theme name does not match source metadata")
if theme.get("type") != context["vscode"]["metadata"]["type"]:
    failures.append("generated theme type does not match source metadata")
if theme.get("semanticHighlighting") is not True:
    failures.append("semantic highlighting must be enabled deliberately")
if not isinstance(theme.get("tokenColors"), list) or not theme["tokenColors"]:
    failures.append("generated theme has no TextMate token colours")
if not isinstance(theme.get("semanticTokenColors"), dict) or not theme[
    "semanticTokenColors"
]:
    failures.append("generated theme has no semantic-token colours")

allowed_colors = {color.upper() for color in context["colors"].values()}
for path, color in iter_hex_colors(theme):
    if color not in allowed_colors:
        failures.append(
            f"generated theme contains unapproved colour {color} at {'.'.join(path)}"
        )

for rule in theme.get("tokenColors", []):
    unexpected = set(rule) - {"name", "scope", "settings"}
    if unexpected:
        failures.append(
            f"generated TextMate rule {rule.get('name')!r} leaked source metadata: "
            + ", ".join(sorted(unexpected))
        )

for selector, settings in theme.get("semanticTokenColors", {}).items():
    unexpected = set(settings) - {"foreground", "background", "fontStyle"}
    if unexpected:
        failures.append(
            f"generated semantic selector {selector!r} leaked source metadata: "
            + ", ".join(sorted(unexpected))
        )

if contract != context["vscode_test_contract"]:
    failures.append("generated VS Code token contract is stale")

for forbidden_scope in ("storage", "storage.type", "support", "meta.function-call"):
    if any(
        forbidden_scope in rule.get("scope", [])
        for rule in theme.get("tokenColors", [])
    ):
        failures.append(f"dangerous broad scope is present: {forbidden_scope}")

if failures:
    print("VS Code validation failed:", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    raise SystemExit(1)

print("Helsing VS Code contract checks passed")
