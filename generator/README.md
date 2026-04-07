# Helsing Theme Generator

This folder contains the generator that turns the canonical palette in `docs/helsing-palette.yml` into target theme files.

## Purpose

The contract lives in one place:

- `docs/helsing-palette.yml`

The generator consumes that contract and renders target-specific output such as:

- `themes/neovim/helsing.lua`
- `themes/wezterm/helsing.toml`
- `themes/vscode/helsing-color-theme.json`

## Layout

- `generator/generate.py`
  - entrypoint for generation
- `generator/requirements.txt`
  - Python dependencies
- `generator/templates/neovim/helsing.lua.j2`
  - Neovim theme template
- `generator/config/neovim.yml`
  - Neovim-specific helper colors and metadata
- `generator/templates/wezterm/helsing.toml.j2`
  - WezTerm color scheme template
- `generator/config/wezterm.yml`
  - WezTerm-specific mappings, ANSI slots, and tab bar colors
- `generator/templates/vscode/helsing-color-theme.json.j2`
  - VS Code color theme template
- `generator/config/vscode.yml`
  - VS Code UI colors, token scopes, and semantic token mappings

## Usage

From the repo root:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r generator/requirements.txt
python generator/generate.py
```

## What is canonical vs target-specific

Canonical data belongs in:

- `docs/helsing-palette.yml`

Target-specific data belongs in:

- `generator/config/neovim.yml`
- `generator/config/wezterm.yml`
- `generator/config/vscode.yml`

Examples of target-specific data:

- diff backgrounds
- popup menu backgrounds
- cursorline surface
- line number tone
- terminal ANSI slot mappings
- tab bar state colors
- quick select and copy mode colors

## Rule

Change the palette in `docs/helsing-palette.yml` first.

Then regenerate targets.
