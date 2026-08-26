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

## Syntax highlighting

Helsing explicitly maps modern Emacs Font Lock and Eglot semantic-token faces to the canonical syntax roles. For the closest parity with the VS Code and Neovim themes, use each language's Tree-sitter mode and install the corresponding native grammar. Legacy major modes remain supported, but they may expose fewer semantic categories for the theme to colour.

## Development

The theme is generated from [`docs/helsing-palette.yml`](../../docs/helsing-palette.yml) using [`generator/config/doom-emacs.yml`](../../generator/config/doom-emacs.yml) and [`generator/templates/doom-emacs/helsing-theme.el.j2`](../../generator/templates/doom-emacs/helsing-theme.el.j2). Do not edit the generated file independently.

From the repository root:

```bash
python generator/generate.py doom-emacs
python generator/generate.py doom-emacs --check
./checks/validate.sh
```

The theme does not configure fonts. Set GoMono Nerd Font through Doom's normal `doom-font` configuration.
