# Dracula-Style Adoption Plan for Helsing Doom Emacs

## Purpose

This document defines how Helsing’s Doom Emacs theme should adopt the useful engineering patterns visible in Dracula’s official Emacs implementation while preserving Helsing’s own palette, light-theme identity, GoMono typography policy, and semantic-role contract.

The objective is not to copy Dracula’s dark colours or visual choices. It is to make the Helsing Emacs target a disciplined adapter between the canonical Helsing contract and Emacs’s face system.

The intended flow is:

```text
canonical Helsing palette and roles
              ↓
Emacs/Doom role and face mapping
              ↓
generated helsing-theme.el
              ↓
Emacs display, package faces, and terminal fallbacks
              ↓
face inspection and automated smoke tests
```

## Implementation status

The contract and safety infrastructure described here are implemented in the repository:

- the role aliases and face contract live in `generator/config/doom-emacs.yml`;
- the generator produces the loadable theme, this target's role matrix, and an executable test contract;
- batch validation checks the graphical face declarations, a real Font Lock buffer, and theme reload behaviour;
- `checks/emacs-inspect.el` reports the rendering path at point;
- speculative Eglot semantic faces are excluded for Emacs 30.2;
- generated-file drift is checked by `generator/generate.py --check`.

Visual review in a normal graphical Doom session remains a release gate whenever a face mapping or helper colour changes. The installed Doom package pin is intentionally updated only after that review.

## What Dracula’s Emacs implementation does

