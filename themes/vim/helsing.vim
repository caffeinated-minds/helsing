" Helsing for Vim, generated from the canonical cortadOS theme snapshot.
" Semantic mapping follows ~/Code/helsing/docs/helsing-theme-spec.md.

if exists('syntax_on')
  syntax reset
endif
set background=light
let g:colors_name = 'helsing'

let s:bg = '#F4F1EA'
let s:bg_alt = '#EAE5DC'
let s:fg = '#2A2A2A'
let s:muted = '#6B6B6B'
let s:subtle = '#A8A29E'
let s:border = '#D6D0C4'
let s:selection = '#E6DCC8'
let s:purple = '#7C6EE6'
let s:blue = '#3A7BD5'
let s:green = '#4C9A5F'
let s:orange = '#C47A2C'
let s:cyan = '#2F8F8B'
let s:pink = '#C05A8C'
let s:red = '#C23B3B'
let s:yellow = '#B58900'
let s:info = '#4A90E2'

execute 'highlight Normal guifg=' . s:fg . ' guibg=' . s:bg . ' ctermfg=235 ctermbg=255'
execute 'highlight NormalNC guifg=' . s:fg . ' guibg=' . s:bg . ' ctermfg=235 ctermbg=255'
execute 'highlight Cursor guifg=' . s:bg . ' guibg=' . s:fg . ' ctermfg=255 ctermbg=235'
execute 'highlight CursorLine guibg=' . s:bg_alt . ' ctermbg=254'
execute 'highlight CursorColumn guibg=' . s:bg_alt . ' ctermbg=254'
execute 'highlight ColorColumn guibg=' . s:bg_alt . ' ctermbg=254'
execute 'highlight LineNr guifg=' . s:subtle . ' guibg=' . s:bg . ' ctermfg=248 ctermbg=255'
execute 'highlight CursorLineNr guifg=' . s:fg . ' guibg=' . s:bg_alt . ' gui=bold ctermfg=235 ctermbg=254 cterm=bold'
execute 'highlight Visual guifg=' . s:fg . ' guibg=' . s:selection . ' ctermfg=235 ctermbg=253'
execute 'highlight Search guifg=' . s:fg . ' guibg=' . s:yellow . ' ctermfg=235 ctermbg=136'
execute 'highlight IncSearch guifg=' . s:bg . ' guibg=' . s:orange . ' ctermfg=255 ctermbg=172'
execute 'highlight MatchParen guifg=' . s:purple . ' guibg=' . s:selection . ' gui=bold ctermfg=99 ctermbg=253 cterm=bold'

execute 'highlight StatusLine guifg=' . s:fg . ' guibg=' . s:selection . ' gui=bold ctermfg=235 ctermbg=253 cterm=bold'
execute 'highlight StatusLineNC guifg=' . s:muted . ' guibg=' . s:bg_alt . ' ctermfg=242 ctermbg=254'
execute 'highlight VertSplit guifg=' . s:border . ' guibg=' . s:bg . ' ctermfg=252 ctermbg=255'
execute 'highlight WinSeparator guifg=' . s:border . ' guibg=' . s:bg . ' ctermfg=252 ctermbg=255'
execute 'highlight Pmenu guifg=' . s:fg . ' guibg=' . s:bg_alt . ' ctermfg=235 ctermbg=254'
execute 'highlight PmenuSel guifg=' . s:fg . ' guibg=' . s:selection . ' gui=bold ctermfg=235 ctermbg=253 cterm=bold'
execute 'highlight WildMenu guifg=' . s:bg . ' guibg=' . s:blue . ' ctermfg=255 ctermbg=68'
execute 'highlight Folded guifg=' . s:muted . ' guibg=' . s:bg_alt . ' ctermfg=242 ctermbg=254'
execute 'highlight SignColumn guibg=' . s:bg . ' ctermbg=255'
execute 'highlight NonText guifg=' . s:subtle . ' ctermfg=248'
execute 'highlight SpecialKey guifg=' . s:subtle . ' ctermfg=248'
execute 'highlight Directory guifg=' . s:blue . ' ctermfg=68'
execute 'highlight Title guifg=' . s:purple . ' gui=bold ctermfg=99 cterm=bold'

