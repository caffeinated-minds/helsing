;;; emacs-inspect.el --- Inspect Helsing's active Emacs rendering path -*- lexical-binding: t; -*-

(require 'seq)

(defun helsing-inspect-face-at-point ()
  "Describe the syntax-highlighting path and face at point.

The result distinguishes the active major mode, built-in Tree-sitter use,
Eglot management, semantic-token API availability, raw face property, and
resolved foreground/background."
  (interactive)
  (let* ((raw-face (get-char-property (point) 'face))
         (faces (cond
                 ((facep raw-face) (list raw-face))
                 ((listp raw-face) (seq-filter #'facep raw-face))
                 (t nil)))
         (primary-face (car faces))
         (result
          (list
           :major-mode major-mode
           :treesit-parser
           (and (fboundp 'treesit-parser-list)
                (treesit-parser-list))
           :eglot-managed
           (and (boundp 'eglot--managed-mode)
                eglot--managed-mode)
           :semantic-token-api
           (fboundp 'eglot-semantic-tokens-mode)
           :semantic-token-mode
           (and (boundp 'eglot-semantic-tokens-mode)
                eglot-semantic-tokens-mode)
           :raw-face raw-face
           :foreground
           (and primary-face
                (face-attribute primary-face :foreground nil t))
           :background
           (and primary-face
                (face-attribute primary-face :background nil t))
           :inherit
           (and primary-face
                (face-attribute primary-face :inherit nil nil)))))
    (message "%S" result)
    result))

(provide 'helsing-emacs-inspect)
;;; emacs-inspect.el ends here
