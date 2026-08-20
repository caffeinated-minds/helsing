# Helsing Theme for VS Code

Helsing is a disciplined light theme built around paper warmth, restrained accents and stable semantic colour roles.

Named for **Abraham Van Helsing**, the scholar, physician and adversary of Dracula, Helsing is conceived as a daylight counterpoint to themes drawn toward the night. Where those themes find character in deep shadow and supernatural colour, Helsing works with warm paper, graphite text and carefully rationed accents.

[Dracula describes itself](https://draculatheme.com/), with admirable modesty, as "the most famous theme ever created and available everywhere." Fair enough. Every famous vampire eventually needs a Van Helsing.

This theme then is the daylight counter Dracula Theme always needed: less crypt, more study; less neon at midnight, more ink on paper.

**Helsing is an independent theme, not a fork, port or official Dracula companion.**

![Helsing Theme in the VS Code workbench](images/helsing-vscode-hero.png)

This is not darkness inverted into glare. Helsing is designed to remain calm during long working sessions: structure comes from measured contrast, and colour is used to communicate meaning rather than decorate every token. The result is a theme with an old-world scholarly character and a modern, workmanlike interface.

## Design

- Warm paper backgrounds instead of pure white
- Dark graphite text instead of pure black
- Consistent semantic colours for code, diagnostics and source control
- TextMate and semantic-token coverage
- A composed daylight identity rather than a conventional high-glare light theme
- No runtime code, telemetry or network access

Helsing changes VS Code's colours only. It does not install or select an editor font, so users remain in control of their typography.

## Language previews

The same restrained semantic palette carries across different language grammars and language-server token sets.

These screenshots use **Go Mono**, installed as `GoMono Nerd Font`. Helsing itself changes colours only and does not install or select an editor font.

### Go

![Helsing displaying Go source code](images/screenshot.png)

### Python

![Helsing displaying Python source code](images/helsing-python.png)

### TypeScript

![Helsing displaying TypeScript source code](images/helsing-typescript.png)

### C

![Helsing displaying C source code](images/helsing-c.png)

### Bash

![Helsing displaying Bash source code](images/helsing-bash.png)

### CSS

![Helsing displaying CSS source code](images/helsing-css.png)

### HTML

![Helsing displaying HTML source code](images/helsing-html.png)

## Install and activate

After installing the extension:

1. Open the Command Palette with `Ctrl+Shift+P` or `Cmd+Shift+P`.
2. Run **Preferences: Color Theme**.
3. Select **Helsing**.

## Feedback

Report inconsistent colours or missing language coverage through the [Helsing issue tracker](https://github.com/caffeinated-minds/helsing/issues). When reporting syntax highlighting, include the language, the relevant source sample and a screenshot.

## Development

The published theme is generated from Helsing's palette contract rather than edited directly:

- Palette: `docs/helsing-palette.yml`
- VS Code mapping: `generator/config/vscode.yml`
- Template: `generator/templates/vscode/helsing-color-theme.json.j2`
- Generated payload: `themes/vscode/themes/helsing-color-theme.json`

Open this directory as the VS Code workspace and press `F5` to launch the **Run Helsing Theme** Extension Development Host configuration.

To regenerate and package from this directory:

```bash
npm ci
npm run theme:generate
npm run package:vsix
```

## License

Helsing Theme is available under the [MIT License](LICENSE).
