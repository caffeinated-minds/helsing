# Helsing for WezTerm

`helsing.toml` is Helsing's generated WezTerm colour scheme. It covers terminal colours, cursor and selection colours, tab bar surfaces, quick-select labels and the ANSI palette. It does not choose a font, keybindings or shell.

## Install

1. Create WezTerm's user colour-scheme directory:

```bash
mkdir -p ~/.config/wezterm/colors
```

2. Copy `helsing.toml` there as `~/.config/wezterm/colors/helsing.toml`.
3. In `~/.config/wezterm/wezterm.lua`, select the scheme:

```lua
config.color_scheme = "Helsing"
```

4. Restart WezTerm or reload its configuration.
