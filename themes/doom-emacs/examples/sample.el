;;; sample.el --- Helsing Emacs Lisp fixture -*- lexical-binding: t; -*-

(defconst helsing-watch-interval 30
  "Seconds between archive inspections.")

(defun helsing-inspect-archive (path &optional verbose)
  "Inspect PATH and report its status when VERBOSE is non-nil."
  (let ((available (file-directory-p path)))
    (when verbose
      (message "Archive %s is %s"
               path
               (if available "ready" "missing")))
    available))

(provide 'helsing-sample)
;;; sample.el ends here
