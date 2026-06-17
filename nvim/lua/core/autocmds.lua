local augroup = vim.api.nvim_create_augroup
local autocmd = vim.api.nvim_create_autocmd

-- ============================================================
-- TREESITTER HIGHLIGHTING — enable per filetype
-- New API for nvim-treesitter main branch + Nvim 0.12
-- ============================================================
local ts_group = augroup("TreesitterHighlight", { clear = true })
autocmd("FileType", {
  group = ts_group,
  pattern = {
    "lua", "python", "bash", "sh",
    "javascript", "typescript", "tsx", "jsx",
    "json", "yaml", "toml",
    "markdown", "markdown_inline",
    "dockerfile", "sql",
    "gitconfig", "gitignore", "gitcommit",
    "vim", "vimdoc", "query",
    "c", "cpp",
  },
  callback = function()
    pcall(vim.treesitter.start)
  end,
})

-- ============================================================
-- TREESITTER FOLDING — opt-in per buffer
-- ============================================================
autocmd("FileType", {
  group = ts_group,
  pattern = { "lua", "python", "javascript", "typescript" },
  callback = function()
    vim.wo[0][0].foldmethod = "expr"
    vim.wo[0][0].foldexpr   = "v:lua.vim.treesitter.foldexpr()"
    vim.wo[0][0].foldenable  = false  -- start unfolded
  end,
})

-- ============================================================
-- HIGHLIGHT ON YANK
-- ============================================================
autocmd("TextYankPost", {
  group = augroup("YankHighlight", { clear = true }),
  callback = function()
    vim.highlight.on_yank({ higroup = "IncSearch", timeout = 150 })
  end,
})

-- ============================================================
-- TRIM TRAILING WHITESPACE ON SAVE
-- ============================================================
autocmd("BufWritePre", {
  group = augroup("TrimWhitespace", { clear = true }),
  callback = function()
    local pos = vim.api.nvim_win_get_cursor(0)
    vim.cmd([[%s/\s\+$//e]])
    vim.api.nvim_win_set_cursor(0, pos)
  end,
})

-- ============================================================
-- RESIZE SPLITS ON WINDOW RESIZE
-- ============================================================
autocmd("VimResized", {
  group = augroup("ResizeSplits", { clear = true }),
  callback = function()
    vim.cmd("tabdo wincmd =")
  end,
})

-- ============================================================
-- RESTORE CURSOR POSITION
-- ============================================================
autocmd("BufReadPost", {
  group = augroup("RestoreCursor", { clear = true }),
  callback = function()
    local mark = vim.api.nvim_buf_get_mark(0, '"')
    local lcount = vim.api.nvim_buf_line_count(0)
    if mark[1] > 0 and mark[1] <= lcount then
      pcall(vim.api.nvim_win_set_cursor, 0, mark)
    end
  end,
})
