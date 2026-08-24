# Helsing Theme Spec

This document turns the local Dracula template pattern and `docs/brief` into a reusable theme contract for Helsing.

## What the local Dracula template shows

### Typical assignment counts

The Dracula-style reference model used during Helsing's initial design has **22 named colour assignments**:

- **11 core palette tokens** used as the main theme contract:
  - `background`
  - `foreground`
  - `selection`
  - `comment`
  - `cyan`
  - `green`
  - `orange`
  - `pink`
  - `purple`
  - `red`
  - `yellow`
- **11 terminal/ANSI completion tokens** used when a target needs a full terminal palette:
  - `black`
  - `blue`
  - `magenta`
  - `bright_black`
  - `bright_red`
  - `bright_green`
  - `bright_yellow`
  - `bright_blue`
  - `bright_magenta`
  - `bright_cyan`
  - `bright_white`

That means the typical Dracula-style setup is:

- **11 semantic/core values** for general theme portability
- **22 named values total** when terminal ANSI slots are included

### Where colours are usually assigned

The pattern in this repo is consistent:

1. **Canonical palette/spec file**
   - Stores the durable palette contract and ANSI mappings
2. **Implementation file**
   - `themes/neovim/helsing.lua`
   - Maps palette tokens onto editor UI, syntax, diagnostics, diff, Treesitter, and plugin groups
3. **Design brief / rationale**
   - `docs/brief`
   - Explains the visual intent and semantic meaning of the tokens

## What the current Helsing implementation contains

The current Neovim theme at `themes/neovim/helsing.lua` defines **26 palette entries**:

- **16 core design tokens**
  - 7 neutral/base tokens
  - 9 accent tokens
- **10 implementation-specific helper tokens**
  - `diff_add`
  - `diff_change`
  - `diff_delete`
  - `search`
  - `incsearch`
  - `cursorline`
  - `linenr`
  - `visual`
  - `pmenu`
  - `pmenu_sel`

It currently maps those tokens across more than **600 highlight groups**, covering Neovim itself and explicitly supported plugin interfaces. These mappings remain declarative: plugin loading and lifecycle behaviour belong in optional integration modules or the user's plugin configuration. The group count will evolve with plugin coverage; the palette roles, rather than the raw count, are the stable contract.

## Recommended Helsing contract

Use a two-layer contract:

- **Layer 1: canonical palette** for portable semantic tokens
- **Layer 2: implementation helpers** for editor-specific UI details

This keeps Helsing portable like Dracula while still letting individual targets solve their own UI needs.

## Layer 1: Canonical palette

These are the tokens Helsing should treat as the stable, cross-platform contract.

### Base tokens

| Role | Token | Hex | Notes |
| --- | --- | --- | --- |
| Background | `bg` | `#F4F1EA` | Warm paper base |
| Background Alt | `bg_alt` | `#EAE5DC` | Panels, splits, line highlight base |
| Foreground | `fg` | `#2A2A2A` | Primary text |
| Muted | `muted` | `#6B6B6B` | Comments, secondary text |
| Subtle | `subtle` | `#A8A29E` | Low-emphasis UI chrome |
| Border | `border` | `#D6D0C4` | Dividers, separators |
| Selection | `selection` | `#E6DCC8` | Visual selection and active emphasis |

### Accent tokens

| Role | Token | Hex | Notes |
| --- | --- | --- | --- |
| Keyword | `purple` | `#7C6EE6` | Logic, control flow, declarations |
| Function | `blue` | `#3A7BD5` | Functions, calls, navigable actions |
| String | `green` | `#4C9A5F` | Strings and success states |
| Number | `orange` | `#C47A2C` | Numbers, constants with warmth |
| Type | `cyan` | `#2F8F8B` | Structural and type-level meaning |
| Constant | `pink` | `#C05A8C` | Constants, macros, rare emphasis |
| Error | `red` | `#C23B3B` | Errors and destructive states |
| Warning | `yellow` | `#B58900` | Warnings and caution states |
| Info | `info` | `#4A90E2` | Optional explicit info token |

### Canonical count

For Helsing, the recommended stable contract is:

- **16 canonical tokens total**
- Split as **7 base + 9 accents**
- If `info` is omitted in a specific target, the minimum contract becomes **15 tokens**

