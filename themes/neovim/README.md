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

## Optional Bufferline integration

The colour scheme itself is declarative and does not load, configure or monitor plugins. Static plugin highlight groups are harmless when their plugins are absent.

`bufferline.nvim` creates file-type icon groups at runtime, so Helsing provides an explicit adapter that makes those generated icons inherit the correct inactive, visible and selected tab backgrounds. Copy `lua/helsing/integrations/bufferline.lua` into the equivalent path beneath your Neovim configuration, then apply it from your Bufferline configuration:

```lua
local opts = {}
require("helsing.integrations.bufferline").apply(opts)
require("bufferline").setup(opts)
```

With LazyVim or another lazy.nvim configuration that supplies `opts`, use:

```lua
{
  "akinsho/bufferline.nvim",
  opts = function(_, opts)
    require("helsing.integrations.bufferline").apply(opts)
  end,
}
```

## Development

The canonical colours live in [`docs/helsing-palette.yml`](../../docs/helsing-palette.yml). Neovim-specific helper surfaces and output paths live in [`generator/config/neovim.yml`](../../generator/config/neovim.yml). The main template composes focused editor, language and plugin partials from `generator/templates/neovim/partials/`; the Bufferline adapter has its own template. Do not edit generated Neovim files independently.

After changing the palette, helpers or mappings, regenerate the theme and validate it from the repository root:

```bash
python generator/generate.py neovim
./checks/validate.sh
```

The validation checks that generated targets are current, mappings do not introduce ad-hoc colour literals, the public colour scheme remains declarative, source lines remain readable, highlight groups are not declared twice and both generated Neovim outputs load successfully when Neovim is available.
