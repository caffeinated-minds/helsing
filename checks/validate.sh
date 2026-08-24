#!/usr/bin/env bash

set -euo pipefail

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if [[ -x "$repo_root/.venv/bin/python" ]]; then
  python_bin="$repo_root/.venv/bin/python"
else
  python_bin=python3
fi

"$python_bin" "$repo_root/generator/generate.py" --check

mapping_body=$(sed -n '/^local function hl/,$p' "$repo_root/generator/templates/neovim/helsing.lua.j2")
if grep -Eq '#[0-9A-Fa-f]{6}' <<<"$mapping_body"; then
  echo "Neovim mappings contain a literal colour outside the palette table." >&2
  exit 1
fi

if command -v nvim >/dev/null 2>&1; then
  runtime_dir=$(mktemp -d)
  trap 'rm -rf -- "$runtime_dir"' EXIT

  HELSING_ROOT="$repo_root" \
    NVIM_LOG_FILE="$runtime_dir/nvim.log" \
    XDG_RUNTIME_DIR="$runtime_dir" \
    nvim -u NONE -i NONE -n --headless \
    '+lua local seen = {}; local set_hl = vim.api.nvim_set_hl; vim.api.nvim_set_hl = function(ns, name, opts) assert(not seen[name], "duplicate highlight declaration: " .. name); seen[name] = true; return set_hl(ns, name, opts) end; dofile(vim.env.HELSING_ROOT .. "/themes/neovim/helsing.lua"); assert(vim.g.colors_name == "helsing", "Helsing did not load")' \
    +qa
else
  echo "Skipping Neovim runtime validation: nvim is not installed."
fi

echo "Helsing validation passed."
