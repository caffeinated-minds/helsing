# Helsing for Doom Emacs

`helsing-theme.el` is Helsing's generated Doom Emacs theme. It maps the canonical Helsing palette onto Doom's editor, completion, modeline, dashboard, Magit, Org, diagnostics and version-control faces.

## Install with Doom

Add this package declaration to your Doom `packages.el`, pinning it to a reviewed Helsing commit:

```elisp
(package! helsing-theme
  :recipe (:host github
           :repo "caffeinated-minds/helsing"
           :files ("themes/doom-emacs/helsing-theme.el"))
  :pin "HELSING_COMMIT_SHA")
```

Set the theme in `config.el`:

```elisp
(setq doom-theme 'helsing)
```

Then run `doom sync` and restart Emacs.

## Rendering model

Helsing maps canonical roles onto standard Font Lock faces. Built-in Emacs Tree-sitter modes use those Font Lock faces after parsing, so they share the same stable contract:

```text
major mode or built-in Tree-sitter query
                ↓
standard Font Lock face
                ↓
Helsing role and colour
```

Emacs 30.2's Eglot does not provide `eglot-semantic-tokens-mode` or `eglot-semantic-*` faces. Helsing therefore does not declare speculative semantic-token faces. It styles the Eglot faces that actually exist for symbol highlights, diagnostic tags and inlay hints; code syntax continues through Font Lock.

The generated [Emacs role matrix](../../docs/helsing-emacs-role-matrix.md) records the expected role and colour for every covered core, Font Lock and Eglot face.

## Inspect a rendered token

Start with Emacs's built-in `M-x describe-face`. To capture the complete rendering path, load the repository helper and inspect the token at point:

```elisp
(load-file "/path/to/helsing/checks/emacs-inspect.el")
M-x helsing-inspect-face-at-point
```

Record the major mode, active face, Tree-sitter parser, Eglot state and resolved colours before changing a theme rule. A missing semantic-token API means Font Lock is the relevant layer.

The language examples under [`themes/vscode/examples`](../vscode/examples) are shared syntax fixtures and can be opened in Emacs for cross-editor comparison. The expected comparison is role parity, not identical parsing information.

## Development

The theme is generated from [`docs/helsing-palette.yml`](../../docs/helsing-palette.yml) using [`generator/config/doom-emacs.yml`](../../generator/config/doom-emacs.yml) and [`generator/templates/doom-emacs/helsing-theme.el.j2`](../../generator/templates/doom-emacs/helsing-theme.el.j2). Do not edit the generated file independently.

From the repository root:

```bash
python generator/generate.py doom-emacs
python generator/generate.py doom-emacs --check
./checks/validate.sh
```

Validation checks the generated artifact, Doom colour aliases, graphical face declarations, a real Font Lock buffer, and unload/reload behaviour. Batch Emacs cannot assess visual balance, so review UI changes in a normal graphical Doom session before release.

Updating the installed Doom package pin is a separate release step. Generate, validate, review, commit, and only then update the pin and run `doom sync`.

The theme does not configure fonts. Set GoMono Nerd Font through Doom's normal `doom-font` configuration.
