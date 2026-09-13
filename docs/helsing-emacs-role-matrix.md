# Helsing Emacs Role Matrix

This file is generated from `docs/helsing-palette.yml` and `generator/config/doom-emacs.yml`. Do not edit it by hand.

The matrix records semantic intent. It does not imply that every face is active in every buffer. The active major mode, Font Lock rules, Tree-sitter queries, Eglot server capabilities, package faces, and overlays determine which face Emacs actually applies.

## Role aliases

| Doom alias | Helsing role | Palette token | Colour |
| --- | --- | --- | --- |
| `builtin` | `pink` | `pink` | `#C05A8C` |
| `comments` | `text_muted` | `muted` | `#6B6B6B` |
| `doc-comments` | `chrome` | `subtle` | `#A8A29E` |
| `constants` | `constant` | `pink` | `#C05A8C` |
| `functions` | `function` | `blue` | `#3A7BD5` |
| `keywords` | `keyword` | `purple` | `#7C6EE6` |
| `methods` | `function` | `blue` | `#3A7BD5` |
| `operators` | `operator` | `purple` | `#7C6EE6` |
| `type` | `type` | `cyan` | `#2F8F8B` |
| `strings` | `string` | `green` | `#4C9A5F` |
| `variables` | `variable` | `fg` | `#2A2A2A` |
| `numbers` | `number` | `orange` | `#C47A2C` |
| `region` | `selection` | `selection` | `#E6DCC8` |
| `error` | `error` | `red` | `#C23B3B` |
| `warning` | `warning` | `yellow` | `#B58900` |
| `success` | `green` | `green` | `#4C9A5F` |
| `vc-modified` | `orange` | `orange` | `#C47A2C` |
| `vc-added` | `green` | `green` | `#4C9A5F` |
| `vc-deleted` | `red` | `red` | `#C23B3B` |

## Face contract

### Core

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `default` | `text` → `fg` (`#2A2A2A`) | `background` → `bg` (`#F4F1EA`) | None | Main editor surface and ordinary text. |
| `cursor` | Inherited | `text` → `fg` (`#2A2A2A`) | None | High-contrast insertion point. |
| `region` | Inherited | `selection` → `selection` (`#E6DCC8`) | None | Selected text; foreground inherits from the buffer. |
| `line-number` | `chrome` → `subtle` (`#A8A29E`) | Inherited | None | Inactive line numbers. |
| `line-number-current-line` | `text` → `fg` (`#2A2A2A`) | Inherited | None | Current line number. |

### Font Lock

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `font-lock-builtin-face` | `builtin_function` → `blue` (`#3A7BD5`) | Inherited | None | Language-provided functions and constructs. |
| `font-lock-comment-face` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Comments. |
| `font-lock-constant-face` | `constant` → `pink` (`#C05A8C`) | Inherited | None | Constants and enum-like values. |
| `font-lock-doc-face` | `chrome` → `subtle` (`#A8A29E`) | Inherited | None | Documentation comments and docstrings when distinguished. |
| `font-lock-function-name-face` | `function` → `blue` (`#3A7BD5`) | Inherited | None | Function names in definitions. |
| `font-lock-function-call-face` | `function` → `blue` (`#3A7BD5`) | Inherited | None | Function names at call sites when distinguished. |
| `font-lock-keyword-face` | `keyword` → `purple` (`#7C6EE6`) | Inherited | None | Control and declaration keywords, including Python def. |
| `font-lock-number-face` | `number` → `orange` (`#C47A2C`) | Inherited | None | Numeric literals. |
| `font-lock-operator-face` | `operator` → `purple` (`#7C6EE6`) | Inherited | None | Operators. |
| `font-lock-preprocessor-face` | `constant` → `pink` (`#C05A8C`) | Inherited | None | Preprocessor directives and macros. |
| `font-lock-property-name-face` | `property` → `fg` (`#2A2A2A`) | Inherited | None | Property names when distinguished. |
| `font-lock-property-use-face` | `property` → `fg` (`#2A2A2A`) | Inherited | None | Property use sites when distinguished. |
| `font-lock-punctuation-face` | `punctuation` → `subtle` (`#A8A29E`) | Inherited | None | Punctuation and delimiters when distinguished. |
| `font-lock-string-face` | `string` → `green` (`#4C9A5F`) | Inherited | None | String literals. |
| `font-lock-type-face` | `type` → `cyan` (`#2F8F8B`) | Inherited | None | Types and class-like identifiers. |
| `font-lock-variable-name-face` | `variable` → `fg` (`#2A2A2A`) | Inherited | None | Variable declarations and names. |
| `font-lock-variable-use-face` | `variable` → `fg` (`#2A2A2A`) | Inherited | None | Variable use sites when distinguished. |

