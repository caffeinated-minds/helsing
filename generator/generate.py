#!/usr/bin/env python3

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
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
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


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

    semantic_roles = palette.get("semantic_roles", {})
    role_contracts = palette.get("role_contracts", {})
    if set(semantic_roles) != set(role_contracts):
        missing_contracts = sorted(set(semantic_roles) - set(role_contracts))
        unknown_contracts = sorted(set(role_contracts) - set(semantic_roles))
        details = []
        if missing_contracts:
            details.append("missing contracts: " + ", ".join(missing_contracts))
        if unknown_contracts:
            details.append("unknown contracts: " + ", ".join(unknown_contracts))
        raise ValueError("Palette role contract mismatch (" + "; ".join(details) + ")")

    for role, token in semantic_roles.items():
        contract = role_contracts[role]
        if contract.get("token") != token:
            raise ValueError(
                f"Role {role!r} maps to {token!r}, but its contract maps to "
                f"{contract.get('token')!r}"
            )
        if token not in colors:
            raise ValueError(f"Role {role!r} references unknown token {token!r}")
        for field in ("intent", "usage", "styles", "fallback", "examples"):
            if field not in contract:
                raise ValueError(f"Role {role!r} has no {field!r} contract field")
        fallback = contract["fallback"]
        if fallback is not None and fallback not in semantic_roles:
            raise ValueError(
                f"Role {role!r} references unknown fallback role {fallback!r}"
            )

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


