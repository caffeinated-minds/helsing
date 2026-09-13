#!/usr/bin/env python3

from __future__ import annotations

import argparse
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
MINTTY_CONFIG_FILE = GENERATOR_DIR / "config" / "mintty.yml"
DOOM_EMACS_CONFIG_FILE = GENERATOR_DIR / "config" / "doom-emacs.yml"


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


def build_mintty_context() -> dict:
    context = build_base_context()
    mintty = load_yaml(MINTTY_CONFIG_FILE)
    context["mintty"] = resolve_tokens(mintty, context["colors"])
    return context


def build_doom_emacs_context() -> dict:
    context = build_base_context()
    doom_emacs = load_yaml(DOOM_EMACS_CONFIG_FILE)
    helpers = doom_emacs.get("helpers", {})

    context["colors"].update(helpers)
    semantic_roles = context["palette"]["semantic_roles"]

    def resolve_role(role: str) -> dict[str, str]:
        token = semantic_roles.get(role, role)
        if token not in context["colors"]:
            raise ValueError(
                f"Unknown Doom Emacs role or token {role!r} (resolved to {token!r})"
            )
        return {
            "role": role,
            "token": token,
            "color": context["colors"][token],
        }

    role_aliases = doom_emacs.get("role_aliases", {})
    context["doom_role_aliases"] = [
        {"alias": alias, **resolve_role(role)}
        for alias, role in role_aliases.items()
    ]

    seen_faces: set[str] = set()
    face_groups = []
    for layer, entries in doom_emacs.get("face_contract", {}).items():
        resolved_entries = []
        for entry in entries:
            face = entry["face"]
            if face in seen_faces:
                raise ValueError(f"Duplicate Doom Emacs face contract: {face}")
            seen_faces.add(face)

            resolved = dict(entry)
            for attribute in ("foreground", "background"):
                if role := entry.get(attribute):
                    resolved[attribute] = resolve_role(role)
            resolved_entries.append(resolved)
        face_groups.append({"layer": layer, "entries": resolved_entries})

    context["doom_face_groups"] = face_groups

    terminal_contract = []
    for name, entry in doom_emacs.get("terminal_contract", {}).items():
        token = entry["token"]
        if token not in context["colors"]:
            raise ValueError(
                f"Unknown Doom Emacs terminal token {token!r} for {name!r}"
            )
        terminal_contract.append(
            {
                "name": name,
                "token": token,
                "color": context["colors"][token],
                "ansi256": entry["ansi256"],
                "tty": entry["tty"],
            }
        )
    context["doom_terminal_contract"] = terminal_contract

    helper_usage = doom_emacs.get("helper_usage", {})
    undocumented_helpers = set(helpers) - set(helper_usage)
    unknown_helper_docs = set(helper_usage) - set(helpers)
    if undocumented_helpers:
        raise ValueError(
            "Undocumented Doom Emacs helpers: "
            + ", ".join(sorted(undocumented_helpers))
        )
    if unknown_helper_docs:
        raise ValueError(
            "Doom Emacs helper documentation has no value: "
            + ", ".join(sorted(unknown_helper_docs))
        )
    context["doom_helper_usage"] = [
        {"name": name, "color": color, "usage": helper_usage[name]}
        for name, color in helpers.items()
    ]
    context["doom_emacs"] = doom_emacs
    context["helpers"] = helpers
    return context


def generate_doom_emacs(*, check: bool = False) -> list[Path]:
    context = build_doom_emacs_context()
    outputs = context["doom_emacs"]["outputs"]

    theme_output = render_template("doom-emacs/helsing-theme.el.j2", context)
    theme_path = ROOT / outputs["theme"]
    write_file(theme_path, theme_output, check=check)

    matrix_output = render_template("doom-emacs/role-matrix.md.j2", context)
    matrix_path = ROOT / outputs["role_matrix"]
    write_file(matrix_path, matrix_output, check=check)

    contract_output = render_template("doom-emacs/face-contract.el.j2", context)
    contract_path = ROOT / outputs["test_contract"]
    write_file(contract_path, contract_output, check=check)

    return [theme_path, matrix_path, contract_path]


def hex_to_rgb_csv(value: str) -> str:
    return ",".join(str(channel) for channel in hex_to_rgb(value))