### Eglot

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `eglot-highlight-symbol-face` | Inherited | `selection` → `selection` (`#E6DCC8`) | None | References highlighted by Eglot. |
| `eglot-diagnostic-tag-unnecessary-face` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Code marked unnecessary by the language server. |
| `eglot-diagnostic-tag-deprecated-face` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Code marked deprecated by the language server. |
| `eglot-inlay-hint-face` | `chrome` → `subtle` (`#A8A29E`) | Inherited | None | Base face for unobtrusive inlay hints. |
| `eglot-type-hint-face` | Inherited | Inherited | `eglot-inlay-hint-face` | Type inlay hints inherit the restrained hint role. |
| `eglot-parameter-hint-face` | Inherited | Inherited | `eglot-inlay-hint-face` | Parameter inlay hints inherit the restrained hint role. |

### Editor Chrome

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `mode-line` | `text` → `fg` (`#2A2A2A`) | `modeline_bg` → `modeline_bg` (`#EAE5DC`) | None | Active modeline. |
| `mode-line-inactive` | `text_muted` → `muted` (`#6B6B6B`) | `modeline_bg_inactive` → `modeline_bg_inactive` (`#D6D0C4`) | None | Inactive modeline. |
| `mode-line-emphasis` | `function` → `blue` (`#3A7BD5`) | Inherited | None | Emphasised modeline content. |
| `doom-modeline-bar` | Inherited | `function` → `blue` (`#3A7BD5`) | None | Active Doom modeline indicator. |
| `doom-modeline-bar-inactive` | Inherited | `border` → `border` (`#D6D0C4`) | None | Inactive Doom modeline indicator. |

### Corfu

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `corfu-default` | `text` → `fg` (`#2A2A2A`) | `popup_bg` → `popup_bg` (`#EAE5DC`) | None | Completion popup surface. |
| `corfu-current` | `text` → `fg` (`#2A2A2A`) | `popup_selection` → `popup_selection` (`#E6DCC8`) | None | Selected completion candidate. |
| `corfu-border` | Inherited | `border` → `border` (`#D6D0C4`) | None | Completion popup border. |
| `corfu-annotations` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Completion annotations. |
| `corfu-deprecated` | `error` → `red` (`#C23B3B`) | Inherited | None | Deprecated completion candidate. |
| `corfu-bar` | Inherited | `function` → `blue` (`#3A7BD5`) | None | Completion scrollbar. |

### Completion

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `vertico-current` | `text` → `fg` (`#2A2A2A`) | `popup_selection` → `popup_selection` (`#E6DCC8`) | None | Current Vertico candidate. |
| `orderless-match-face-0` | `function` → `blue` (`#3A7BD5`) | Inherited | None | First Orderless match component. |
| `orderless-match-face-1` | `keyword` → `purple` (`#7C6EE6`) | Inherited | None | Second Orderless match component. |
| `orderless-match-face-2` | `string` → `green` (`#4C9A5F`) | Inherited | None | Third Orderless match component. |
| `orderless-match-face-3` | `warning` → `yellow` (`#B58900`) | Inherited | None | Fourth Orderless match component. |
| `marginalia-documentation` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Marginalia documentation. |
| `marginalia-file-name` | `text` → `fg` (`#2A2A2A`) | Inherited | None | Marginalia file names. |
| `marginalia-size` | `chrome` → `subtle` (`#A8A29E`) | Inherited | None | Marginalia sizes and secondary measurements. |
| `marginalia-modified` | `orange` → `orange` (`#C47A2C`) | Inherited | None | Marginalia modified state. |

### Dashboard

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `dashboard-heading` | `keyword` → `purple` (`#7C6EE6`) | Inherited | None | Dashboard section headings. |
| `dashboard-items-face` | `text` → `fg` (`#2A2A2A`) | Inherited | None | Dashboard items. |
| `dashboard-no-items-message` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Dashboard empty state. |
| `dashboard-banner-logo-title` | `function` → `blue` (`#3A7BD5`) | Inherited | None | Dashboard title. |
| `dashboard-footer` | `chrome` → `subtle` (`#A8A29E`) | Inherited | None | Dashboard footer. |