def find_hex_literals(value, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from find_hex_literals(item, (*path, str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from find_hex_literals(item, (*path, str(index)))
    elif isinstance(value, str) and HEX_COLOR.fullmatch(value):
        yield path, value


def build_vscode_context() -> dict:
    context = build_base_context()
    source = load_yaml(VSCODE_CONFIG_FILE)
    helpers = source.get("helpers", {})
    helper_usage = source.get("helper_usage", {})
    semantic_roles = context["palette"]["semantic_roles"]
    role_contracts = context["palette"]["role_contracts"]

    unapproved_literals = [
        (path, value)
        for path, value in find_hex_literals(source)
        if not path or path[0] != "helpers"
    ]
    if unapproved_literals:
        locations = ", ".join(
            f"{'.'.join(path)}={value}" for path, value in unapproved_literals
        )
        raise ValueError(
            "VS Code source contains raw hex colours outside helpers: " + locations
        )

    if set(helpers) != set(helper_usage):
        undocumented = sorted(set(helpers) - set(helper_usage))
        unknown_docs = sorted(set(helper_usage) - set(helpers))
        details = []
        if undocumented:
            details.append("undocumented helpers: " + ", ".join(undocumented))
        if unknown_docs:
            details.append("unknown helper docs: " + ", ".join(unknown_docs))
        raise ValueError("VS Code helper contract mismatch (" + "; ".join(details) + ")")
    for helper, color in helpers.items():
        if not isinstance(color, str) or not HEX_COLOR.fullmatch(color):
            raise ValueError(f"VS Code helper {helper!r} is not a six-digit hex colour")
        if not isinstance(helper_usage[helper], str) or not helper_usage[helper].strip():
            raise ValueError(f"VS Code helper {helper!r} has no usage explanation")

    context["colors"].update(helpers)

    def role_details(role: str) -> dict[str, str]:
        if role not in semantic_roles:
            raise ValueError(f"Unknown VS Code role {role!r}")
        token = semantic_roles[role]
        return {"role": role, "token": token, "color": context["colors"][token]}

    def validate_style(role: str, settings: dict, location: str) -> None:
        style_value = settings.get("fontStyle")
        if style_value is None:
            return
        styles = [style for style in style_value.split() if style] or ["normal"]
        allowed = set(role_contracts[role]["styles"])
        invalid = sorted(set(styles) - allowed)
        if invalid:
            raise ValueError(
                f"{location} uses styles not allowed by role {role!r}: "
                + ", ".join(invalid)
            )

    resolved_colors = {}
    for name, token in source.get("colors", {}).items():
        if token not in context["colors"]:
            raise ValueError(
                f"VS Code workbench colour {name!r} references unknown token {token!r}"
            )
        resolved_colors[name] = context["colors"][token]

    textmate_roles: dict[str, list[str]] = defaultdict(list)
    scope_owners: dict[str, str] = {}
    token_colors = []
    for rule in source.get("tokenColors", []):
        role = rule.get("role")
        details = role_details(role)
        settings = dict(rule.get("settings", {}))
        if "foreground" in settings:
            raise ValueError(
                f"VS Code TextMate rule {rule['name']!r} embeds a foreground; use its role"
            )
        validate_style(role, settings, f"VS Code TextMate rule {rule['name']!r}")
        settings["foreground"] = details["color"]
        scopes = rule.get("scope", [])
        if not scopes:
            raise ValueError(f"VS Code TextMate rule {rule['name']!r} has no scopes")
        for scope in scopes:
            if scope in scope_owners:
                raise ValueError(
                    f"VS Code TextMate scope {scope!r} is owned by both "
                    f"{scope_owners[scope]!r} and {rule['name']!r}"
                )
            scope_owners[scope] = rule["name"]
        textmate_roles[role].extend(scopes)
        token_colors.append(
            {"name": rule["name"], "scope": scopes, "settings": settings}
        )

    dangerous_scopes = {
        "storage",
        "storage.type",
        "support",
        "support.function",
        "support.type",
        "variable",
        "meta.function-call",
    }
    allowlist = source.get("scope_allowlist", {})
    used_dangerous_scopes = dangerous_scopes.intersection(scope_owners)
    if used_dangerous_scopes != set(allowlist):
        unapproved = sorted(used_dangerous_scopes - set(allowlist))
        unused = sorted(set(allowlist) - used_dangerous_scopes)
        details = []
        if unapproved:
            details.append("unapproved: " + ", ".join(unapproved))
        if unused:
            details.append("unused allow-list entries: " + ", ".join(unused))
        raise ValueError("VS Code dangerous-scope contract mismatch (" + "; ".join(details) + ")")
    for scope, exception in allowlist.items():
        owner = next(rule for rule in source["tokenColors"] if scope in rule["scope"])
        if exception.get("role") != owner["role"] or not exception.get("reason"):
            raise ValueError(f"Invalid VS Code scope allow-list entry for {scope!r}")

    semantic_roles_used: dict[str, list[str]] = defaultdict(list)
    semantic_token_colors = {}
    for selector, specification in source.get("semanticTokenColors", {}).items():
        settings = dict(specification.get("settings", {}))
        role = specification.get("role")
        is_modifier = specification.get("modifier") is True
        if bool(role) == is_modifier:
            raise ValueError(
                f"VS Code semantic selector {selector!r} must define exactly one of role or modifier"
            )
        if "foreground" in settings:
            raise ValueError(
                f"VS Code semantic selector {selector!r} embeds a foreground; use its role"
            )
        if role:
            details = role_details(role)
            validate_style(role, settings, f"VS Code semantic selector {selector!r}")
            settings["foreground"] = details["color"]
            semantic_roles_used[role].append(selector)
        elif not selector.startswith("*.") or not settings.get("fontStyle"):
            raise ValueError(
                f"VS Code semantic modifier {selector!r} must be a style-only wildcard selector"
            )
        semantic_token_colors[selector] = settings

    def textmate_selector_matches(selector: str, observed_scope: str) -> bool:
        leaf_selector = selector.split()[-1]
        return observed_scope == leaf_selector or observed_scope.startswith(
            leaf_selector + "."
        )

    def textmate_winning_roles(observed_scopes: list[str]) -> set[str]:
        candidates = []
        for rule in source.get("tokenColors", []):
            for selector in rule.get("scope", []):
                for observed_scope in observed_scopes:
                    if textmate_selector_matches(selector, observed_scope):
                        leaf_selector = selector.split()[-1]
                        specificity = len(leaf_selector.split("."))
                        candidates.append((specificity, rule["role"]))
        if not candidates:
            return set()
        winning_specificity = max(specificity for specificity, _role in candidates)
        return {
            role
            for specificity, role in candidates
            if specificity == winning_specificity
        }

    def semantic_selector_matches(selector: str, observed_token: str) -> bool:
        if selector.startswith("*."):
            return False
        return observed_token == selector or observed_token.startswith(selector + ".")

    def semantic_winning_roles(observed_token: str) -> set[str]:
        candidates = []
        for selector, specification in source.get("semanticTokenColors", {}).items():
            role = specification.get("role")
            if role and semantic_selector_matches(selector, observed_token):
                candidates.append((len(selector.split(".")), role))
        if not candidates:
            return set()
        winning_specificity = max(specificity for specificity, _role in candidates)
        return {
            role
            for specificity, role in candidates
            if specificity == winning_specificity
        }

    coverage = source.get("coverage", {})
    semantic_fallbacks = coverage.get("semantic_fallbacks", {})
    for role in coverage.get("required_roles", []):
        if not textmate_roles.get(role):
            raise ValueError(f"Required VS Code role {role!r} has no TextMate mapping")
        if not semantic_roles_used.get(role) and role not in semantic_fallbacks:
            raise ValueError(
                f"Required VS Code role {role!r} has no semantic mapping or documented fallback"
            )

    fixture_path = ROOT / source["fixtures"]
    fixture_contract = load_yaml(fixture_path)
    for fixture in fixture_contract.get("fixtures", []):
        source_path = ROOT / fixture["path"]
        if not source_path.is_file():
            raise ValueError(f"VS Code fixture is missing: {fixture['path']}")
        source_text = source_path.read_text(encoding="utf-8")
        for expectation in fixture.get("expectations", []):
            role = expectation["role"]
            role_details(role)
            textmate_role = expectation.get("textmate_role", role)
            semantic_role = expectation.get("semantic_role", role)
            role_details(textmate_role)
            role_details(semantic_role)
            if (textmate_role != role or semantic_role != role) and not expectation.get(
                "fallback_reason"
            ):
                raise ValueError(
                    f"VS Code fixture expectation {fixture['path']}:{expectation['text']!r} "
                    "overrides a rendering role without a fallback reason"
                )
            occurrence = expectation.get("occurrence", 1)
            if source_text.count(expectation["text"]) < occurrence:
                raise ValueError(
                    f"VS Code fixture {fixture['path']} does not contain occurrence "
                    f"{occurrence} of {expectation['text']!r}"
                )
            if not expectation.get("textmate_scopes"):
                raise ValueError(
                    f"VS Code fixture expectation {fixture['path']}:{expectation['text']!r} "
                    "has no TextMate scope record"
                )
            textmate_roles_winning = textmate_winning_roles(
                expectation["textmate_scopes"]
            )
            if textmate_role not in textmate_roles_winning:
                rendered_roles = ", ".join(sorted(textmate_roles_winning)) or "none"
                raise ValueError(
                    f"VS Code fixture expectation {fixture['path']}:{expectation['text']!r} "
                    f"resolves to TextMate role(s) {rendered_roles}, not {textmate_role!r}"
                )
            if "semantic_token" not in expectation:
                raise ValueError(
                    f"VS Code fixture expectation {fixture['path']}:{expectation['text']!r} "
                    "does not record semantic-token behaviour"
                )
            semantic_token = expectation["semantic_token"]
            if semantic_token is not None:
                semantic_roles_winning = semantic_winning_roles(semantic_token)
                if semantic_role not in semantic_roles_winning:
                    rendered_roles = (
                        ", ".join(sorted(semantic_roles_winning)) or "none"
                    )
                    raise ValueError(
                        f"VS Code fixture expectation {fixture['path']}:{expectation['text']!r} "
                        f"resolves to semantic role(s) {rendered_roles}, not {semantic_role!r}"
                    )

    all_role_rows = []
    for role, contract in role_contracts.items():
        token = semantic_roles[role]
        all_role_rows.append(
            {
                "role": role,
                "token": token,
                "color": context["colors"][token],
                "intent": contract["intent"],
                "styles": contract["styles"],
                "fallback": contract["fallback"],
                "textmate_scopes": textmate_roles.get(role, []),
                "semantic_selectors": semantic_roles_used.get(role, []),
                "semantic_fallback": semantic_fallbacks.get(role),
            }
        )

    context["vscode"] = {
        "metadata": source["metadata"],
        "outputs": source["outputs"],
        "colors": resolved_colors,
        "tokenColors": token_colors,
        "semanticTokenColors": semantic_token_colors,
    }
    context["vscode_role_rows"] = all_role_rows
    context["vscode_fixture_contract"] = fixture_contract
    context["vscode_test_contract"] = {
        "theme": source["metadata"]["name"],
        "paletteVersion": context["palette"]["version"],
        "roles": {row["role"]: row for row in all_role_rows},
        "scopeAllowlist": allowlist,
        "fixtures": fixture_contract.get("fixtures", []),
    }
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
    outputs = context["vscode"]["outputs"]

    output = render_template("vscode/helsing-color-theme.json.j2", context)
    output_path = ROOT / outputs["theme"]
    write_file(output_path, output, check=check)

    matrix_output = render_template("vscode/role-matrix.md.j2", context)
    matrix_path = ROOT / outputs["role_matrix"]
    write_file(matrix_path, matrix_output, check=check)

    contract_output = json.dumps(context["vscode_test_contract"], indent=2) + "\n"
    contract_path = ROOT / outputs["test_contract"]
    write_file(contract_path, contract_output, check=check)

    return [output_path, matrix_path, contract_path]


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
