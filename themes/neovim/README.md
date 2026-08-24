# Helsing for Neovim

`helsing.lua` is Helsing's generated Neovim colour scheme. It covers core editor groups, diagnostics, LSP semantic tokens, Tree-sitter captures and common plugin interfaces.

## Install

1. Copy `helsing.lua` to `~/.config/nvim/colors/helsing.lua`.
2. Add the following after your plugin manager and colour settings are loaded:

```lua
vim.opt.termguicolors = true
vim.cmd.colorscheme("helsing")
```

3. Restart Neovim or run `:colorscheme helsing`.

Tree-sitter Markdown captures receive Helsing's six-level heading hierarchy when the Markdown parsers are installed. Vim-compatible Markdown highlight groups remain as fallbacks.

## Development

The canonical colours live in [`docs/helsing-palette.yml`](../../docs/helsing-palette.yml). Neovim-specific helper surfaces live in [`generator/config/neovim.yml`](../../generator/config/neovim.yml), and highlight mappings belong in [`generator/templates/neovim/helsing.lua.j2`](../../generator/templates/neovim/helsing.lua.j2). Do not edit the generated `helsing.lua` independently.

After changing the palette, helpers or mappings, regenerate the theme and validate it from the repository root:

```bash
python generator/generate.py neovim
./checks/validate.sh
```

The validation checks that generated targets are current, Neovim mappings do not introduce ad-hoc colour literals, highlight groups are not declared twice and the generated theme loads successfully when Neovim is available.
