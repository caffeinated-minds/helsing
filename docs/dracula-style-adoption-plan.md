# Dracula-Style Theme Adoption Plan for Helsing

## Implementation status

The VS Code adoption work is implemented at repository level. The canonical contract now declares role intent, token, permitted styles and fallbacks; `generator/config/vscode.yml` maps named roles to workbench, TextMate and semantic-token output; generation produces the extension JSON, a role matrix and a machine-readable fixture contract; validation rejects drift, invalid palette references and unapproved broad selectors; packaging runs validation first; and CI repeats the clean-checkout package path.

The only intentionally manual acceptance step is interactive inspection in VS Code. Grammar and language-server classifications are runtime inputs owned by VS Code and installed language extensions, so `generator/config/vscode-fixtures.yml` records the expected evidence but must be confirmed with **Developer: Inspect Editor Tokens and Scopes** whenever those dependencies change. This is validation of the implementation, not an unimplemented theme component.

## Purpose

This document defines a concrete adoption plan for making Helsing’s palette contract and editor implementations work like a mature, multi-application theme project.

The goal is not to copy Dracula’s colours or visual style. The goal is to adopt the useful engineering pattern behind Dracula’s VS Code theme:

```text
canonical palette and role contract
            ↓
target-specific source definition
            ↓
generated or packaged application theme
            ↓
scope inspection, fixtures, and validation
```

This plan is deliberately conservative. It preserves Helsing’s existing palette, typography, light-theme identity, and role names while making implementation drift easier to detect.

## Desired outcomes

After this work:

- `docs/helsing-palette.yml` remains the canonical colour and role contract.
- Every target consumes named Helsing roles instead of inventing equivalent colours.
- VS Code has one authoritative source file and a reproducible generated JSON artifact.
- TextMate scopes and semantic-token rules are treated as separate, testable layers.
- Broad scope selectors cannot silently override more specific semantic roles.
- Python, Go, Bash, JavaScript/TypeScript, React, C, CSS, HTML, and other supported languages have representative fixtures.
- Theme changes can be validated without relying only on screenshots.
- Generated files, palette references, and fixture expectations are checked in local validation and CI.
- Other targets—Neovim, Vim, Doom Emacs, terminals, and browser themes—remain aligned with the same role contract.

## Non-goals

This plan does not:

- change the Helsing palette;
- make all applications use the same rendering engine;
- guarantee identical syntax colouring where an application or language server exposes different token information;
- eliminate every target-specific helper colour;
- replace useful application-native UI colours with arbitrary Helsing accents;
- require semantic highlighting to be available in every editor.

The contract is about stable semantic intent. Each target remains an adapter to its own rendering model.

## Current system map

### Canonical contract

`docs/helsing-palette.yml` currently defines:

- structural colours such as `bg`, `bg_alt`, `fg`, `muted`, `subtle`, `border`, and `selection`;
- semantic colours such as `purple`, `blue`, `green`, `orange`, `cyan`, `pink`, `red`, `yellow`, and `info`;
- semantic roles such as `keyword`, `function`, `string`, `type`, `variable`, `parameter`, `property`, and diagnostics;
- typography roles, including GoMono Nerd Font;
- rules forbidding ad-hoc target hex values and separating structural from semantic colours.

### Generated targets

The repository currently contains generator inputs in `generator/config/`, templates in `generator/templates/`, and generated or packaged theme files under `themes/`.

The adoption work should preserve that structure and make the source-to-artifact relationship explicit.

### Target rendering layers

Different applications receive different information:

| Target | Primary mechanism | Important limitation |
| --- | --- | --- |
| VS Code | TextMate scopes plus optional semantic tokens | LSP and grammar precedence can differ by language |
| Neovim | Highlight groups, Tree-sitter, and plugin-specific groups | Plugins introduce their own groups and inheritance |
| Vim | Syntax groups and editor highlight groups | Less semantic information than modern LSP clients |
| Doom Emacs | Font-lock, Tree-sitter, and optional Eglot faces | Eglot servers may not expose semantic tokens |
| Alacritty/WezTerm | Terminal palette and UI colours | Programs emit ANSI colours independently |
| Chrome | Manifest/theme colour properties | Browser UI has a smaller role vocabulary |