execute 'highlight Comment guifg=' . s:muted . ' gui=italic ctermfg=242 cterm=italic'
execute 'highlight Constant guifg=' . s:pink . ' ctermfg=168'
execute 'highlight String guifg=' . s:green . ' ctermfg=71'
execute 'highlight Character guifg=' . s:green . ' ctermfg=71'
execute 'highlight Number guifg=' . s:orange . ' ctermfg=172'
execute 'highlight Boolean guifg=' . s:orange . ' gui=bold ctermfg=172 cterm=bold'
execute 'highlight Float guifg=' . s:orange . ' ctermfg=172'
execute 'highlight Identifier guifg=' . s:blue . ' ctermfg=68'
execute 'highlight Function guifg=' . s:blue . ' ctermfg=68'
execute 'highlight Statement guifg=' . s:purple . ' gui=bold ctermfg=99 cterm=bold'
execute 'highlight Keyword guifg=' . s:purple . ' gui=bold ctermfg=99 cterm=bold'
execute 'highlight Operator guifg=' . s:purple . ' ctermfg=99'
execute 'highlight PreProc guifg=' . s:pink . ' ctermfg=168'
execute 'highlight Type guifg=' . s:cyan . ' ctermfg=30'
execute 'highlight StorageClass guifg=' . s:cyan . ' ctermfg=30'
execute 'highlight Structure guifg=' . s:cyan . ' ctermfg=30'
execute 'highlight Typedef guifg=' . s:cyan . ' ctermfg=30'
execute 'highlight Special guifg=' . s:orange . ' ctermfg=172'
execute 'highlight Underlined guifg=' . s:blue . ' gui=underline ctermfg=68 cterm=underline'
execute 'highlight Todo guifg=' . s:bg . ' guibg=' . s:yellow . ' gui=bold ctermfg=255 ctermbg=136 cterm=bold'
execute 'highlight Error guifg=' . s:red . ' guibg=' . s:bg . ' gui=bold ctermfg=167 ctermbg=255 cterm=bold'
execute 'highlight ErrorMsg guifg=' . s:red . ' guibg=' . s:bg . ' gui=bold ctermfg=167 ctermbg=255 cterm=bold'
execute 'highlight WarningMsg guifg=' . s:yellow . ' guibg=' . s:bg . ' gui=bold ctermfg=136 ctermbg=255 cterm=bold'
execute 'highlight MoreMsg guifg=' . s:green . ' ctermfg=71'
execute 'highlight Question guifg=' . s:info . ' ctermfg=68'
execute 'highlight ModeMsg guifg=' . s:blue . ' gui=bold ctermfg=68 cterm=bold'

execute 'highlight DiffAdd guifg=' . s:green . ' guibg=' . s:bg_alt . ' ctermfg=71 ctermbg=254'
execute 'highlight DiffChange guifg=' . s:purple . ' guibg=' . s:bg_alt . ' ctermfg=99 ctermbg=254'
execute 'highlight DiffDelete guifg=' . s:red . ' guibg=' . s:bg_alt . ' ctermfg=167 ctermbg=254'
execute 'highlight DiffText guifg=' . s:fg . ' guibg=' . s:selection . ' gui=bold ctermfg=235 ctermbg=253 cterm=bold'

highlight! link htmlTag Type
highlight! link htmlArg Identifier
" Match Neovim's Tree-sitter Markdown heading hierarchy.
execute 'highlight markdownH1 guifg=' . s:blue . ' gui=bold ctermfg=68 cterm=bold'
execute 'highlight markdownH2 guifg=' . s:purple . ' gui=bold ctermfg=99 cterm=bold'
execute 'highlight markdownH3 guifg=' . s:cyan . ' gui=bold ctermfg=30 cterm=bold'
execute 'highlight markdownH4 guifg=' . s:green . ' gui=bold ctermfg=71 cterm=bold'
execute 'highlight markdownH5 guifg=' . s:orange . ' gui=bold ctermfg=172 cterm=bold'
execute 'highlight markdownH6 guifg=' . s:pink . ' gui=bold ctermfg=168 cterm=bold'
highlight! link markdownHeadingDelimiter Keyword
highlight! link markdownCode String
highlight! link yamlKey Identifier
highlight! link jsonKeyword Identifier
highlight! link shVariable Identifier
highlight! link pythonBuiltin Type