def render_template(template_name: str, context: dict) -> str:
    environment = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    environment.filters["to_pretty_json"] = lambda value: json.dumps(value, indent=2)
    environment.filters["to_rgb_csv"] = hex_to_rgb_csv
    template = environment.get_template(template_name)
    return template.render(**context)


def write_file(path: Path, content: str, *, check: bool = False) -> None:
    if check:
        if not path.is_file():
            raise ValueError(f"Generated output is missing: {path.relative_to(ROOT)}")
        if path.read_text(encoding="utf-8") != content:
            raise ValueError(f"Generated output is stale: {path.relative_to(ROOT)}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_neovim(*, check: bool = False) -> list[Path]:
    context = build_neovim_context()
    theme_output = render_template("neovim/helsing.lua.j2", context)
    theme_path = ROOT / context["neovim"]["outputs"]["theme"]
    write_file(theme_path, theme_output, check=check)

    bufferline_output = render_template("neovim/bufferline.lua.j2", context)
    bufferline_path = ROOT / context["neovim"]["outputs"]["bufferline"]
    write_file(bufferline_path, bufferline_output, check=check)
    return [theme_path, bufferline_path]


def generate_wezterm(*, check: bool = False) -> list[Path]:
    context = build_wezterm_context()
    output = render_template("wezterm/helsing.toml.j2", context)
    output_path = ROOT / context["wezterm"]["output"]
    write_file(output_path, output, check=check)
    return [output_path]


def generate_vscode(*, check: bool = False) -> list[Path]:
    context = build_vscode_context()
    output = render_template("vscode/helsing-color-theme.json.j2", context)
    output_path = ROOT / context["vscode"]["output"]
    write_file(output_path, output, check=check)
    return [output_path]


def generate_alacritty(*, check: bool = False) -> list[Path]:
    context = build_alacritty_context()
    output = render_template("alacritty/helsing.toml.j2", context)
    output_path = ROOT / context["alacritty"]["output"]
    write_file(output_path, output, check=check)
    return [output_path]


def generate_waybar(*, check: bool = False) -> list[Path]:
    context = build_waybar_context()
    style_output = render_template("waybar/style.css.j2", context)
    style_path = ROOT / context["waybar"]["outputs"]["style"]
    write_file(style_path, style_output, check=check)

    colors_output = render_template("waybar/colors.css.j2", context)
    colors_path = ROOT / context["waybar"]["outputs"]["colors"]
    write_file(colors_path, colors_output, check=check)
    return [style_path, colors_path]


def generate_sway(*, check: bool = False) -> list[Path]:
    context = build_sway_context()
    output = render_template("sway/config.j2", context)
    output_path = ROOT / context["sway"]["output"]
    write_file(output_path, output, check=check)
    return [output_path]


def generate_chrome(*, check: bool = False) -> list[Path]:
    context = build_chrome_context()
    output = render_template("chrome/manifest.json.j2", context)
    output_path = ROOT / context["chrome"]["output"]
    write_file(output_path, output, check=check)
    return [output_path]


def generate_mintty(*, check: bool = False) -> list[Path]:
    context = build_mintty_context()
    output = render_template("mintty/helsing.minttyrc.j2", context)
    output_path = ROOT / context["mintty"]["output"]
    write_file(output_path, output, check=check)
    return [output_path]


def main() -> int:
    generators = {
        "neovim": generate_neovim,
        "wezterm": generate_wezterm,
        "vscode": generate_vscode,
        "alacritty": generate_alacritty,
        "waybar": generate_waybar,
        "sway": generate_sway,
        "chrome": generate_chrome,
        "mintty": generate_mintty,
        "doom-emacs": generate_doom_emacs,
    }
    parser = argparse.ArgumentParser(
        description="Generate Helsing theme artifacts."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        choices=generators,
        help="targets to generate (default: all targets)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated outputs without modifying them",
    )
    args = parser.parse_args()
    selected_targets = args.targets or list(generators)

    try:
        output_paths = [
            output_path
            for target in selected_targets
            for output_path in generators[target](check=args.check)
        ]
    except Exception as exc:  # pragma: no cover - CLI failure path
        print(f"Generation failed: {exc}", file=sys.stderr)
        return 1

    action = "Verified" if args.check else "Generated"
    for output_path in output_paths:
        print(f"{action} {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