The contract must therefore map roles, not assume that every target exposes identical token names.

## Phase 1: Freeze and document the contract

### 1. Establish the palette source of truth

Keep `docs/helsing-palette.yml` as the only canonical machine-readable palette. Every colour used in a target should be traceable to one of these categories:

1. a structural token;
2. a semantic token;
3. an explicitly documented target helper token.

Do not add a second palette file for VS Code.

### 2. Add explicit role definitions

Expand `semantic_roles` documentation so every role includes:

- intent;
- canonical colour token;
- expected foreground/background usage;
- whether bold, italic, or underline is allowed;
- fallback role when the target lacks that category;
- representative examples.

For example:

```yaml
keyword:
  token: purple
  intent: "Language control and declaration keywords"
  textmate_scopes:
    - keyword
    - storage
  semantic_tokens:
    - keyword
  fallback: text
```

The exact YAML shape can be chosen during implementation; the important point is that the role-to-scope mapping becomes explicit rather than living only in template code.

### 3. Define precedence rules

Document the rule that a more-specific scope must not accidentally change semantic intent. For example:

```text
specific language declaration scope > generic type scope
semantic token rule > fallback scope rule when semantic data exists
explicit error/warning rule > ordinary token rule
```

This directly protects against errors such as Python’s `storage.type.function.python` being caught by a generic `storage.type` rule and rendered as a type instead of a keyword.

### 4. Define permitted target exceptions

Target-specific exceptions are acceptable only when they are:

- required by the target’s grammar or API;
- narrower than the generic rule they refine;
- documented with the affected language and example;
- covered by a fixture or validation check.

An exception must never be justified only because a screenshot looks convenient.

## Phase 2: Create a VS Code source-of-truth file

### 5. Introduce a named-palette VS Code source

Create a source file analogous to Dracula’s `src/dracula.yml`. It should contain:

- theme metadata;
- named references to Helsing structural and semantic tokens;
- VS Code workbench colours;
- TextMate `tokenColors`;
- semantic-token rules;
- documented target-specific helpers.

The source should refer to role names or palette aliases, not repeat raw hex values.

Conceptually:

```yaml
helsing:
  bg: "{structural.bg}"
  fg: "{structural.fg}"
  keyword: "{semantic.purple}"
  function: "{semantic.blue}"
  type: "{semantic.cyan}"
  string: "{semantic.green}"

tokenColors:
  - name: Keywords
    scope:
      - keyword
      - storage
    settings:
      foreground: "{keyword}"
```

The exact syntax can be JSON, YAML, or a generator-specific model. The design requirement is one authoritative source with reusable role references.

### 6. Keep generated JSON out of manual-edit workflows

The packaged VS Code file should be generated from the source definition. The workflow should be:

```text
edit palette or VS Code source
        ↓
run generator
        ↓
validate generated JSON
        ↓
package extension
```

Generated output may remain committed if the extension packaging workflow needs it, but it must be marked as generated and checked for drift.

### 7. Preserve the existing extension interface

The generated theme must continue to expose the existing Helsing theme name and extension metadata. This avoids breaking local installations, marketplace packaging, or user settings.

## Phase 3: Build the TextMate scope matrix

### 8. Define the core scope matrix

Start with a small, stable set of roles:

| Helsing role | Typical TextMate scopes | Colour |
| --- | --- | --- |
| keyword | `keyword`, `storage` | purple |
| operator | `keyword.operator`, operator scopes | purple |
| function | `entity.name.function`, function-call scopes | blue |
| type | `entity.name.type`, selected `support.type` scopes | cyan |
| namespace | namespace/entity scopes | cyan |
| string | `string` | green |
| regexp | regexp scopes | pink |
| number | numeric constant scopes | orange |
| constant | constant scopes | pink |
| decorator | decorator/annotation scopes | pink |
| variable | variable scopes | foreground |
| parameter | parameter scopes | foreground |
| property | property/member scopes | foreground |
| comment | comment scopes | muted or comment role |
| punctuation | punctuation scopes | subtle |

