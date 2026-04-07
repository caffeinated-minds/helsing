-- helsing.lua
-- A light Neovim colourscheme inspired by the idea of a daylight counterpart to Dracula.

if vim.g.colors_name then
  vim.cmd("highlight clear")
end

if vim.fn.exists("syntax_on") then
  vim.cmd("syntax reset")
end

vim.o.background = "light"
vim.g.colors_name = "helsing"

local c = {
  -- Base
  bg        = "#F4F1EA",
  bg_alt    = "#EAE5DC",
  fg        = "#2A2A2A",
  muted     = "#6B6B6B",
  subtle    = "#A8A29E",
  border    = "#D6D0C4",
  selection = "#E6DCC8",

  -- Accents
  purple    = "#7C6EE6",
  blue      = "#3A7BD5",
  green     = "#4C9A5F",
  orange    = "#C47A2C",
  cyan      = "#2F8F8B",
  pink      = "#C05A8C",
  red       = "#C23B3B",
  yellow    = "#B58900",

  -- Extra UI tones
  diff_add    = "#DCEEDB",
  diff_change = "#E8E1F3",
  diff_delete = "#F3D9D9",
  search      = "#F1E7B8",
  incsearch   = "#E8D58B",
  cursorline  = "#EFE9DF",
  linenr      = "#B3ADA4",
  visual      = "#E6DCC8",
  pmenu       = "#ECE7DE",
  pmenu_sel   = "#DDD4C5",
}

local function hl(group, opts)
  vim.api.nvim_set_hl(0, group, opts)
end

-- Editor UI
hl("Normal",       { fg = c.fg, bg = c.bg })
hl("NormalFloat",  { fg = c.fg, bg = c.bg_alt })
hl("FloatBorder",  { fg = c.border, bg = c.bg_alt })
hl("ColorColumn",  { bg = c.bg_alt })
hl("Cursor",       { fg = c.bg, bg = c.fg })
hl("CursorLine",   { bg = c.cursorline })
hl("CursorColumn", { bg = c.cursorline })
hl("CursorLineNr", { fg = c.orange, bg = c.cursorline, bold = true })
hl("LineNr",       { fg = c.linenr, bg = c.bg })
hl("SignColumn",   { fg = c.subtle, bg = c.bg })
hl("EndOfBuffer",  { fg = c.border, bg = c.bg })
hl("VertSplit",    { fg = c.border, bg = c.bg })
hl("WinSeparator", { fg = c.border, bg = c.bg })
hl("Folded",       { fg = c.muted, bg = c.bg_alt })
hl("FoldColumn",   { fg = c.subtle, bg = c.bg })
hl("MatchParen",   { fg = c.red, bg = c.selection, bold = true })
hl("Visual",       { bg = c.visual })
hl("VisualNOS",    { bg = c.visual })
hl("Search",       { fg = c.fg, bg = c.search })
hl("IncSearch",    { fg = c.fg, bg = c.incsearch, bold = true })
hl("CurSearch",    { fg = c.fg, bg = c.incsearch, bold = true })
hl("Pmenu",        { fg = c.fg, bg = c.pmenu })
hl("PmenuSel",     { fg = c.fg, bg = c.pmenu_sel, bold = true })
hl("PmenuSbar",    { bg = c.bg_alt })
hl("PmenuThumb",   { bg = c.subtle })
hl("StatusLine",   { fg = c.fg, bg = c.bg_alt })
hl("StatusLineNC", { fg = c.muted, bg = c.bg_alt })
hl("TabLine",      { fg = c.muted, bg = c.bg_alt })
hl("TabLineFill",  { bg = c.bg_alt })
hl("TabLineSel",   { fg = c.fg, bg = c.bg, bold = true })
hl("Title",        { fg = c.blue, bold = true })
hl("Directory",    { fg = c.blue, bold = true })
hl("NonText",      { fg = c.border })
hl("Whitespace",   { fg = c.border })
hl("SpecialKey",   { fg = c.subtle })

-- Syntax
hl("Comment",      { fg = c.muted, italic = true })
hl("Constant",     { fg = c.pink })
hl("String",       { fg = c.green })
hl("Character",    { fg = c.green })
hl("Number",       { fg = c.orange })
hl("Boolean",      { fg = c.orange, bold = true })
hl("Float",        { fg = c.orange })
hl("Identifier",   { fg = c.fg })
hl("Function",     { fg = c.blue })
hl("Statement",    { fg = c.purple })
hl("Conditional",  { fg = c.purple })
hl("Repeat",       { fg = c.purple })
hl("Label",        { fg = c.purple })
hl("Operator",     { fg = c.red })
hl("Keyword",      { fg = c.purple })
hl("Exception",    { fg = c.purple })
hl("PreProc",      { fg = c.pink })
hl("Include",      { fg = c.purple })
hl("Define",       { fg = c.pink })
hl("Macro",        { fg = c.pink })
hl("PreCondit",    { fg = c.pink })
hl("Type",         { fg = c.cyan })
hl("StorageClass", { fg = c.cyan })
hl("Structure",    { fg = c.cyan })
hl("Typedef",      { fg = c.cyan })
hl("Special",      { fg = c.red })
hl("SpecialChar",  { fg = c.red })
hl("Tag",          { fg = c.blue })
hl("Delimiter",    { fg = c.subtle })
hl("SpecialComment", { fg = c.muted, italic = true })
hl("Debug",        { fg = c.red })
hl("Underlined",   { underline = true })
hl("Bold",         { bold = true })
hl("Italic",       { italic = true })
hl("Error",        { fg = c.red, bold = true })
hl("Todo",         { fg = c.yellow, bg = c.bg_alt, bold = true })

