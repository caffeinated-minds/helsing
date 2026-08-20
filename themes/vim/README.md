# Helsing for Vim

This directory contains the Vimscript edition of Helsing. It is deliberately
separate from `themes/neovim`, whose Lua theme includes Neovim, Treesitter, LSP
and plugin-specific highlight groups.

## Install

Copy `helsing.vim` into Vim's colour directory:

```bash
mkdir -p ~/.vim/colors
cp helsing.vim ~/.vim/colors/helsing.vim
```

Then add this to `~/.vimrc`:

```vim
set termguicolors
colorscheme helsing
```

The file was rendered from cortadOS's vendored copy of the canonical Helsing
palette. Future palette changes should update both the Vim and Neovim editions.