The table is a design index, not a promise that every grammar emits every scope.

### 9. Prefer precise scopes

Avoid rules such as:

```text
storage.type → type
```

unless every language using that scope really means a type.

Prefer:

```text
entity.name.type → type
storage.type.c → type
storage.type.rust → type
source.go storage.type → type
```

Keep declaration keywords such as Python `def`, `class`, and similar constructs in the keyword/declaration path when their grammar exposes them as storage scopes.

### 10. Add language-specific scope exceptions

For each supported language:

1. inspect declaration keywords;
2. inspect function definitions and calls;
3. inspect type names and built-ins;
4. inspect parameters, properties, strings, comments, and literals;
5. add only the narrowest required scope selector.

Each exception should include a comment explaining the grammar behaviour it handles.

### 11. Decide precedence intentionally

VS Code chooses the most specific matching scope for each style property. Therefore:

- broad defaults should appear before specific refinements;
- specific language scopes must not be shadowed by a broad rule;
- a rule should not claim a scope merely because it contains a matching word such as `type` or `function`;
- foreground and font-style precedence should be tested independently.

## Phase 4: Define semantic-token behaviour

### 12. Enable semantic highlighting deliberately

Set `semanticHighlighting` according to the intended Helsing behaviour. Document whether the theme expects semantic highlighting to be enabled by default.

### 13. Map standard semantic token types

Define semantic mappings for the standard categories Helsing already understands:

- `keyword` → purple;
- `operator` → purple;
- `function` → blue;
- `method` → blue;
- `type` and `class` → cyan;
- `namespace` → cyan;
- `string` → green;
- `number` → orange;
- `enumMember` and constants → pink;
- `parameter`, `variable`, and `property` → foreground;
- comments → muted/comment colour.

### 14. Treat modifiers as secondary attributes

Modifiers such as `readonly`, `static`, `declaration`, `definition`, `async`, and `documentation` should normally change style—italic, bold, or underline—rather than unexpectedly changing the semantic colour.

Any modifier that changes foreground colour must be justified in the contract.

### 15. Test semantic and TextMate paths independently

Every fixture must be checked in at least two modes:

1. semantic highlighting available and enabled;
2. semantic highlighting disabled or unavailable.

The fallback should remain readable and role-consistent in both cases.

This is essential because VS Code/Pylance, Emacs/Eglot, and other clients may expose different semantic-token capabilities.

## Phase 5: Build fixtures and an inspection workflow

### 16. Create representative source fixtures

Create small, intentionally boring files under a test or fixture directory for:

- Python;
- Go;
- Bash;
- JavaScript;
- TypeScript;
- React/TSX;
- C;
- CSS;
- HTML;
- JSON/YAML/TOML where relevant.

Each fixture should include examples of:

- declarations;
- function definitions;
- function calls;
- classes/types/interfaces;
- parameters and properties;
- constants and numbers;
- strings and regular expressions;
- comments and documentation comments;
- operators and punctuation;
- diagnostics where practical.

### 17. Record expected roles, not screenshots alone

For every important token, record:

- source text;
- language;
- expected role;
- expected colour token;
- expected TextMate scope;
- expected semantic token, if available;
- acceptable fallback behaviour.

Screenshots remain useful for visual review, but they should not be the only test evidence.

### 18. Use VS Code’s scope inspector

For each fixture token, run `Developer: Inspect Editor Tokens and Scopes` and record:

- TextMate scopes;
- semantic token type and modifiers;
- winning theme rule;
- final foreground and font style.

When a token is wrong, determine whether the cause is:

1. the grammar’s scope;
2. semantic-token data;
3. rule specificity;
4. an incorrect palette mapping;
5. a generated-artifact drift problem.

## Phase 6: Add generator validation

### 19. Validate palette references

The generator should fail if:

- a referenced palette token does not exist;
- a generated colour differs from the canonical palette unexpectedly;
- a target contains an unapproved raw hex colour;
- structural and semantic tokens are mixed without documentation.

### 20. Validate generated artifacts

The check should:

