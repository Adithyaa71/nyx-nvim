local M = {}

-- ============================================================
-- ROOT — change this one value to relocate the entire workstation
-- ============================================================
M.root = "/mnt/Obsidian/nvim"

-- ============================================================
-- RUNTIME — plugin installs, parsers, mason
-- ============================================================
M.lazy_root     = M.root .. "/runtime/lazy"       -- lazy.nvim install dir
M.lazy_self     = M.lazy_root .. "/lazy.nvim"     -- lazy.nvim itself
M.mason_root    = M.root .. "/runtime/mason"      -- mason packages
M.ts_install    = M.root .. "/runtime/treesitter" -- treesitter parsers

-- ============================================================
-- STATE — undo, swap, backup, sessions, shada
-- ============================================================
M.undo     = M.root .. "/state/undo"
M.swap     = M.root .. "/state/swap"
M.backup   = M.root .. "/state/backup"
M.sessions = M.root .. "/state/sessions"
M.shada    = M.root .. "/state/shada/main.shada"

-- ============================================================
-- CACHE / LOGS
-- ============================================================
M.cache = M.root .. "/cache"
M.logs  = M.root .. "/logs"

-- ============================================================
-- WORKSPACE
-- ============================================================
M.projects  = M.root .. "/projects"
M.repos     = M.root .. "/repos"
M.workspace = M.root .. "/workspace"
M.notes     = M.root .. "/notes"
M.scratch   = M.root .. "/scratch"

-- ============================================================
-- ZK — knowledge vault lives OUTSIDE nvim runtime hierarchy
-- Agent-agnostic: usable from Obsidian, terminal, and Neovim
-- ============================================================
M.zk_notebook = "/mnt/Obsidian/zk"

-- ============================================================
-- ENSURE — creates all required directories on startup
-- Call this once from init.lua before anything else loads
-- ============================================================
function M.ensure()
  local dirs = {
    M.lazy_root, M.mason_root, M.ts_install,
    M.undo, M.swap, M.backup, M.sessions,
    M.cache, M.logs,
    M.projects, M.repos, M.workspace, M.notes, M.scratch,
    vim.fn.fnamemodify(M.shada, ":h"), -- parent dir of shada file
  }
  for _, dir in ipairs(dirs) do
    vim.fn.mkdir(dir, "p")
  end
end

return M
