# Helsing for Waybar

This directory contains Helsing's generated Waybar styling:

- `style.css` styles the bar, workspace buttons and the common modules used by the cortadOS layout.
- `colors.css` exposes the palette as GTK CSS `@define-color` values for use in additional rules.

## Install

Use `style.css` as the stylesheet for a Waybar configuration that provides the corresponding modules. To test it without replacing your current configuration:

```bash
waybar --config ~/.config/waybar/config --style /path/to/helsing/themes/waybar/style.css
```

If you write custom CSS, add this at the top of that stylesheet to use Helsing's named colour definitions:

```css
@import url("colors.css");
```