### Magit Transient

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `magit-section-heading` | `function` → `blue` (`#3A7BD5`) | Inherited | None | Magit section heading. |
| `magit-section-heading-selection` | `orange` → `orange` (`#C47A2C`) | Inherited | None | Selected Magit section heading. |
| `magit-section-highlight` | Inherited | Inherited | `hl-line` | Highlighted Magit section. |
| `magit-diff-added` | `green` → `green` (`#4C9A5F`) | `diff_add_bg` → `diff_add_bg` (`#DCEEDB`) | None | Added diff line. |
| `magit-diff-added-highlight` | `green` → `green` (`#4C9A5F`) | `diff_add_bg` → `diff_add_bg` (`#DCEEDB`) | None | Selected added diff line. |
| `magit-diff-removed` | `red` → `red` (`#C23B3B`) | `diff_delete_bg` → `diff_delete_bg` (`#F3D9D9`) | None | Removed diff line. |
| `magit-diff-removed-highlight` | `red` → `red` (`#C23B3B`) | `diff_delete_bg` → `diff_delete_bg` (`#F3D9D9`) | None | Selected removed diff line. |
| `magit-diff-context-highlight` | `text` → `fg` (`#2A2A2A`) | `surface` → `bg_alt` (`#EAE5DC`) | None | Highlighted unchanged diff context. |
| `magit-diff-hunk-heading` | `keyword` → `purple` (`#7C6EE6`) | `diff_change_bg` → `diff_change_bg` (`#E8E1F3`) | None | Diff hunk heading. |
| `magit-diff-hunk-heading-highlight` | `background` → `bg` (`#F4F1EA`) | `keyword` → `purple` (`#7C6EE6`) | None | Selected diff hunk heading. |
| `magit-header-line` | `text` → `fg` (`#2A2A2A`) | `selection` → `selection` (`#E6DCC8`) | None | Magit header line. |
| `magit-dimmed` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Dimmed Magit content. |
| `transient-heading` | `keyword` → `purple` (`#7C6EE6`) | Inherited | None | Transient section heading. |
| `transient-key` | `function` → `blue` (`#3A7BD5`) | Inherited | None | Transient command key. |
| `transient-value` | `string` → `green` (`#4C9A5F`) | Inherited | None | Transient argument value. |
| `transient-inactive-argument` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Inactive Transient argument. |
| `transient-inactive-value` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Inactive Transient value. |

### Diagnostics

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `hl-line` | Inherited | `surface` → `bg_alt` (`#EAE5DC`) | None | Current line surface. |
| `hl-todo` | `error` → `red` (`#C23B3B`) | Inherited | None | TODO-style attention marker. |
| `whitespace-trailing` | Inherited | `diff_delete_bg` → `diff_delete_bg` (`#F3D9D9`) | None | Trailing whitespace warning. |
| `whitespace-tab` | Inherited | `base0` → `base0` (`#FBF9F4`) | None | Visible tab background. |
| `whitespace-indentation` | Inherited | `base0` → `base0` (`#FBF9F4`) | None | Visible indentation background. |

### Org Markdown

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `org-block` | Inherited | `base2` → `base2` (`#EAE5DC`) | None | Org source block. |
| `org-block-begin-line` | `text_muted` → `muted` (`#6B6B6B`) | `base2` → `base2` (`#EAE5DC`) | None | Org source block opening line. |
| `org-block-end-line` | `text_muted` → `muted` (`#6B6B6B`) | `base2` → `base2` (`#EAE5DC`) | None | Org source block closing line. |
| `org-code` | `orange` → `orange` (`#C47A2C`) | Inherited | None | Inline Org code. |
| `org-link` | `function` → `blue` (`#3A7BD5`) | Inherited | None | Org link. |
| `org-todo` | `green` → `green` (`#4C9A5F`) | Inherited | None | Open Org task. |
| `org-done` | `text_muted` → `muted` (`#6B6B6B`) | Inherited | None | Completed Org task. |
| `markdown-header-face` | `keyword` → `purple` (`#7C6EE6`) | Inherited | None | Markdown heading. |
| `markdown-markup-face` | `chrome` → `subtle` (`#A8A29E`) | Inherited | None | Markdown markup punctuation. |
| `markdown-code-face` | Inherited | `base2` → `base2` (`#EAE5DC`) | None | Markdown code. |

### Dired Evil Vc

