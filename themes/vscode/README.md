# Helsing Theme for VS Code

Helsing is a light theme built around paper warmth, restrained accents, and stable semantic color roles.

## Local development

From this folder, you can open the extension in VS Code and run the `Run Extension` launch target.

The theme payload lives at `themes/helsing-color-theme.json` and is generated from the repo palette contract.

## Packaging

This scaffold uses the current VS Code extension packaging tool, `@vscode/vsce`, as a local dev dependency.

Requirements:

- Node.js 20+
- repo `.venv` with the generator dependencies installed

From this folder:

```bash
npm install
npm run package:vsix
```

That produces a `.vsix` file in this directory.

To publish to the Marketplace:

```bash
export VSCE_PAT=your_pat_here
npm run publish:marketplace
```

## Regenerating the theme

From the repo root:

```bash
.venv/bin/python generator/generate.py
```

Or from this extension folder:

```bash
npm run theme:generate
```