- parse generated JSON;
- confirm required VS Code theme metadata exists;
- confirm `tokenColors` is present;
- confirm semantic highlighting configuration is valid;
- confirm all referenced colours are valid CSS/VS Code colours;
- regenerate output and fail if the working tree changes.

### 21. Detect dangerous broad selectors

Add a review or lint check for selectors known to cause collisions, including:

- generic `storage.type`;
- generic `support`;
- generic `variable` rules with foreground changes;
- selectors that overlap a more specific rule without an explicit reason.

This need not ban every broad selector. It should require an allow-list or explanatory comment for high-risk cases.

### 22. Validate role coverage

The validation report should show, for every canonical role:

- whether VS Code has a TextMate mapping;
- whether VS Code has a semantic-token mapping;
- whether each other target has an implementation;
- which roles intentionally fall back to another role.

Missing coverage should be visible, not silently inferred.

## Phase 7: Align other target implementations

### 23. Map each target back to canonical roles

For each theme target, create a small mapping table from application-specific groups to Helsing roles.

Examples:

```text
Neovim @keyword → Helsing keyword/purple
Vim Statement → Helsing keyword/purple
Doom font-lock-keyword-face → Helsing keyword/purple
Alacritty normal → Helsing fg/bg
```

### 24. Keep target helpers local

Popup surfaces, diff backgrounds, plugin-specific groups, and application chrome may require helper colours. Keep them in the target implementation unless they are genuinely shared across applications.

Promote a helper into the canonical palette only when:

- at least two targets need it;
- its visual meaning is stable;
- its contrast and relationship to existing roles are documented.

### 25. Do not force semantic parity where information differs

If an Emacs language server does not expose semantic tokens, use its font-lock or Tree-sitter groups. Record that limitation rather than adding arbitrary colour rules intended to imitate information the editor does not provide.

## Phase 8: CI and release workflow

### 26. Define the local validation command

Provide one documented command that runs:

1. palette validation;
2. generator validation;
3. target generation;
4. JSON/syntax checks;
5. fixture checks;
6. generated-file drift checks.

### 27. Run validation before packaging

The VS Code package command should depend on successful generation and validation. A VSIX must never be produced from stale generated theme files.

### 28. Review visual changes separately

Automated checks should verify structure and role mapping. Human review should verify:

- overall contrast;
- readability at laptop and ultrawide resolutions;
- UI hierarchy;
- absence of accidental bright or commented-out-looking text;
- consistency of active and inactive states.

### 29. Keep releases reproducible

Record:

- the Helsing repository commit;
- generator version;
- palette version;
- target package version;
- fixture/validation result.

Generated output should be reproducible from a clean checkout.

## Recommended implementation order

Implement in this order to keep the blast radius small:

1. Document the current contract and scope matrix.
2. Add palette-reference validation without changing colours.
3. Refactor the VS Code source to use named palette references.
4. Remove or narrow dangerous broad scopes, beginning with generic `storage.type`.
5. Add semantic-token mappings and test them separately.
6. Add language fixtures and scope-inspection records.
7. Add generated-artifact drift checks.
8. Align Neovim, Vim, and Doom Emacs mappings with the role matrix.
9. Add CI and package validation.
10. Reassess visual output and only then consider palette changes.

## Acceptance criteria

The adoption is complete when:

- the palette contract is the only canonical colour source;
- VS Code’s packaged theme is generated from a named-role source;
- Python `def` and `class` resolve to the keyword role;
- actual type names resolve to the type role;
- function names and calls resolve to the function role;
- behaviour remains sensible with semantic highlighting disabled;
- every supported language has at least one fixture;
- generated output is checked for drift;
- broad scope collisions are either removed or explicitly justified;
- other targets document their role mappings and known rendering limitations;
- a clean checkout can generate and validate the theme without manual edits.

## Engineering principle

The important change is not “use more colours” or “copy Dracula’s file layout.” It is to establish a controlled translation boundary:

```text
Helsing role contract
        ↓
target-specific token/scope mapping
        ↓
application rendering behaviour
```

When a result is wrong, that boundary tells us where to investigate: the contract, the mapping, the editor’s token data, or the generated artifact. That makes future theme debugging a repeatable engineering process rather than visual guesswork.
