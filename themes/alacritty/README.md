# Helsing for Alacritty

`helsing.toml` is Helsing's generated Alacritty colour theme. It sets terminal surfaces, cursor and selection colours, search colours, and the complete ANSI palette. It does not select a font or change terminal behaviour.

## Install

1. Copy `helsing.toml` somewhere stable, for example `~/.config/alacritty/themes/helsing.toml`.
2. Add an import to your main `alacritty.toml`, replacing the example path with your real path:

```toml
[general]
import = ["/home/you/.config/alacritty/themes/helsing.toml"]
```

3. Restart Alacritty.

Keep colour settings in the imported theme rather than duplicating them in the main configuration, since the main file can override imported values.

## Development
