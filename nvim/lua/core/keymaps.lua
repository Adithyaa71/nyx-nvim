vim.g.mapleader      = " "
vim.g.maplocalleader = "\\"

local map = function(mode, lhs, rhs, opts)
  opts = opts or {}
  opts.silent = opts.silent ~= false
  vim.keymap.set(mode, lhs, rhs, opts)
end

-- ============================================================
-- WINDOW NAVIGATION
-- ============================================================
map("n", "<C-h>", "<C-w>h", { desc = "Window left" })
map("n", "<C-l>", "<C-w>l", { desc = "Window right" })
map("n", "<C-j>", "<C-w>j", { desc = "Window down" })
map("n", "<C-k>", "<C-w>k", { desc = "Window up" })

-- ============================================================
-- BUFFER
-- ============================================================
map("n", "<leader>bd", "<cmd>bdelete<cr>",   { desc = "Delete buffer" })
map("n", "<leader>bn", "<cmd>bnext<cr>",     { desc = "Next buffer" })
map("n", "<leader>bp", "<cmd>bprevious<cr>", { desc = "Prev buffer" })

-- ============================================================
-- FILE SAVE / QUIT
-- ============================================================
map("n", "<leader>w", "<cmd>w<cr>",  { desc = "Save" })
map("n", "<leader>q", "<cmd>q<cr>",  { desc = "Quit" })
map("n", "<leader>Q", "<cmd>qa<cr>", { desc = "Quit all" })

-- ============================================================
-- MISC
-- ============================================================
map("n", "<Esc>", "<cmd>nohlsearch<cr>", { desc = "Clear search" })
map("v", "<",     "<gv",                 { desc = "Indent left" })
map("v", ">",     ">gv",                 { desc = "Indent right" })
map("n", "<leader>e", "<cmd>Explore<cr>", { desc = "Explorer" })
