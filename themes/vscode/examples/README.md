# Helsing VS Code fixtures

These small, self-contained fixtures exercise common syntax and semantic-token roles without exposing personal projects or machine details. They support scope inspection and regression review as well as Marketplace screenshots.

The set covers Python, Go, Bash, JavaScript, TypeScript, React/TSX, C, CSS, HTML, JSON, YAML, and TOML. Expected source text, Helsing roles, TextMate scopes, and semantic tokens are recorded in `generator/config/vscode-fixtures.yml`; the generated test contract is `checks/generated/helsing-vscode-token-contract.json`.

## Inspect a token

1. Open the repository in VS Code and select the Helsing theme.
2. Open a fixture and place the cursor on the token being checked.
3. Run **Developer: Inspect Editor Tokens and Scopes** from the Command Palette.
4. Compare the TextMate scopes, semantic token and winning rule with `generator/config/vscode-fixtures.yml`.
5. Repeat with `"editor.semanticHighlighting.enabled": false` in workspace settings to verify the TextMate fallback, then remove the setting or change it to `true` and verify the semantic path.

If observed data differs, update the manifest only after deciding whether the grammar or semantic provider changed, or whether the Helsing mapping is wrong. The extension supplies colours; the installed grammar and language extension supply the classifications. When a grammar lacks enough information to express the intended semantic role, record the honest `textmate_role` or `semantic_role` fallback and explain it with `fallback_reason` rather than forcing a misleading scope rule.

## Validate

From `themes/vscode`:

```bash
npm run theme:check
```

This validates the source contract and generated artifacts and confirms that each recorded token still exists in its fixture. It cannot replace the interactive inspector when VS Code, a bundled grammar, or a language extension changes.

## Capture screenshots

Open this directory as a VS Code workspace, select the Helsing theme and capture one language at a time with the Explorer, Activity Bar, tabs and Status Bar visible.

The examples form a fictional daylight watch system and are not shipped in the VSIX package.