-- Diagnostics
hl("DiagnosticError",            { fg = c.red })
hl("DiagnosticWarn",             { fg = c.yellow })
hl("DiagnosticInfo",             { fg = c.blue })
hl("DiagnosticHint",             { fg = c.cyan })
hl("DiagnosticOk",               { fg = c.green })

hl("DiagnosticUnderlineError",   { undercurl = true, sp = c.red })
hl("DiagnosticUnderlineWarn",    { undercurl = true, sp = c.yellow })
hl("DiagnosticUnderlineInfo",    { undercurl = true, sp = c.blue })
hl("DiagnosticUnderlineHint",    { undercurl = true, sp = c.cyan })

hl("DiagnosticVirtualTextError", { fg = c.red, bg = c.bg_alt })
hl("DiagnosticVirtualTextWarn",  { fg = c.yellow, bg = c.bg_alt })
hl("DiagnosticVirtualTextInfo",  { fg = c.blue, bg = c.bg_alt })
hl("DiagnosticVirtualTextHint",  { fg = c.cyan, bg = c.bg_alt })

hl("DiagnosticSignError",        { fg = c.red, bg = c.bg })
hl("DiagnosticSignWarn",         { fg = c.yellow, bg = c.bg })
hl("DiagnosticSignInfo",         { fg = c.blue, bg = c.bg })
hl("DiagnosticSignHint",         { fg = c.cyan, bg = c.bg })

-- Diff / Git
hl("DiffAdd",    { bg = c.diff_add })
hl("DiffChange", { bg = c.diff_change })
hl("DiffDelete", { bg = c.diff_delete })
hl("DiffText",   { bg = c.selection, bold = true })

hl("Added",      { fg = c.green })
hl("Changed",    { fg = c.purple })
hl("Removed",    { fg = c.red })

-- Spelling
hl("SpellBad",   { undercurl = true, sp = c.red })
hl("SpellCap",   { undercurl = true, sp = c.blue })
hl("SpellRare",  { undercurl = true, sp = c.purple })
hl("SpellLocal", { undercurl = true, sp = c.cyan })

-- Treesitter fallbacks
hl("@comment",             { link = "Comment" })
hl("@comment.todo",        { link = "Todo" })
hl("@constant",            { link = "Constant" })
hl("@constant.builtin",    { fg = c.pink, italic = true })
hl("@string",              { link = "String" })
hl("@string.escape",       { fg = c.red })
hl("@character",           { link = "Character" })
hl("@number",              { link = "Number" })
hl("@boolean",             { link = "Boolean" })
hl("@function",            { link = "Function" })
hl("@function.call",       { link = "Function" })
hl("@function.builtin",    { fg = c.blue, italic = true })
hl("@method",              { fg = c.blue })
hl("@method.call",         { fg = c.blue })
hl("@constructor",         { fg = c.cyan })
hl("@parameter",           { fg = c.fg })
hl("@keyword",             { link = "Keyword" })
hl("@keyword.function",    { fg = c.purple })
hl("@keyword.return",      { fg = c.purple, italic = true })
hl("@conditional",         { link = "Conditional" })
hl("@repeat",              { link = "Repeat" })
hl("@operator",            { link = "Operator" })
hl("@type",                { link = "Type" })
hl("@type.builtin",        { fg = c.cyan, italic = true })
hl("@property",            { fg = c.fg })
hl("@field",               { fg = c.fg })
hl("@variable",            { fg = c.fg })
hl("@variable.builtin",    { fg = c.red, italic = true })
hl("@punctuation.delimiter", { fg = c.subtle })
hl("@punctuation.bracket", { fg = c.subtle })
hl("@tag",                 { link = "Tag" })
hl("@tag.attribute",       { fg = c.orange })
hl("@tag.delimiter",       { fg = c.subtle })

-- Common plugin groups
hl("GitSignsAdd",          { fg = c.green, bg = c.bg })
hl("GitSignsChange",       { fg = c.purple, bg = c.bg })
hl("GitSignsDelete",       { fg = c.red, bg = c.bg })

hl("TelescopeNormal",      { fg = c.fg, bg = c.bg_alt })
hl("TelescopeBorder",      { fg = c.border, bg = c.bg_alt })
hl("TelescopePromptNormal",{ fg = c.fg, bg = c.bg_alt })
hl("TelescopePromptBorder",{ fg = c.border, bg = c.bg_alt })
hl("TelescopeSelection",   { bg = c.selection, bold = true })
hl("TelescopeMatching",    { fg = c.blue, bold = true })

hl("NvimTreeNormal",       { fg = c.fg, bg = c.bg_alt })
hl("NvimTreeWinSeparator", { fg = c.border, bg = c.bg_alt })
hl("NvimTreeRootFolder",   { fg = c.blue, bold = true })
hl("NvimTreeFolderName",   { fg = c.blue })
hl("NvimTreeOpenedFolderName", { fg = c.blue, bold = true })
hl("NvimTreeEmptyFolderName",  { fg = c.muted })
hl("NvimTreeIndentMarker", { fg = c.border })

hl("WhichKey",             { fg = c.purple })
hl("WhichKeyGroup",        { fg = c.blue })
hl("WhichKeyDesc",         { fg = c.fg })
hl("WhichKeySeparator",    { fg = c.subtle })
hl("WhichKeyFloat",        { bg = c.bg_alt })

-- Markdown
hl("markdownH1",           { fg = c.blue, bold = true })
hl("markdownH2",           { fg = c.purple, bold = true })
hl("markdownH3",           { fg = c.cyan, bold = true })
hl("markdownCode",         { fg = c.green })
hl("markdownCodeBlock",    { fg = c.green })
hl("markdownItalic",       { italic = true })
hl("markdownBold",         { bold = true })
hl("markdownUrl",          { fg = c.blue, underline = true })