The official implementation is [`dracula-theme.el`](https://github.com/dracula/emacs/blob/master/dracula-theme.el). It is a conventional Emacs Custom Theme rather than a cross-editor generator.

Its important patterns are:

1. It declares a real Emacs theme with `deftheme`.
2. It exposes user-facing options with `defgroup` and `defcustom`.
3. It defines named colour variables once, including GUI, 256-colour, and TTY fallbacks.
4. It maps those variables to a large, explicitly grouped face table.
5. It uses face inheritance where a package face has the same meaning as an existing role.
6. It includes package-specific face mappings for completion, version control, diagnostics, navigation, documentation, and other common packages.
7. It includes Eglot and Tree-sitter-related support as Emacs capabilities evolve.
8. It provides a test profile/script for graphical, true-colour terminal, and limited-colour terminal environments.
9. It documents configuration options and reload requirements.

The file’s opening commentary states that it tries to follow the shared Dracula specification, while the implementation necessarily uses Emacs-specific faces and fallbacks. [Dracula theme source](https://raw.githubusercontent.com/dracula/emacs/master/dracula-theme.el)

This is the useful lesson for Helsing: one stable role vocabulary, one explicit face mapping, deliberate package coverage, and tests for the display environments that Emacs actually supports.

## What Helsing already has

Helsing currently has several good foundations:

- `docs/helsing-palette.yml` is the canonical machine-readable palette;
- `generator/config/doom-emacs.yml` defines Doom-specific helper colours;
- `generator/templates/doom-emacs/helsing-theme.el.j2` is the generation template;
- `themes/doom-emacs/helsing-theme.el` is generated output;
- the theme maps core Font Lock faces, Eglot semantic faces, Doom UI, Corfu, Vertico, Magit, diagnostics, Org, Markdown, Dired, Evil, and version-control faces;
- the theme uses explicit light-background and warm-paper structural roles;
- the Doom package is installed from the Helsing repository at a pinned commit.

The main remaining work is to make the contract-to-face mapping more explicit, make package coverage measurable, and test the actual face selected in each rendering path.

## Scope and non-goals

This plan covers:

- the generated Doom theme;
- standard Emacs faces;
- Font Lock and Tree-sitter faces;
- Eglot semantic faces;
- Doom and package-specific faces;
- graphical and terminal fallbacks;
- loading, reload, and validation workflows.

It does not:

- change the Helsing palette;
- require every package to receive a unique colour;
- force Emacs to imitate VS Code where Emacs receives less token information;
- configure GoMono through the theme itself;
- replace Doom’s package configuration;
- add arbitrary face colours merely because a package exposes a face.

## Design principles

### 1. Roles are canonical; faces are adapters

The palette defines semantic intent. Emacs faces are implementation names.

For example:

```text
Helsing keyword role
        ↓
font-lock-keyword-face
eglot-semantic-keyword
tree-sitter-hl-face:keyword
```

All three should resolve to the Helsing keyword colour unless Emacs’s rendering model requires a documented fallback.

### 2. Core faces first, package faces second

The theme should first establish predictable defaults for:

- `default`;
- cursor and selection;
- comments and documentation;
- keywords, operators, functions, types, strings, constants, numbers, variables, properties, and punctuation;
- errors, warnings, success, and informational states.

Package-specific faces should inherit from those roles wherever possible.

### 3. Inheritance is preferred to duplicated colour literals

If a package face means “success,” use `:inherit success` or the equivalent generated role rather than repeating the green hex value.

This makes later palette changes safe and makes the semantic intent visible in the source.

### 4. Explicit exceptions must be narrow

A package or mode may need a special face, but the mapping should state why it exists. Do not use a broad face override to repair one mode if it changes unrelated modes.

### 5. Terminal support is part of the target contract

Emacs can run graphically, in a true-colour terminal, in a 256-colour terminal, or in a 16-colour terminal. A complete theme must define sensible fallbacks instead of assuming 24-bit colour is always available.

## Phase 1: Formalise the Emacs role model

### 1. Add an Emacs role matrix

Create a documented mapping table, either in the generator configuration or a dedicated documentation file, with these columns:

| Helsing role | Emacs face/group | Source layer | Fallback | Notes |
| --- | --- | --- | --- | --- |
| background | `default` background | core | terminal background | Main paper surface |
| text | `default` foreground | core | terminal foreground | Normal code and prose |
| keyword | `font-lock-keyword-face` | Font Lock | text | Control/declaration keywords |
| function | `font-lock-function-name-face` | Font Lock | text | Definitions and names |
| type | `font-lock-type-face` | Font Lock | builtin/type | Types and classes |
| string | `font-lock-string-face` | Font Lock | text | String literals |
| comment | `font-lock-comment-face` | Font Lock | muted | Comments and documentation |
| parameter | mode-provided Font Lock face | Font Lock | variable | Emacs 30.2 Eglot has no semantic-token faces |
| property | `font-lock-property-name-face` | Font Lock | variable | Property names when the mode distinguishes them |
| punctuation | `font-lock-punctuation-face` | Font Lock | subtle | Delimiters and punctuation |

The matrix should cover every role in `docs/helsing-palette.yml`.

### 2. Record source precedence

Document the expected precedence:

```text
package or overlay face, when applied
        ↓
Font Lock face assigned by the major mode
        ↓
default text role
```

Built-in Emacs Tree-sitter modes parse syntax and then assign Font Lock faces. Emacs 30.2's Eglot does not provide a semantic-token face layer. If a future Emacs release adds one, it must be detected and tested before the model becomes:

```text
verified semantic-token face, when supported and applied
        ↓
Font Lock fallback
```

This is a conceptual precedence model. Actual Emacs face inheritance and mode setup must be verified with `describe-face` and buffer inspection.

### 3. Define intentional aliases

The current theme has aliases such as `functions`, `keywords`, `type`, `strings`, and `variables`. Keep these aliases, but document them as semantic role aliases rather than independent colours.

For example:

```text
keywords → semantic_roles.keyword → purple
functions → semantic_roles.function → blue
strings → semantic_roles.string → green
```

## Phase 2: Refine the generated theme structure

### 4. Keep the generated file authoritative at runtime

`themes/doom-emacs/helsing-theme.el` should remain generated from:

- `docs/helsing-palette.yml`;
- `generator/config/doom-emacs.yml`;
- `generator/templates/doom-emacs/helsing-theme.el.j2`.

Do not make manual edits to the generated file. Change the palette, configuration, or template and regenerate.

### 5. Group faces by semantic responsibility

Follow the existing grouped structure and keep it stable:

1. core/editor faces;
2. syntax and Font Lock;
3. supported Eglot UI, diagnostic and inlay-hint faces;
4. verified compatibility faces, if any;
5. completion and minibuffer;
6. Doom modeline and editor chrome;
7. diagnostics and warnings;
8. version control and diffs;
9. Org and Markdown;
10. package-specific integrations.

This mirrors Dracula’s maintainable face table without copying its dark-theme choices.

### 6. Use role aliases in the template

The template should refer to semantic aliases such as `keywords`, `functions`, `type`, `strings`, `comments`, and `variables`. It should use direct palette names only when the face’s meaning is genuinely a structural or diagnostic role.

### 7. Minimise target-only helper colours

Keep helpers such as `base0`–`base8`, popup surfaces, modeline surfaces, and diff backgrounds in `generator/config/doom-emacs.yml` unless they become cross-target concepts.

Every helper should document:

- why the canonical role is insufficient;
- which package or Emacs surface needs it;
- its contrast relationship to `bg`, `bg_alt`, and `fg`;
- whether it is foreground, background, border, or decoration only.

## Phase 3: Implement the syntax stack deliberately

### 8. Core Font Lock mapping

Ensure the following faces map consistently:

| Face | Helsing role |
| --- | --- |
| `font-lock-keyword-face` | keyword/purple |
| `font-lock-operator-face` | operator/purple |
| `font-lock-function-name-face` | function/blue |
| `font-lock-function-call-face` | function/blue |
| `font-lock-builtin-face` | builtin function/blue or documented builtin role |
| `font-lock-type-face` | type/cyan |
| `font-lock-string-face` | string/green |
| `font-lock-constant-face` | constant/pink |
| `font-lock-number-face` | number/orange |
| `font-lock-variable-name-face` | variable/foreground |
| `font-lock-property-name-face` | property/foreground |
| `font-lock-comment-face` | comment/muted |
| `font-lock-doc-face` | documentation/subtle |
| `font-lock-punctuation-face` | punctuation/subtle |

The literal Python `def` keyword must arrive at `font-lock-keyword-face` or an equivalent semantic keyword face. A function name after `def` must arrive at the function face. These are separate checks.

### 9. Tree-sitter mapping

Built-in Emacs Tree-sitter modes use Font Lock faces and are covered by the core mapping. Do not invent a separate `treesit-face-*` layer. The external legacy `tree-sitter` package may use `tree-sitter-hl-face:*`; add one of those faces only after runtime inspection proves that an installed mode applies it.

Recommended role mapping:

```text
keyword → font-lock-keyword-face
function → font-lock-function-name-face
function.call → font-lock-function-call-face
type → font-lock-type-face
string → font-lock-string-face
comment → font-lock-comment-face
constant → font-lock-constant-face
variable → font-lock-variable-name-face
punctuation → subtle/punctuation
```

### 10. Eglot mapping

Map the Eglot faces that exist in the supported Emacs version:

| Eglot face | Helsing role |
| --- | --- |
| `eglot-highlight-symbol-face` | selection background |
| `eglot-diagnostic-tag-unnecessary-face` | muted |
| `eglot-diagnostic-tag-deprecated-face` | muted and struck through |
| `eglot-inlay-hint-face` | subtle |
| `eglot-type-hint-face` | inherit inlay hint |
| `eglot-parameter-hint-face` | inherit inlay hint |

Emacs 30.2 does not define `eglot-semantic-tokens-mode` or `eglot-semantic-*` faces. Syntax highlighting therefore remains a Font Lock responsibility even when Eglot is managing the buffer.

### 11. Do not force semantic tokens on unsupported servers

Do not declare speculative `eglot-semantic-*` faces. Before adding semantic-token support for a future Emacs release, verify the installed API, verify language-server capability, and add tests for both the semantic and Font Lock fallback paths.

## Phase 4: Package and Doom integration

### 12. Map Doom’s own faces

Review and explicitly cover the Doom surfaces used by this configuration:

- modeline and inactive modeline;
- popup windows;
- dashboard;
- completion menus;
- project and buffer selectors;
- which-key;
- notifications;
- search and jump interfaces;
- file trees;
- status indicators.

Package faces should inherit from `bg_alt`, `selection`, `muted`, `subtle`, and the semantic roles rather than introducing unrelated shades.

### 13. Map active package faces by installed configuration

The theme should prioritise packages that are actually enabled in this Doom installation, including:

- Corfu;
- Vertico and Orderless;
- Marginalia;
- Magit and Transient;
- Flymake;
- Org and Markdown;
- Dired;
- Evil;
- which-key;
- the active file tree and picker packages.

Other package groups can be added incrementally when installed or requested.

### 14. Use inheritance for repeated states

Examples:

```elisp
(flymake-error :inherit error)
(flymake-warning :inherit warning)
(go-test--ok-face :inherit success)
(evil-ex-lazy-highlight :inherit lazy-highlight)
```

The exact generated syntax may differ, but the principle is stable: state faces should inherit the semantic state role.

## Phase 5: Typography and display behaviour

### 15. Keep fonts outside the theme

Dracula exposes optional heading sizing and boldness controls. Helsing should document similar options only if they are genuinely needed, but should not set the global font from the theme.

GoMono Nerd Font belongs in Doom’s `doom-font` or system font configuration. The theme controls colour, weight, slant, and height only where that is part of semantic presentation.

### 16. Make heading styling explicit and restrained

Document whether headings should:

- remain the default size;
- use bold only;
- use controlled relative sizes;
- apply to Org, Markdown, dashboard, and documentation buffers consistently.

Avoid adding package-specific heading sizes until the base behaviour is stable on laptop and ultrawide displays.

### 17. Validate graphical and terminal displays

At minimum, test:

- graphical Emacs;
- `emacs -nw` with true-colour support;
- 256-colour terminal;
- constrained 16-colour terminal where practical.

The terminal fallback values should preserve role distinction even when exact RGB values are unavailable.

## Phase 6: Build a face inspection workflow

### 18. Inspect the active buffer, not only the theme file

For a problematic token:

1. identify the major mode;
2. check whether Tree-sitter is active;
3. check whether Eglot is active and has semantic-token capability;
4. inspect the token’s face with `face-at-point` or equivalent;
5. inspect the face definition with `describe-face`;
6. inspect face inheritance and buffer-local overlays;
7. compare the result with the expected Helsing role.

### 19. Record the rendering path

Each test result should state:

```text
mode: python-ts-mode
tree-sitter: active
eglot: active
semantic tokens: unavailable
token: def
face: font-lock-keyword-face
role: keyword
colour: purple
```

This prevents a Font Lock problem from being misdiagnosed as an Eglot problem.

### 20. Use representative fixtures

Create small fixtures for:

- Python;
- Go;
- Bash;
- JavaScript/TypeScript;
- React/TSX;
- C;
- CSS;
- HTML;
- Emacs Lisp;
- Markdown and Org.

Each fixture should include declarations, functions, types, strings, comments, constants, properties, parameters, operators, and diagnostics where supported.

## Phase 7: Automated validation

### 21. Validate generated output

The generator check should fail when:

- the generated theme differs from the template and palette inputs;
- a referenced role does not exist;
- a raw colour is introduced without an approved helper declaration;
- a required core face is missing;
- a target helper has no documented purpose;
- generated Elisp is syntactically invalid.

### 22. Validate role coverage

Produce a report showing, for each canonical role:

- core Emacs face coverage;
- Tree-sitter coverage;
- Eglot coverage;
- Doom/package coverage;
- terminal fallback coverage;
- known limitations.

### 23. Add an Emacs smoke test

The smoke test should launch a minimal Emacs profile and verify that:

- the theme loads without warnings;
- `helsing` is discoverable through `custom-theme-load-path`;
- the default face has the expected background and foreground;
- core syntax faces resolve to expected colours;
- package faces referenced by the theme do not cause load errors;
- the theme can be disabled/reloaded cleanly.

### 24. Test both package-present and package-absent cases

Emacs themes commonly run with optional packages missing. The theme must not fail merely because a package face is not currently defined.

Use guarded face specifications or the theme framework’s supported approach for optional faces.

### 25. Test reload behaviour

Changing a theme option or generated face should not require guessing which process is stale. Document and test:

- restart Emacs;
- unload and reload the theme;
- Doom reload/sync where package files changed;
- regeneration of the theme file.

## Phase 8: Documentation and release discipline

### 26. Keep the Emacs README operational

The Doom Emacs README should document:

- installation and pinning;
- `doom sync` and restart requirements;
- font configuration ownership;
- syntax rendering layers;
- known Eglot/Tree-sitter limitations;
- generation commands;
- validation commands;
- how to inspect a face at point.

### 27. Add a changelog entry for face changes

Every semantic face change should state:

- the affected role;
- the affected modes/packages;
- whether the change affects Font Lock, Tree-sitter, Eglot, or UI faces;
- whether a restart or `doom sync` is required;
- the expected rollback path.

### 28. Pin reviewed theme revisions

The Doom package declaration should remain pinned to a reviewed Helsing commit. Updating the pin is a separate operation from changing local generated output.

The update process is:

1. generate and validate locally;
2. review fixture output;
3. commit the Helsing theme changes;
4. update the Nix/Doom pin;
5. run `doom sync`;
6. restart Emacs;
7. verify the active loaded file and commit.

## Recommended implementation order

Implement this in small, reversible stages:

1. Add the Emacs role matrix and rendering-path documentation.
2. Audit the current generated theme against the matrix.
3. Remove duplicate colour literals where an existing role alias is available.
4. Verify and correct core Font Lock faces.
5. Verify Tree-sitter face families against the installed Emacs modes.
6. Verify Eglot faces and server capability reporting.
7. Audit active Doom/package faces and replace duplicated colours with inheritance.
8. Add terminal fallback tests.
9. Add fixture files and face-inspection records.
10. Add the Emacs smoke test and generated-output drift check.
11. Update the README and changelog.
12. Only then consider visual refinements.

## Acceptance criteria

The Helsing Doom Emacs implementation is in the desired state when:

- the theme is generated from the canonical palette and Doom configuration;
- every core semantic role has a documented Emacs face mapping;
- Python `def` is purple as a keyword;
- Python function names are blue as functions;
- types and classes are cyan;
- strings are green;
- comments are muted;
- the same role mappings work through Font Lock and Tree-sitter where available;
- supported Eglot UI, diagnostic and hint mappings are present;
- unsupported `eglot-semantic-*` faces are absent;
- optional package faces do not break theme loading;
- the theme is readable in graphical and terminal modes;
- GoMono is configured separately from theme colour loading;
- generated files pass validation;
- a clean checkout can generate, load, inspect, and smoke-test the theme.

## Engineering principle

The Emacs theme should be treated as a typed adapter, not a bag of face colours:

```text
Helsing semantic role
        ↓
Emacs face family
        ↓
active mode/package rendering path
```

When a colour is wrong, troubleshoot that path in order:

1. Is the canonical role correct?
2. Did the generator map the role correctly?
3. Which face did the buffer actually apply?
4. Was that face supplied by Font Lock, Tree-sitter, Eglot, a package, or an overlay?
5. Did inheritance or a later face override change the result?
6. Is the display using the expected colour capability?

That process gives Helsing the same useful discipline as Dracula’s Emacs project while retaining a stronger cross-editor source-of-truth model.

## References

- [Dracula Emacs repository](https://github.com/dracula/emacs)
- [Dracula Emacs theme source](https://github.com/dracula/emacs/blob/master/dracula-theme.el)
- [Dracula Emacs installation and configuration](https://draculatheme.com/emacs)
- [Helsing canonical palette](./helsing-palette.yml)
- [Helsing Doom Emacs theme](../themes/doom-emacs/helsing-theme.el)
- [Helsing Doom Emacs generator configuration](../generator/config/doom-emacs.yml)
