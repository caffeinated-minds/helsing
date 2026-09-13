# Helsing Emacs fixtures

These files exercise Emacs-specific syntax and prose faces. The Python, Go, Bash, TypeScript, C, CSS and HTML fixtures in [`themes/vscode/examples`](../../vscode/examples) are shared across editors so that Helsing can be compared against the same source text.

For each fixture:

1. open the file in Doom Emacs;
2. confirm the intended major mode;
3. load `checks/emacs-inspect.el`;
4. run `M-x helsing-inspect-face-at-point` on representative tokens;
5. compare the face and colour with `docs/helsing-emacs-role-matrix.md`.

Review semantic roles rather than expecting different parsers to expose identical token detail.
