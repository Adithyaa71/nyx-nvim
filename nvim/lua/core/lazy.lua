local paths = require("util.paths")

-- Bootstrap lazy.nvim if not present
if not vim.uv.fs_stat(paths.lazy_self) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    paths.lazy_self,
  })
end

-- Add lazy.nvim to runtime
vim.opt.rtp:prepend(paths.lazy_self)

require("lazy").setup({
  -- All plugin specs live in lua/plugins/ as individual files
  spec = {
    { import = "plugins" },
  },

  -- ============================================================
  -- REDIRECT all plugin installs to NVMe
  -- ============================================================
  root = paths.lazy_root,

  -- Lockfile stays in config dir (git-tracked)
  lockfile = vim.fn.stdpath("config") .. "/lazy-lock.json",

  defaults = {
    lazy = false,
  },

  install = {
    missing = true,
    colorscheme = { "habamax" },
  },

  checker = {
    enabled = false, -- manual updates only; saves CPU on Pi
  },

  performance = {
    rtp = {
      disabled_plugins = {
        "gzip", "matchit", "matchparen",
        "netrwPlugin", "tarPlugin", "tohtml",
        "tutor", "zipPlugin",
      },
    },
  },

  ui = {
    border = "rounded",
  },
})
