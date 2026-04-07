#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


ROOT = Path(__file__).resolve().parent.parent
GENERATOR_DIR = ROOT / "generator"
TEMPLATES_DIR = GENERATOR_DIR / "templates"
PALETTE_FILE = ROOT / "docs" / "helsing-palette.yml"
NEOVIM_CONFIG_FILE = GENERATOR_DIR / "config" / "neovim.yml"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at {path}")
    return data


def build_context() -> dict:
    palette = load_yaml(PALETTE_FILE)
    neovim = load_yaml(NEOVIM_CONFIG_FILE)

    core = palette["core"]
    structural = core["structural"]
    semantic = core["semantic"]
    helpers = neovim["helpers"]

    colors = {}
    colors.update(structural)
    colors.update(semantic)
    colors.update(helpers)

    return {
        "palette": palette,
        "target": neovim,
        "colors": colors,
        "structural": structural,
        "semantic": semantic,
        "helpers": helpers,
    }


def render_template(template_name: str, context: dict) -> str:
    environment = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    template = environment.get_template(template_name)
    return template.render(**context)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_neovim() -> Path:
    context = build_context()
    output = render_template("neovim/helsing.lua.j2", context)
    output_path = ROOT / context["target"]["output"]
    write_file(output_path, output)
    return output_path


def main() -> int:
    try:
        output_path = generate_neovim()
    except Exception as exc:  # pragma: no cover - CLI failure path
        print(f"Generation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Generated {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
