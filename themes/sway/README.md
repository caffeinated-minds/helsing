# Helsing for Sway

`config` is Helsing's generated Sway configuration. It includes visual settings as well as keybindings, startup commands, input configuration and application choices; it is therefore a complete personal starting point, not a small drop-in colour fragment.

## Use safely

Read the configuration before using it. In particular, adapt the terminal, launcher, browser, keyboard, startup services, wallpaper and any machine-specific outputs to your own system.

For a non-destructive review, validate a copy before loading it:

```bash
sway -C -c /path/to/helsing/config
```

After integrating the relevant sections into your own configuration, reload Sway with `swaymsg reload`. Do not overwrite a working Sway configuration without keeping a recoverable copy.

## Development
