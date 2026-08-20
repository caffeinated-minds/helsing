# Publishing Helsing to the Chrome Web Store

This is the release runbook for publishing the Helsing browser theme to the
Chrome Web Store. Chrome treats a theme as a special extension: it is packaged
and reviewed through the same Developer Dashboard, but it should contain no
JavaScript or HTML.

Last checked against Google's documentation: **2026-08-19**.

## Release model

Keep these identities separate:

- **Source:** `generator/config/chrome.yml` and
  `generator/templates/chrome/manifest.json.j2`
- **Generated package:** `themes/chrome/manifest.json` plus its referenced
  release assets
- **Store listing:** descriptions, screenshots, privacy declarations and
  distribution settings held in the Chrome Web Store Developer Dashboard
- **Store item ID:** the permanent ID assigned when the first ZIP is uploaded

The current unpacked development ID is path-derived. Do not put that ID into
cortadOS. After the Store item exists, record its assigned ID and use that for
future managed installation.

## Current readiness

The current theme already has several useful properties:

- Manifest V3
- a single, narrow purpose
- no JavaScript or HTML
- no permissions or host permissions
- no network requests or user-data handling
- colours generated from the canonical Helsing palette

Complete these items before the first upload:

- [ ] Commission and approve the final Helsing icon.
- [ ] Add at least a 128×128 PNG icon to the package and declare it in the
      generated manifest.
- [ ] Produce the Store screenshots and promotional artwork listed below.
- [ ] Publish the Helsing website, support page and a short privacy statement.
- [ ] Choose the final publisher identity, probably `Caffeinated Minds`.
- [ ] Add a project licence at the repository root.
- [ ] Test the exact release ZIP in current stable Chrome and Brave.

Do not edit `themes/chrome/manifest.json` directly. Add icon metadata or other
manifest changes to the generator config/template, then regenerate it.

## 1. Create the publisher account

1. Choose a long-lived Google account that will own Helsing releases. Google
   recommends an account dedicated to Chrome Web Store publishing because the
   account email cannot later be changed without transferring the items.
2. Enable strong multi-factor authentication and store recovery codes safely.
3. Open the [Chrome Web Store Developer Dashboard][dashboard].
4. Accept the developer agreement and pay the one-time registration fee shown
   by the Dashboard.
5. Set a monitored publisher email address.
6. When the Helsing website is ready, verify it in Google Search Console and
   select it as the official URL in the listing.

The registration fee is intentionally not recorded here because Google can
change it; use the amount displayed by the Dashboard.

## 2. Prepare the release source

1. Start from a clean branch and review all pending changes.
2. Make palette changes in `docs/helsing-palette.yml`, not in generated files.
3. Update the theme version. The Chrome manifest currently gets its version
   from `version` in `docs/helsing-palette.yml`.
4. Ensure the version is one to four dot-separated integers. Every Store update
   must use a version higher than the version already published.
5. Regenerate all targets:

   ```bash
   .venv/bin/python generator/generate.py
   ```

6. Validate the generated manifest:

   ```bash
   python3 -m json.tool themes/chrome/manifest.json >/dev/null
   git diff --check
   git status --short
   ```

7. Confirm that the Chrome package contains only theme resources. It must not
   acquire scripts, permissions, host permissions or remote code.

The manifest should eventually contain an icon entry generated from source,
for example:

```json
"icons": {
  "128": "icons/helsing-128.png"
}
```

The path is relative to the package root, and the file must exist with exactly
the same spelling and case.

## 3. Test the exact theme locally

Test before creating the ZIP:

1. Open `chrome://extensions` or `brave://extensions`.
2. Enable **Developer mode**.
3. Select **Load unpacked**.
4. Choose the `themes/chrome` directory.
5. Check normal and private/incognito windows.

Verify at least:

- active and inactive tabs
- normal and inactive window frames
- toolbar buttons
- address bar text, background and selected suggestions
- bookmark text
- new-tab background, text and links
- readable contrast at 100% and 125% display scaling
- Chrome and Brave on their current stable releases

Do not accept a release merely because the manifest loads. The prediction is
that every declared role is readable in both browsers; the visual checks test
that mental model.

## 4. Build a minimal ZIP

Create a ZIP whose root contains `manifest.json`. Do not zip the enclosing
`chrome` directory, the generator files, this guide, Git metadata or browser
caches such as `Cached Theme.pak`.

With `zip` installed:

```bash
mkdir -p dist
(
  cd themes/chrome
  zip -r ../../dist/helsing-chrome-theme-0.1.0.zip manifest.json icons
)
unzip -l dist/helsing-chrome-theme-0.1.0.zip
```

If `zip` is unavailable in Git Bash, Windows PowerShell can create the same
archive:

```powershell
New-Item -ItemType Directory -Force dist | Out-Null
Push-Location themes/chrome
Compress-Archive -Force -Path manifest.json,icons -DestinationPath ../../dist/helsing-chrome-theme-0.1.0.zip
Pop-Location
```

Use the real release version in the filename. Extract that ZIP into a temporary
directory and repeat the **Load unpacked** test against the extracted contents.
This catches missing files, wrong filename case and accidentally nested ZIPs.

## 5. Create the Store item

1. Open the [Developer Dashboard][dashboard].
2. Select **Add new item**.
3. Upload the release ZIP.
4. Confirm that the Dashboard identifies it as a theme and accepts the
   manifest.
5. Record the assigned Store item ID immediately:

   ```text
   Chrome Web Store item ID: __________________________________
   Draft created:            __________________________________
   Publisher account:        __________________________________
   ```

That Store item ID is the durable identity for Chrome, Brave and later
cortadOS management.

### Optional: align the unpacked development ID