| Emacs face | Foreground role | Background role | Inherits | Notes |
| --- | --- | --- | --- | --- |
| `dired-directory` | `function` → `blue` (`#3A7BD5`) | Inherited | None | Dired directory name. |
| `dired-symlink` | `type` → `cyan` (`#2F8F8B`) | Inherited | None | Dired symbolic link. |
| `evil-ex-lazy-highlight` | Inherited | Inherited | `lazy-highlight` | Evil Ex secondary match. |
| `diff-added` | `green` → `green` (`#4C9A5F`) | `diff_add_bg` → `diff_add_bg` (`#DCEEDB`) | None | Added line in Diff mode. |
| `diff-removed` | `red` → `red` (`#C23B3B`) | `diff_delete_bg` → `diff_delete_bg` (`#F3D9D9`) | None | Removed line in Diff mode. |
| `diff-changed` | `keyword` → `purple` (`#7C6EE6`) | `diff_change_bg` → `diff_change_bg` (`#E8E1F3`) | None | Changed line in Diff mode. |

## Terminal contract

| Doom colour | Palette token | Graphical | 256-colour fallback | TTY fallback |
| --- | --- | --- | --- | --- |
| `bg` | `bg` | `#F4F1EA` | `white` | `white` |
| `fg` | `fg` | `#2A2A2A` | `black` | `black` |
| `bg-alt` | `bg_alt` | `#EAE5DC` | `white` | `white` |
| `fg-alt` | `muted` | `#6B6B6B` | `black` | `brightblack` |
| `muted` | `muted` | `#6B6B6B` | `black` | `brightblack` |
| `subtle` | `subtle` | `#A8A29E` | `brightblack` | `brightblack` |
| `border` | `border` | `#D6D0C4` | `brightblack` | `brightblack` |
| `info` | `info` | `#4A90E2` | `brightblue` | `brightblue` |
| `red` | `red` | `#C23B3B` | `red` | `red` |
| `orange` | `orange` | `#C47A2C` | `brightred` | `brightred` |
| `green` | `green` | `#4C9A5F` | `green` | `green` |
| `yellow` | `yellow` | `#B58900` | `yellow` | `yellow` |
| `blue` | `blue` | `#3A7BD5` | `brightblue` | `brightblue` |
| `pink` | `pink` | `#C05A8C` | `magenta` | `magenta` |
| `purple` | `purple` | `#7C6EE6` | `brightmagenta` | `brightmagenta` |
| `cyan` | `cyan` | `#2F8F8B` | `brightcyan` | `brightcyan` |
| `selection` | `selection` | `#E6DCC8` | `brightblack` | `brightblack` |

## Target helpers

| Helper | Colour | Purpose |
| --- | --- | --- |
| `base0` | `#FBF9F4` | Lightest paper surface for whitespace and subtle overlays. |
| `base1` | `#F4F1EA` | Doom neutral ramp alias for the canonical background. |
| `base2` | `#EAE5DC` | Secondary paper surface used by blocks and panels. |
| `base3` | `#D6D0C4` | Neutral border step. |
| `base4` | `#B8B1A7` | Intermediate neutral required by Doom's base palette. |
| `base5` | `#A8A29E` | Subtle chrome neutral. |
| `base6` | `#6B6B6B` | Muted foreground neutral. |
| `base7` | `#4A4742` | Dark neutral between foreground and muted text. |
| `base8` | `#2A2A2A` | Doom neutral ramp alias for the canonical foreground. |
| `modeline_bg` | `#EAE5DC` | Active modeline surface. |
| `modeline_bg_inactive` | `#D6D0C4` | Inactive modeline surface. |
| `popup_bg` | `#EAE5DC` | Completion and popup surface. |
| `popup_selection` | `#E6DCC8` | Selected completion or picker row. |
| `diff_add_bg` | `#DCEEDB` | Low-chroma added-line background. |
| `diff_change_bg` | `#E8E1F3` | Low-chroma changed-line background. |
| `diff_delete_bg` | `#F3D9D9` | Low-chroma deleted-line background. |

## Rendering paths

Built-in Emacs Tree-sitter modes normally assign Font Lock faces, so their contract is the Font Lock section above. The legacy `tree-sitter` package has a separate `tree-sitter-hl-face:*` namespace; Helsing does not map those faces without runtime evidence that an installed mode uses them.

Eglot faces are conditional. They affect a buffer only when Eglot is managing it, semantic-token highlighting is enabled, and the language server advertises a semantic-token provider. Otherwise, Font Lock remains the fallback.

## Inspection rule

When a token renders incorrectly, record the major mode, face at point, inherited faces, Eglot state, semantic-token capability, and final foreground/background before changing the theme.
