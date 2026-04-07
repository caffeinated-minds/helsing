#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


ROOT = Path(__file__).resolve().parent.parent
GENERATOR_DIR = ROOT / "generator"
TEMPLATES_DIR = GENERATOR_DIR / "templates"
PALETTE_FILE = ROOT / "docs" / "helsing-palette.yml"
NEOVIM_CONFIG_FILE = GENERATOR_DIR / "config" / "neovim.yml"
WEZTERM_CONFIG_FILE = GENERATOR_DIR / "config" / "wezterm.yml"
VSCODE_CONFIG_FILE = GENERATOR_DIR / "config" / "vscode.yml"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at {path}")
    return data


def build_base_context() -> dict:
    palette = load_yaml(PALETTE_FILE)

    core = palette["core"]
    structural = core["structural"]
    semantic = core["semantic"]

    colors = {}
    colors.update(structural)
    colors.update(semantic)

    return {
        "palette": palette,
        "colors": colors,
        "structural": structural,
        "semantic": semantic,
    }


def build_neovim_context() -> dict:
    context = build_base_context()
    neovim = load_yaml(NEOVIM_CONFIG_FILE)
    helpers = neovim["helpers"]

    context["colors"].update(helpers)
    context["neovim"] = neovim
    context["helpers"] = helpers
    return context


def build_wezterm_context() -> dict:
    context = build_base_context()
    wezterm = load_yaml(WEZTERM_CONFIG_FILE)
    context["wezterm"] = wezterm
    return context


def resolve_tokens(value, colors: dict) -> object:
    if isinstance(value, dict):
        return {key: resolve_tokens(item, colors) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve_tokens(item, colors) for item in value]
    if isinstance(value, str):
        return colors.get(value, value)
    return value


def build_vscode_context() -> dict:
    context = build_base_context()
    vscode = load_yaml(VSCODE_CONFIG_FILE)
    helpers = vscode.get("helpers", {})

    context["colors"].update(helpers)
    context["vscode"] = resolve_tokens(vscode, context["colors"])
    return context


def render_template(template_name: str, context: dict) -> str:
    environment = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    environment.filters["to_pretty_json"] = lambda value: json.dumps(value, indent=2)
    template = environment.get_template(template_name)
    return template.render(**context)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_neovim() -> Path:
    context = build_neovim_context()
    output = render_template("neovim/helsing.lua.j2", context)
    output_path = ROOT / context["neovim"]["output"]
    write_file(output_path, output)
    return output_path


def generate_wezterm() -> Path:
    context = build_wezterm_context()
    output = render_template("wezterm/helsing.toml.j2", context)
    output_path = ROOT / context["wezterm"]["output"]
    write_file(output_path, output)
    return output_path


def generate_vscode() -> Path:
    context = build_vscode_context()
    output = render_template("vscode/helsing-color-theme.json.j2", context)
    output_path = ROOT / context["vscode"]["output"]
    write_file(output_path, output)
    return output_path


def main() -> int:
    try:
        output_paths = [
            generate_neovim(),
            generate_wezterm(),
            generate_vscode(),
        ]
    except Exception as exc:  # pragma: no cover - CLI failure path
        print(f"Generation failed: {exc}", file=sys.stderr)
        return 1

    for output_path in output_paths:
        print(f"Generated {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
