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
ALACRITTY_CONFIG_FILE = GENERATOR_DIR / "config" / "alacritty.yml"
WAYBAR_CONFIG_FILE = GENERATOR_DIR / "config" / "waybar.yml"
SWAY_CONFIG_FILE = GENERATOR_DIR / "config" / "sway.yml"
CHROME_CONFIG_FILE = GENERATOR_DIR / "config" / "chrome.yml"


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


def build_alacritty_context() -> dict:
    context = build_base_context()
    alacritty = load_yaml(ALACRITTY_CONFIG_FILE)
    helpers = alacritty.get("helpers", {})

    context["colors"].update(helpers)
    context["alacritty"] = resolve_tokens(alacritty, context["colors"])
    return context


def build_waybar_context() -> dict:
    context = build_base_context()
    waybar = load_yaml(WAYBAR_CONFIG_FILE)
    helpers = waybar.get("helpers", {})

    context["colors"].update(helpers)
    context["waybar"] = resolve_tokens(waybar, context["colors"])
    return context


def build_sway_context() -> dict:
    context = build_base_context()
    sway = load_yaml(SWAY_CONFIG_FILE)
    helpers = sway.get("helpers", {})

    context["colors"].update(helpers)
    context["sway"] = resolve_tokens(sway, context["colors"])
    return context


def hex_to_rgb(value: str) -> list[int]:
    if not value.startswith("#"):
        raise ValueError(f"Expected hex color, got {value!r}")

    hex_value = value.removeprefix("#")
    if len(hex_value) == 3:
        hex_value = "".join(channel * 2 for channel in hex_value)
    if len(hex_value) != 6:
        raise ValueError(f"Expected 3 or 6 hex digits, got {value!r}")

    return [int(hex_value[index : index + 2], 16) for index in range(0, 6, 2)]


def build_chrome_context() -> dict:
    context = build_base_context()
    chrome = load_yaml(CHROME_CONFIG_FILE)
    helpers = chrome.get("helpers", {})

    context["colors"].update(helpers)
    resolved = resolve_tokens(chrome, context["colors"])

    theme_colors = resolved.get("theme", {}).get("colors", {})
    resolved["theme"]["colors"] = {
        key: hex_to_rgb(value) if isinstance(value, str) else value
        for key, value in theme_colors.items()
    }

    context["chrome"] = resolved
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


def generate_alacritty() -> Path:
    context = build_alacritty_context()
    output = render_template("alacritty/helsing.toml.j2", context)
    output_path = ROOT / context["alacritty"]["output"]
    write_file(output_path, output)
    return output_path


def generate_waybar() -> Path:
    context = build_waybar_context()
    style_output = render_template("waybar/style.css.j2", context)
    style_path = ROOT / context["waybar"]["outputs"]["style"]
    write_file(style_path, style_output)

    colors_output = render_template("waybar/colors.css.j2", context)
    colors_path = ROOT / context["waybar"]["outputs"]["colors"]
    write_file(colors_path, colors_output)
    return style_path


def generate_sway() -> Path:
    context = build_sway_context()
    output = render_template("sway/config.j2", context)
    output_path = ROOT / context["sway"]["output"]
    write_file(output_path, output)
    return output_path


def generate_chrome() -> Path:
    context = build_chrome_context()
    output = render_template("chrome/manifest.json.j2", context)
    output_path = ROOT / context["chrome"]["output"]
    write_file(output_path, output)
    return output_path


def main() -> int:
    try:
        output_paths = [
            generate_neovim(),
            generate_wezterm(),
            generate_vscode(),
            generate_alacritty(),
            generate_waybar(),
            generate_sway(),
            generate_chrome(),
        ]
    except Exception as exc:  # pragma: no cover - CLI failure path
        print(f"Generation failed: {exc}", file=sys.stderr)
        return 1

    for output_path in output_paths:
        print(f"Generated {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
