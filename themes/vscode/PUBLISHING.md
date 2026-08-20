# Publishing Helsing to the VS Code Marketplace

This is the maintainer runbook for preparing, testing and publishing the
Helsing colour-theme extension.

## Release model

Keep these layers distinct:

```text
docs/helsing-palette.yml
        +
generator/config/vscode.yml
        +
generator/templates/vscode/helsing-color-theme.json.j2
        |
        v
themes/vscode/themes/helsing-color-theme.json
        +
themes/vscode/package.json and Marketplace documentation
        |
        v
helsing-theme-<version>.vsix
        |
        v
Visual Studio Marketplace item
```

The palette, target mapping and template are source. The colour-theme JSON is
a generated, version-controlled artifact. The VSIX is the exact release
artifact. The Marketplace owns publisher identity, install statistics, reviews
and the public extension page.

## Current identity

The manifest currently proposes:

- Publisher ID: `caffeinatedminds`
- Extension name: `helsing-theme`
- Extension ID: `caffeinatedminds.helsing-theme`
- Display name: `Helsing Theme`
- Initial version: `0.1.0`
- Minimum VS Code version: `1.85.0`

Before the first upload, confirm that the `caffeinatedminds` publisher exists
in the account that will own Helsing. A publisher ID cannot be changed after it
is created. Also search the Marketplace to confirm that the extension name and
display name are available.

## First-release blockers

Do not publish until all of these are resolved:

- [ ] Confirm or create the `caffeinatedminds` Marketplace publisher.
- [ ] Choose the project licence and add it to the repository and extension.
- [ ] Obtain the final artist-created extension icon.
- [ ] Add at least one clean Marketplace screenshot.
- [ ] Review the Marketplace README as public-facing copy.
- [ ] Test the packaged VSIX on stable VS Code.
- [ ] Test representative source files and all important UI states.
- [ ] Commit, push and tag the exact source used to build the VSIX.

The licence and icon are deliberately not invented in this repository. They
are ownership and brand decisions, not packaging defaults.

## 1. Finish the visual assets

### Extension icon

Ask the artist for a square PNG. Use 256 by 256 pixels so it also looks crisp
on high-density screens; Microsoft requires at least 128 by 128 pixels.

Place it at:

```text
themes/vscode/images/icon.png
```

Then add `"images"` to the `files` array and this field to `package.json`:

```json
"icon": "images/icon.png"
```

Do not use an SVG icon. `vsce` rejects user-provided SVG images for security
reasons.

### Screenshot

Capture a clean editor window using Helsing with no personal data, tokens,
hostnames or private repositories visible. A useful first screenshot shows:

- Explorer, Activity Bar, tabs, editor and Status Bar
- a representative language with comments, strings, numbers, functions and
  types
- one diagnostic and a Git diff or source-control state if practical
- enough contrast to judge selections, line numbers and the current line

Store the primary screenshot as `themes/vscode/images/screenshot.png`. Add
`"images"` to the
manifest's `files` array and reference the screenshot from `README.md` using a
relative Markdown link. The manifest's `vsce.baseContentUrl` and
`vsce.baseImagesUrl` point link rewriting at this extension's monorepo
directory. Verify those rendered links in the packaged README before
publishing; the repository must already contain the referenced commit.

Images referenced by `README.md` and `CHANGELOG.md` must resolve through HTTPS.
Avoid SVG screenshots.

## 2. Choose and record a licence

The repository currently has no Helsing project licence. Choose one before
public release; do not copy the licence from a dependency or template without
confirming that it expresses the intended terms for Helsing.

After choosing it:

1. Add the licence as `themes/vscode/LICENSE`. A root project licence may also
   apply, but the extension needs its own packaged copy for the Marketplace.
2. Add `"LICENSE"` to the manifest's `files` array.
3. Add one of the following manifest forms:

   ```json
   "license": "MIT"
   ```

   or:

   ```json
   "license": "SEE LICENSE IN LICENSE"
   ```

4. Add a short Licence section to the public README.

## 3. Create the publisher

Use the [Visual Studio Marketplace publisher management page][publisher-page].
Sign in with a durable Microsoft account controlled by the project owner.

Create a publisher only after confirming its permanent ID. The publisher's
display name can represent the brand, but its ID becomes part of every
extension identifier and public URL.

Do not put a Personal Access Token, Microsoft credential or exported login
state in this repository.

## 4. Prepare the development environment

Current `@vscode/vsce` requires Node.js 22 or newer. From the repository root,
prepare the Python generator once:

```bash
python3 -m venv .venv
.venv/bin/pip install -r generator/requirements.txt
```

Then install the locked Node dependencies:

```bash
cd themes/vscode
npm ci
```

Commit `package-lock.json`; do not commit `node_modules/`.

## 5. Generate and inspect the source artifact

Change colours in the canonical palette or VS Code generator mapping, never in
the generated JSON alone.

