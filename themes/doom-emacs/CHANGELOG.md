# Changelog

## Unreleased

- Added a generated role-to-face contract and human-readable Emacs role matrix.
- Added batch validation for colour aliases, graphical face declarations, real Font Lock classification, and theme reload safety.
- Made the `default` and `region` faces explicit instead of relying on implicit Doom defaults.
- Removed speculative `eglot-semantic-*` mappings that do not exist in Emacs 30.2.
- Added mappings for Eglot's actual symbol-highlight, diagnostic-tag, and inlay-hint faces.
- Documented that built-in Emacs Tree-sitter modes use the Font Lock contract and that legacy Tree-sitter faces require runtime evidence before inclusion.
