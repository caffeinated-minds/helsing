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
