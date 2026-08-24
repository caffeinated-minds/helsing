# Helsing Theme — Chrome Web Store listing worksheet

Use this document while completing the Chrome Web Store Developer Dashboard. Everything below describes the currently prepared `0.1.1` release. Do not upload a new package until its version is higher than the version already published.

## Release upload

- **ZIP to upload:** `dist/helsing-chrome-theme-0.1.1.zip`
- **Manifest name:** `Helsing Theme`
- **Manifest version:** `0.1.1`
- **Package purpose:** a browser theme only; it contains no JavaScript, HTML, permissions, host permissions, network requests, or user-data handling.

The ZIP root contains `manifest.json`, as required by the Store.

## Store listing

### Product details

- **Name:** Helsing Theme
- **Language:** English (United Kingdom)
- **Category:** Select the closest available theme/appearance category in the Dashboard.
- **Short description:**

  ```text
  A disciplined daylight browser theme with paper warmth and semantic restraint.
  ```

- **Detailed description:**

  ```text
  Helsing is a light browser theme designed for calm, readable daytime use. It uses warm paper backgrounds, charcoal text and restrained semantic accents across tabs, the toolbar, address bar and new-tab page.

  Helsing contains no executable code, requests no permissions and does not collect or transmit user data.
  ```

### Listing artwork

Upload these files from the repository:

- **Store icon (128×128):** `themes/chrome/icons/helsing-128.png`
- **Screenshot (1280×800):** `themes/chrome/images/listing/helsing-chrome-store-1280x800.png`
- **Small promotional tile (440×280):** `themes/chrome/images/listing/helsing-chrome-promo-tile-440x280.png`
- **Marquee (1400×560):** leave blank for this first release unless a dedicated artwork asset is prepared.
- **Promo video:** leave blank; Helsing is a visual theme and the screenshot demonstrates its function directly.

### Links and support

- **Homepage URL:** `https://github.com/caffeinated-minds/helsing`
- **Support URL:** `https://github.com/caffeinated-minds/helsing/issues`
- **Official URL / verified publisher URL:** leave blank until the Helsing website exists and is verified in Google Search Console.

### Privacy practices

Choose the answers consistent with this package:

- **Single purpose:** Helsing changes the colours and appearance of the browser interface.
- **Permissions:** none.
- **Host permissions:** none.
- **Remote code:** none.
- **User data collected, stored, transmitted, sold, or shared:** none.
- **Privacy policy URL:** use the project website when one exists. If the Dashboard permits submission without one for this no-data theme, leave it blank rather than linking to an inaccurate placeholder.

If a free-text declaration is requested, paste:

```text
Helsing Browser Theme does not collect, store, transmit, sell or share personal data or browsing activity. The package contains no executable code and requests no browser permissions. It only changes browser interface colours.
```

### Distribution and submission

- **Visibility:** Public, when the listing and support links are ready.
- **Regions:** All regions.
- **Mature content:** No.
- **Test instructions (if requested):**

  ```text
  No account or credentials are required. Install the theme and inspect the browser frame, tabs, toolbar, address bar and new-tab page in a normal and an incognito/private window.
  ```

- **Publishing choice:** Prefer deferred publishing for the first release, if the Dashboard offers it. This lets review complete before making the listing public.

## After first upload

Record these values here or in the release issue:

- **Chrome Web Store item ID:**
- **Store listing URL:**
- **Publisher account:**
- **Draft/submission date:**
- **Review decision date:**

Then install the Store-delivered theme in Chrome and Brave, confirm the item ID and visual behaviour, commit the release assets, and tag the exact source revision.
