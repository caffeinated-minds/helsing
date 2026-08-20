# Helsing for Mintty / Git Bash

`helsing.minttyrc` is a generated Mintty colour scheme. It covers the default
foreground, background, cursor, selection, and all 16 ANSI colours without
changing shell or terminal behaviour.

## Install for one Windows user

From Git Bash, copy the theme into Mintty's per-user theme directory:

```bash
mkdir -p ~/.mintty/themes
cp /path/to/helsing/themes/mintty/helsing.minttyrc ~/.mintty/themes/
```

Then open **Options → Looks**, choose `helsing.minttyrc` from **Theme**, and
select **Save**. Open a new Git Bash window to verify the saved setting.

Alternatively, set this in `~/.minttyrc`:

```ini
ThemeFile=helsing.minttyrc
```

The theme intentionally does not select a font. For the complete Helsing
profile, install Fira Code in Windows and select it under **Options → Text**.