## Layer 2: Implementation helper tokens

These are allowed, but they should be considered derived or target-specific rather than part of the universal contract.

### Current Neovim helper tokens

| Token | Current Hex | Purpose |
| --- | --- | --- |
| `diff_add` | `#DCEEDB` | Added line background |
| `diff_change` | `#E8E1F3` | Changed line background |
| `diff_delete` | `#F3D9D9` | Removed line background |
| `search` | `#F1E7B8` | Search match background |
| `incsearch` | `#E8D58B` | Active search match |
| `cursorline` | `#EFE9DF` | Current line background |
| `linenr` | `#B3ADA4` | Inactive line numbers |
| `visual` | `#E6DCC8` | Visual alias of `selection` |
| `pmenu` | `#ECE7DE` | Popup menu background |
| `pmenu_sel` | `#DDD4C5` | Popup menu active item |

### Rule for helper tokens

Helper tokens should be:

- derived from the canonical palette when possible
- kept in implementation files like `themes/neovim/helsing.lua`
- avoided in the cross-platform spec unless multiple targets need them

## Semantic mapping rules

Helsing should follow role-based mapping, not syntax-name-first mapping.

| Semantic role | Token |
| --- | --- |
| Text | `fg` |
| Secondary text | `muted` |
| UI chrome | `subtle` |
| Border | `border` |
| Background | `bg` |
| Panel / alternate surface | `bg_alt` |
| Selection | `selection` |
| Keyword / control flow | `purple` |
| Function / callable | `blue` |
| String / success | `green` |
| Number / numeric literal | `orange` |
| Type / structural symbol | `cyan` |
| Constant / macro / special value | `pink` |
| Error / invalid | `red` |
| Warning / caution | `yellow` |
| Info / hint | `info` or `blue` |

## Assignment rules

### 1. Keep one canonical source of truth

Helsing should have exactly one palette spec file that defines the canonical tokens. Every implementation should import or mirror those tokens instead of inventing local hex values.

### 2. No ad-hoc hex in mappings

Implementation files should map groups to tokens, not directly to fresh colours. If a new hex value is necessary, promote it into either the canonical palette or the implementation helper section.

### 3. Separate semantic tokens from target helpers

Cross-platform tokens should stay stable. Editor-specific tokens such as popup menu backgrounds, diff fills, and search fills should live in the target implementation layer.

### 4. Prefer semantic names over editor names

Use token names like `bg`, `fg`, `muted`, `purple`, and `red` as the durable contract. Avoid making `LineNr`, `CursorLine`, or `Pmenu` part of the shared palette vocabulary.

### 5. Preserve warmth and restraint

Helsing should remain daylight-oriented, paper-like, and controlled:

- no pure white backgrounds
- no pure black foregrounds
- no neon accents
- low-chroma neutrals
- accents used for meaning, not decoration

### 6. Reuse accents consistently

Each accent should carry stable meaning across targets:

- `purple` for keywords and control flow
- `blue` for functions, links, and active affordances
- `green` for strings and positive status
- `orange` for numbers and warm emphasis
- `cyan` for types and structure
- `pink` for constants and special values
- `red` for errors and invalid states
- `yellow` for warnings and caution

### 7. Add ANSI only when the target needs it

If a target is a terminal theme, define the ANSI 0-15 slots explicitly. If it is an editor theme only, the canonical semantic palette is enough.

## Suggested file layout for Helsing

- `docs/helsing-theme-spec.md`
  - design contract, token meanings, mapping rules
- `docs/helsing-palette.yml`
  - optional future canonical machine-readable palette file
- `themes/neovim/helsing.lua`
  - Neovim implementation and helper tokens
- future targets such as `themes/vscode/`, `themes/alacritty/`, or `themes/wezterm/`
  - target-specific mappings that consume the same canonical tokens

## Practical baseline to use going forward

If you want Helsing to be easy to generate across tools, use this baseline:

- **15-16 canonical tokens** for the shared design system
- **22 total named values** when building a full Dracula-style terminal/ANSI contract
- **target-specific helper tokens** only in implementation files

That gives you a theme system that stays small enough to manage, but structured enough to port cleanly.
