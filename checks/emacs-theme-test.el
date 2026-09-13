;;; emacs-theme-test.el --- Helsing Emacs batch checks -*- lexical-binding: t; -*-

(require 'cl-lib)
(require 'seq)
(require 'doom-themes)
(require 'eglot)
(require 'helsing-emacs-face-contract)

(defun helsing-test--fail (format-string &rest args)
  "Signal a Helsing test failure using FORMAT-STRING and ARGS."
  (error "Helsing Emacs test: %s" (apply #'format format-string args)))

(defun helsing-test--assert (condition format-string &rest args)
  "Fail unless CONDITION is non-nil."
  (unless condition
    (apply #'helsing-test--fail format-string args)))

(defun helsing-test--same-color-p (actual expected)
  "Return non-nil when ACTUAL and EXPECTED are equal colour strings."
  (and (stringp actual)
       (string-equal (downcase actual) (downcase expected))))

(defun helsing-test--face-includes-p (actual expected)
  "Return non-nil when ACTUAL face data includes EXPECTED."
  (cond
   ((eq actual expected) t)
   ((listp actual) (memq expected actual))
   (t nil)))

(defun helsing-test--face-at-text (text)
  "Return the face applied to the first occurrence of TEXT."
  (goto-char (point-min))
  (unless (search-forward text nil t)
    (helsing-test--fail "fixture text %S was not found" text))
  (get-text-property (match-beginning 0) 'face))

(defun helsing-test--theme-face-attribute (theme face attribute)
  "Return THEME's graphical ATTRIBUTE declaration for FACE.

Batch Emacs has no colour display, so `face-attribute' cannot select the
graphical branch. Reading the enabled theme declaration validates the branch
that a graphical frame will use."
  (let* ((settings (get theme 'theme-settings))
         (entry
          (seq-find
           (lambda (item)
             (and (eq (car-safe item) 'theme-face)
                  (eq (cadr item) face)))
           settings))
         (spec (nth 3 entry))
         (graphical-properties (cadr (car spec))))
    (unless entry
      (helsing-test--fail "theme has no declaration for face %S" face))
    (plist-get graphical-properties attribute)))

(let* ((root (or (getenv "HELSING_ROOT")
                 (helsing-test--fail "HELSING_ROOT is not set")))
       (theme-dir (expand-file-name "themes/doom-emacs" root)))
  (load (expand-file-name "checks/emacs-inspect.el" root) nil nil)
  (helsing-test--assert
   (fboundp 'helsing-inspect-face-at-point)
   "inspection helper did not load")
  (add-to-list 'custom-theme-load-path theme-dir)
  (load-theme 'helsing t)

  (helsing-test--assert
   (custom-theme-enabled-p 'helsing)
   "theme did not enable")

  ;; Validate Doom colour aliases against the generated role contract.
  (dolist (entry helsing-test-role-aliases)
    (pcase-let ((`(,alias ,_role ,_token ,expected) entry))
      (let ((actual (doom-color alias)))
        (helsing-test--assert
         (helsing-test--same-color-p actual expected)
         "role alias %S resolved to %S, expected %S"
         alias actual expected))))

  ;; Verify all three colour branches registered by the Doom theme. This is a
  ;; deterministic fallback test; final TTY readability still needs a human.
  (dolist (entry helsing-test-terminal-contract)
    (pcase-let ((`(,name ,graphical ,ansi256 ,tty) entry))
      (let ((actual (cdr (assq name doom-themes--colors)))
            (expected (list graphical ansi256 tty)))
        (helsing-test--assert
         (equal actual expected)
         "terminal colour %S resolved to %S, expected %S"
         name actual expected))))

  ;; Validate the graphical branch registered by the enabled theme. Batch
  ;; Emacs has no colour display and otherwise reports unspecified-fg/bg.
  (dolist (entry helsing-test-face-contract)
    (let ((face (car entry))
          (properties (cdr entry)))
      (when (memq (plist-get properties :layer) '(core font_lock eglot))
        (helsing-test--assert (facep face) "face %S was not defined" face))
      (dolist (attribute '(:foreground :background :inherit))
        (when-let ((expected (plist-get properties attribute)))
          (let ((actual
                 (helsing-test--theme-face-attribute
                  'helsing face attribute)))
            (helsing-test--assert
             (if (eq attribute :inherit)
                 (eq actual expected)
               (helsing-test--same-color-p actual expected))
             "face %S has %S %S, expected %S"
             face attribute actual expected))))))

  ;; Exercise a real Font Lock path. Built-in Tree-sitter modes also assign
  ;; Font Lock faces, so this verifies the stable contract boundary.
  (with-temp-buffer
    (emacs-lisp-mode)
    (insert "(defun helsing-sample (value)\n"
            "  (if value\n"
            "      (message \"watch\")))\n")
    (font-lock-ensure)
    (dolist (expectation
             '(("defun" font-lock-keyword-face)
               ("helsing-sample" font-lock-function-name-face)
               ("if" font-lock-keyword-face)
               ("\"watch\"" font-lock-string-face)))
      (pcase-let ((`(,text ,expected-face) expectation))
        (let ((actual-face (helsing-test--face-at-text text)))
          (helsing-test--assert
           (helsing-test--face-includes-p actual-face expected-face)
           "fixture token %S has face %S, expected %S"
           text actual-face expected-face)))))

  ;; A theme must be safe to unload and reload in a running session.
  (disable-theme 'helsing)
  (helsing-test--assert
   (not (custom-theme-enabled-p 'helsing))
   "theme remained enabled after disable-theme")
  (load-theme 'helsing t)
  (helsing-test--assert
   (custom-theme-enabled-p 'helsing)
   "theme did not re-enable")
  (disable-theme 'helsing))

(message "Helsing Emacs theme checks passed")

;;; emacs-theme-test.el ends here