The Dashboard can display the item's public key. Adding that public key to the
generated manifest under the `key` field makes local unpacked builds use the
same ID as the Store item. This is optional for a pure theme, but useful for
testing managed installation.

The public key is not a secret. Add it through the generator and commit it. Do
not create or commit a private signing key; the Chrome Web Store signs and
serves Store packages.

## 6. Complete the Store listing

Use clear, literal language. The listing must describe only what the package
actually does.

Suggested values:

```text
Name: Helsing Theme

Short description:
A disciplined daylight browser theme with paper warmth and semantic restraint.

Detailed description:
Helsing is a light browser theme designed for calm, readable daytime use. It
uses warm paper backgrounds, charcoal text and restrained semantic accents
across tabs, the toolbar, address bar and new-tab page.

Helsing contains no executable code, requests no permissions and does not
collect or transmit user data.
```

Prepare these listing assets and follow the requirements currently shown in
the Dashboard:

- 128×128 store icon
- at least one screenshot; 1280×800 is preferred, with 640×400 also accepted
- up to five screenshots showing the actual theme
- 440×280 small promotional tile
- optional 1400×560 marquee image
- optional demonstration video if it materially improves the listing

For Helsing, useful screenshots would show:

1. a normal browser window with active/inactive tabs and the address bar
2. an incognito/private window
3. a new-tab page and bookmarks bar

Use full-size, current screenshots without excessive text, fake UI, review
badges or claims such as “official”, “best” or “number one”.

Add the eventual Helsing homepage and support URL. A GitHub Issues page can be
the initial support URL if that is where support will genuinely be handled.

## 7. Complete Privacy practices

Use this single-purpose statement:

```text
Helsing changes the colours and appearance of the browser interface.
```

For the current theme package, declare accurately:

- no permissions
- no host permissions
- no remote code
- no user data collected, stored, transmitted, sold or shared

If the Dashboard requests a privacy-policy URL—or simply to make the promise
clear—publish a small page containing language such as:

```text
Helsing Browser Theme does not collect, store, transmit, sell or share personal
data or browsing activity. The package contains no executable code and requests
no browser permissions. It only changes browser interface colours.
```

Update that statement if the product ever changes. Dashboard disclosures, the
privacy page and actual package behaviour must agree.

## 8. Choose distribution and submit

1. Select the intended regions. Use all regions unless there is a real reason
   to restrict distribution.
2. For pre-release testing, use the Dashboard's trusted-tester, private or
   unlisted option that best matches the audience currently offered.
3. For the public launch, select public visibility.
4. Provide test instructions if requested:

   ```text
   No account or credentials are required. Install the theme and inspect the
   browser frame, tabs, toolbar, address bar and new-tab page in a normal and
   an incognito/private window.
   ```

5. Select **Submit for Review**.
6. Prefer deferred publishing for the first release. This allows approval to
   complete before coordinating the website and announcement. An approved
   staged submission must currently be published within 30 days or it returns
   to draft.

Reviews commonly take days and can take weeks. Consult the current review page
for service notices; Google recommends contacting developer support when an
item has remained pending for more than three weeks.

## 9. Validate after publication

- [ ] Install from the public Store page in stable Chrome.
- [ ] Install from the same Store page in stable Brave using **Add to Brave**.
- [ ] Confirm the installed item ID matches the Dashboard ID.
- [ ] Confirm normal restart and browser sync behaviour.
- [ ] Confirm all visual checks from the local test.
- [ ] Add the public Store URL and item ID to `themes/chrome/README.md`.
- [ ] Create and push a signed or annotated Git tag for the exact release.
- [ ] Keep the submitted ZIP so the Store artifact can be traced to source.

Only after these checks should cortadOS replace its local unpacked-theme setup
with a managed Store installation using the permanent item ID.

## 10. Publish an update

1. Make changes in the canonical palette or Chrome generator source.
2. Increase the manifest version.
3. Regenerate and repeat the local and extracted-ZIP tests.
4. Upload a complete new ZIP from the item's **Package** tab.
5. Review listing and privacy metadata for accuracy.
6. Submit the update for review.
7. Test the Store-delivered update after publication.

Never reuse or decrease a published version. If a bad release escapes, prepare
a corrected package with a higher version and use the Dashboard's supported
rollback or update flow; do not try to replace Store state manually.

## Automation boundary

Do the first release manually. It exposes every piece of Store-owned state and
makes the review contract understandable. Consider the Chrome Web Store API
only after repeated releases make manual upload a genuine source of risk or
friction. Do not store publisher credentials or access tokens in this repo.

## Official references

- [Chrome themes][theme-docs]
- [Register a developer account][register]
- [Publish in the Chrome Web Store][publish]
- [Complete the Store listing][listing]
- [Create a strong listing][best-listing]
- [Complete Privacy practices][privacy]
- [Chrome Web Store review process][review]
- [Update an existing item][update]
- [Keep a consistent development ID][manifest-key]

[dashboard]: https://chrome.google.com/webstore/devconsole
[theme-docs]: https://developer.chrome.com/docs/extensions/develop/ui/themes
[register]: https://developer.chrome.com/docs/webstore/register
[publish]: https://developer.chrome.com/docs/webstore/publish
[listing]: https://developer.chrome.com/docs/webstore/cws-dashboard-listing
[best-listing]: https://developer.chrome.com/docs/webstore/best-listing
[privacy]: https://developer.chrome.com/docs/webstore/cws-dashboard-privacy
[review]: https://developer.chrome.com/docs/webstore/review-process
[update]: https://developer.chrome.com/docs/webstore/update
[manifest-key]: https://developer.chrome.com/docs/extensions/reference/manifest/key
