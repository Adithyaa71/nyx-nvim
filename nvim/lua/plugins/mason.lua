-- FILE: lua/plugins/mason.lua
-- NOTE: mason-org/mason.nvim is the new org name (same plugin)
-- install_root_dir redirects all LSP servers/formatters to NVMe

local paths = require("util.paths")

return {
  {
    "mason-org/mason.nvim",
    build = ":MasonUpdate",
    opts = {
      install_root_dir = paths.mason_root,
      ui = {
        border = "rounded",
        icons = {
          package_installed   = "✓",
          package_pending     = "➜",
          package_uninstalled = "✗",
        },
      },
      max_concurrent_installers = 2, -- conservative for Pi 5
    },
  },
}