From `themes/vscode`:

```bash
npm run theme:generate
```

Inspect the generated diff:

```bash
git diff -- themes/vscode/themes/helsing-color-theme.json
```

If no colour change was intended, that command should print nothing. Confirm
that the palette and extension manifest versions agree before a release:

```bash
grep '^version:' ../../docs/helsing-palette.yml
grep '"version"' package.json
```

## 6. Test the theme in an Extension Development Host

Open `themes/vscode` as the VS Code workspace and press `F5`. Select **Helsing**
in the development window.

Test at least:

- JavaScript or TypeScript
- Go
- Python
- Bash
- JSON and YAML
- Markdown
- Dockerfile
- Terraform or HCL if it is part of the expected audience

For each language, inspect comments, strings, numbers, keywords, functions,
types, constants, parameters and invalid syntax. Use **Developer: Inspect
Editor Tokens and Scopes** when a token has the wrong colour; it shows whether
the source is a TextMate scope or a semantic token.

Also exercise:

- [ ] active and inactive tabs
- [ ] selections, search matches and bracket matching
- [ ] Command Palette and suggestion widgets
- [ ] hover and peek views
- [ ] warnings, errors, hints and information diagnostics
- [ ] Git added, modified and deleted decorations
- [ ] sidebars, panels and the integrated terminal
- [ ] diff editors
- [ ] empty, no-folder and remote windows

Prediction: because Helsing has no executable extension code, failures should
be visual mapping errors or packaging errors, not activation or runtime
failures. If the extension host reports runtime activation, investigate why;
that is outside the intended package boundary.

## 7. Build and inspect the VSIX

From `themes/vscode`:

```bash
npm run check:release
npm run check:contents
npm run package:vsix
```

`check:release` deliberately fails if the licence, icon, screenshot, manifest
metadata or version alignment is unfinished. `check:contents` shows exactly
what `vsce` intends to include. The resulting
file should be named like `helsing-theme-0.1.0.vsix`.

Check that it contains only the manifest, README, changelog, licence, images
and generated theme payload. It must not contain:

- `node_modules`
- source credentials
- `.git` or local editor state
- Python caches or virtual environments
- generator internals
- previous VSIX files

Install the exact VSIX that will be uploaded:

```bash
code --install-extension helsing-theme-0.1.0.vsix --force
```

Restart VS Code, select Helsing and repeat the core smoke test. This
distinguishes “works from the source tree” from “the published package contains
everything it needs.”

## 8. Publish the first release manually

For the first release, prefer a manual VSIX upload through the
[publisher management page][publisher-page]:

1. Build and test the final VSIX.
2. Sign in to the publisher management page.
3. Select the intended publisher.
4. Choose **New extension** and **Visual Studio Code**.
5. Upload the tested VSIX.
6. Inspect the rendered README, icon, banner, links, category and version.
7. Complete the publication.

This path keeps credentials out of local files and Git. It is also easier to
audit: the file tested locally is the file uploaded.

Microsoft currently still documents PAT-based `vsce publish`, but global Azure
DevOps PATs retire on 1 December 2026. If releases later become frequent,
implement Microsoft Entra ID workload-identity publishing rather than building
new long-lived PAT automation.

## 9. Validate the public release

- [ ] Install `caffeinatedminds.helsing-theme` from a clean stable VS Code.
- [ ] Confirm the publisher, name, version and repository links.
- [ ] Confirm the README images render over HTTPS.
- [ ] Select Helsing and repeat the smoke test.
- [ ] Confirm the extension installs in VS Code for the Web.
- [ ] Record the Marketplace URL in this README and the project website.
- [ ] Preserve the uploaded VSIX as a release artifact.
- [ ] Create a signed or annotated Git tag for the released version.

## 10. Publish an update

1. Change the palette or VS Code generator source.
2. Increase the SemVer version in both the palette and extension manifest.
3. Update `CHANGELOG.md`.
4. Regenerate, test and package.
5. Install and test the exact new VSIX.
6. Upload it to the existing Marketplace item.
7. Validate the Store-delivered update.

Never reuse a published version number. Avoid removing an extension unless the
loss of its identity and statistics is genuinely intended; Microsoft documents
removal as irreversible and the extension name remains reserved.

## Official references

- [VS Code colour-theme guide][theme-guide]
- [Extension manifest reference][manifest]
- [Publishing extensions and packaging VSIX files][publishing]
- [Marketplace presentation tips][presentation]
- [`@vscode/vsce` package][vsce]

[publisher-page]: https://marketplace.visualstudio.com/manage/publishers/
[theme-guide]: https://code.visualstudio.com/api/extension-guides/color-theme
[manifest]: https://code.visualstudio.com/api/references/extension-manifest
[publishing]: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
[presentation]: https://code.visualstudio.com/api/working-with-extensions/publishing-extension#marketplace-integration
[vsce]: https://www.npmjs.com/package/@vscode/vsce
