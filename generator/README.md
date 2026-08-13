# Helsing Theme Generator

This folder contains the generator that turns the canonical palette in `docs/helsing-palette.yml` into target theme files.

## Purpose

The contract lives in one place:

- `docs/helsing-palette.yml`

The generator consumes that contract and renders target-specific output such as:

- `themes/neovim/helsing.lua`
- `themes/wezterm/helsing.toml`
- `themes/vscode/themes/helsing-color-theme.json`
- `themes/alacritty/helsing.toml`
- `themes/waybar/style.css`
- `themes/waybar/colors.css`
- `themes/sway/config`
- `themes/chrome/manifest.json`

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
- `generator/templates/alacritty/helsing.toml.j2`
  - Alacritty color theme template
- `generator/config/alacritty.yml`
  - Alacritty color mappings, cursor/search colors, and ANSI slots
- `generator/templates/waybar/style.css.j2`
  - Waybar stylesheet template
- `generator/templates/waybar/colors.css.j2`
  - Waybar GTK color definitions for imported palette values
- `generator/config/waybar.yml`
  - Waybar CSS mappings, helper surfaces, and module accent groups
- `generator/templates/sway/config.j2`
  - Sway config template
- `generator/config/sway.yml`
  - Sway theme values, startup commands, and client color mappings
- `generator/templates/chrome/manifest.json.j2`
  - Chrome theme manifest template
- `generator/config/chrome.yml`
  - Chrome browser color mappings and theme metadata

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
- `generator/config/alacritty.yml`
- `generator/config/waybar.yml`
- `generator/config/sway.yml`
- `generator/config/chrome.yml`

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
