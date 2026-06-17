local paths = require("util.paths")

local opt = vim.opt

-- ============================================================
-- STORAGE — redirect all state to NVMe
-- ============================================================
opt.undofile   = true
opt.undodir    = { paths.undo }
opt.swapfile   = true
opt.directory  = { paths.swap }
opt.backup     = true
opt.backupdir  = { paths.backup }
opt.shadafile  = paths.shada

-- ============================================================
-- EDITOR
-- ============================================================
opt.number         = true
opt.relativenumber = true
opt.signcolumn     = "yes"
opt.cursorline     = true
opt.wrap           = false
opt.scrolloff      = 8
opt.sidescrolloff  = 8

-- ============================================================
-- INDENTATION
-- ============================================================
opt.tabstop     = 2
opt.shiftwidth  = 2
opt.expandtab   = true
opt.smartindent = true

-- ============================================================
-- SEARCH
-- ============================================================
opt.ignorecase = true
opt.smartcase  = true
opt.hlsearch   = false
opt.incsearch  = true

-- ============================================================
-- APPEARANCE
-- ============================================================
opt.termguicolors = true
opt.showmode      = false   -- lualine will show this later
opt.cmdheight     = 1
opt.pumheight     = 10      -- completion menu height

-- ============================================================
-- PERFORMANCE (important on Pi 5)
-- ============================================================
opt.updatetime  = 250
opt.timeoutlen  = 400
opt.redrawtime  = 1500

-- ============================================================
-- SPLITS
-- ============================================================
opt.splitright = true
opt.splitbelow = true

-- ============================================================
-- MISC
-- ============================================================
opt.mouse      = "a"
opt.clipboard  = "unnamedplus"
opt.completeopt = { "menu", "menuone", "noselect" }
opt.fileencoding = "utf-8"
opt.conceallevel = 0

-- MCP socket for Nyx agent
local nyx_socket = '/tmp/nvim-' .. vim.fn.getpid() .. '.sock'
vim.fn.serverstart(nyx_socket)
vim.g.nvim_socket_path = nyx_socket
