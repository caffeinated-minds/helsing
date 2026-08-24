#!/usr/bin/env bash

set -euo pipefail

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if [[ -x "$repo_root/.venv/bin/python" ]]; then
  python_bin="$repo_root/.venv/bin/python"
else
  python_bin=python3
fi

"$python_bin" "$repo_root/generator/generate.py" --check

mapping_body=$(sed -n '/^local function hl/,$p' "$repo_root/themes/neovim/helsing.lua")
if grep -Eq '#[0-9A-Fa-f]{6}' <<<"$mapping_body"; then
  echo "Neovim mappings contain a literal colour outside the palette table." >&2
  exit 1
fi

if grep -Eq 'nvim_create_(autocmd|augroup)|vim\.defer_fn|VeryLazy' \
  "$repo_root/themes/neovim/helsing.lua"; then
  echo "The public Neovim colour scheme contains plugin lifecycle behaviour." >&2
  exit 1
fi

while IFS= read -r source_file; do
  if awk 'length($0) > 120 { exit 1 }' "$source_file"; then
    continue
  fi
  echo "Neovim source exceeds 120 columns: ${source_file#"$repo_root/"}" >&2
  exit 1
done < <(find "$repo_root/generator/templates/neovim" -type f -name '*.j2' -print)

if command -v nvim >/dev/null 2>&1; then
  runtime_dir=$(mktemp -d)
  trap 'rm -rf -- "$runtime_dir"' EXIT

  HELSING_ROOT="$repo_root" \
    NVIM_LOG_FILE="$runtime_dir/nvim.log" \
    XDG_RUNTIME_DIR="$runtime_dir" \
    nvim -u NONE -i NONE -n --headless \
    '+lua local seen = {}; local set_hl = vim.api.nvim_set_hl; vim.api.nvim_set_hl = function(ns, name, opts) assert(not seen[name], "duplicate highlight declaration: " .. name); seen[name] = true; return set_hl(ns, name, opts) end; dofile(vim.env.HELSING_ROOT .. "/themes/neovim/helsing.lua"); assert(vim.g.colors_name == "helsing", "Helsing did not load"); local integration = dofile(vim.env.HELSING_ROOT .. "/themes/neovim/lua/helsing/integrations/bufferline.lua"); local opts = integration.apply({}); assert(type(opts.highlights) == "function", "Bufferline integration did not configure highlights")' \
    +qa
else
  echo "Skipping Neovim runtime validation: nvim is not installed."
fi

doom_themes_dir=""
for candidate in \
  "$HOME/.config/emacs/.local/straight/build-"*/doom-themes \
  "$HOME/.config/emacs/.local/straight/repos/themes"; do
  if [[ -f "$candidate/doom-themes.el" ]]; then
    doom_themes_dir="$candidate"
    break
  fi
done

if command -v emacs >/dev/null 2>&1 && [[ -n "$doom_themes_dir" ]]; then
  HELSING_THEME_DIR="$repo_root/themes/doom-emacs" \
    emacs --batch -Q -L "$doom_themes_dir" \
    --eval '(progn
      (require '\''doom-themes'')
      (add-to-list '\''custom-theme-load-path (getenv "HELSING_THEME_DIR"))
      (load-theme '\''helsing t)
      (unless (custom-theme-enabled-p '\''helsing)
        (error "Helsing Doom theme did not enable"))
      (unless (equal (cdr (assq '\''bg doom-themes--colors))
                     '\''("#F4F1EA" "white" "white"))
        (error "Helsing Doom background token is incorrect"))
      (unless (equal (cdr (assq '\''fg doom-themes--colors))
                     '\''("#2A2A2A" "black" "black"))
        (error "Helsing Doom foreground token is incorrect"))
      (disable-theme '\''helsing))'
else
  echo "Skipping Doom Emacs runtime validation: Emacs or doom-themes is not installed."
fi

echo "Helsing validation passed."
