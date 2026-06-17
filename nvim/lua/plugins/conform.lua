-- FILE: lua/plugins/conform.lua
-- Formatter: conform.nvim
-- Formatters are installed via Mason separately (mason-tool-installer or manually)

return {
  {
    "stevearc/conform.nvim",
    event = { "BufWritePre" },
    cmd   = { "ConformInfo" },
    opts = {
      formatters_by_ft = {
        lua        = { "stylua" },
        python     = { "black", "isort" },
        javascript = { "prettier" },
        typescript = { "prettier" },
        tsx        = { "prettier" },
        jsx        = { "prettier" },
        json       = { "prettier" },
        yaml       = { "prettier" },
        toml       = { "taplo" },
        markdown   = { "prettier" },
        bash       = { "shfmt" },
        sh         = { "shfmt" },
        ["*"]      = { "trim_whitespace" },
      },
      format_on_save = {
        timeout_ms   = 1000,
        lsp_fallback = true,
      },
      formatters = {
        shfmt = {
          prepend_args = { "-i", "2", "-ci" },
        },
      },
    },
  },
}
