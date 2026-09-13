# Helsing Theme Generator

This folder contains the generator that turns the canonical colour and typography contract in `docs/helsing-palette.yml` into target theme files.

## Purpose

The contract lives in one place:

- `docs/helsing-palette.yml`

The generator consumes that contract and renders target-specific output such as:

- `themes/neovim/helsing.lua`
- `themes/neovim/lua/helsing/integrations/bufferline.lua`
- `themes/wezterm/helsing.toml`
- `themes/vscode/themes/helsing-color-theme.json`
- `themes/alacritty/helsing.toml`
- `themes/waybar/style.css`
- `themes/waybar/colors.css`
- `themes/sway/config`
- `themes/chrome/manifest.json`
- `themes/mintty/helsing.minttyrc`
- `themes/doom-emacs/helsing-theme.el`

## Layout

- `generator/generate.py`
  - entrypoint for generation
- `generator/requirements.txt`
  - Python dependencies
- `generator/templates/neovim/helsing.lua.j2`
  - Neovim theme entrypoint
- `generator/templates/neovim/partials/`
  - declarative editor, language and optional plugin highlight mappings
- `generator/templates/neovim/bufferline.lua.j2`
  - explicit `bufferline.nvim` configuration adapter
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
- `generator/templates/mintty/helsing.minttyrc.j2`
  - Mintty and Git Bash colour-scheme template
- `generator/config/mintty.yml`
  - Mintty foreground, background, selection, cursor, and ANSI mappings
- `generator/templates/doom-emacs/helsing-theme.el.j2`
  - Doom Emacs theme entrypoint
- `generator/templates/doom-emacs/role-matrix.md.j2`
  - generated role-to-face documentation
- `generator/templates/doom-emacs/face-contract.el.j2`
  - generated executable test expectations
- `generator/config/doom-emacs.yml`
  - Doom-specific neutral ramp, semantic aliases, face contract and helper surfaces

## Usage

From the repo root:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r generator/requirements.txt
python generator/generate.py
```

Generate only the targets needed by a target-specific release:

```bash
python generator/generate.py vscode
python generator/generate.py chrome mintty
python generator/generate.py doom-emacs
```

With no target arguments, the generator continues to render every target.

Verify that every committed generated target matches its template and configuration without modifying the working tree:

```bash
python generator/generate.py --check
```

Run the repository validation after changing a palette, target configuration or template:

```bash
./checks/validate.sh
```

The Doom Emacs target produces three coordinated artifacts: the loadable theme, `docs/helsing-emacs-role-matrix.md`, and `checks/generated/helsing-emacs-face-contract.el`. This keeps implementation, documentation and tests on the same contract.

The VS Code target also produces three coordinated artifacts: the packaged theme, `docs/helsing-vscode-role-matrix.md`, and `checks/generated/helsing-vscode-token-contract.json`. The target validator rejects unknown palette references, undocumented helper colours, dangerous broad selectors, missing role coverage, stale outputs, and fixture expectations that no longer identify source text.

From `themes/vscode`, the reproducible target commands are:

```bash
npm ci
npm run theme:check
npm run package:vsix
```

`npm run package:vsix` invokes `vscode:prepublish`, so packaging stops if the generated artifacts are stale or validation fails. Set `HELSING_PYTHON` only when the project virtual environment and the normal `python3` or `python` commands are unavailable.

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
- `generator/config/mintty.yml`
- `generator/config/doom-emacs.yml`

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
