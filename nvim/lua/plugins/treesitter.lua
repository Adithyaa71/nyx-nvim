-- FILE: lua/plugins/treesitter.lua
-- BRANCH: main (full rewrite, Nvim 0.12+ only)
-- API: require("nvim-treesitter").setup{} — NOT configs.setup

local paths = require("util.paths")

return {
  {
    "nvim-treesitter/nvim-treesitter",
    branch = "main",
    lazy = false,          -- must NOT be lazy-loaded per upstream docs
    build = ":TSUpdate",
    config = function()
      require("nvim-treesitter").setup({
        -- Redirect parsers to NVMe
        -- This prepends install_dir to runtimepath so parsers are found
        install_dir = paths.ts_install,
      })

      -- Install Phase 1 parsers
      -- This is async; run :TSUpdate after first launch to confirm
      require("nvim-treesitter").install({
        "lua", "python", "bash",
        "javascript", "typescript", "tsx",
        "json", "yaml", "toml",
        "markdown", "markdown_inline",
        "dockerfile", "sql",
        "gitcommit", "git_config", "gitignore",
        "vim", "vimdoc", "query",
        "c",
      })
    end,
  },
}
