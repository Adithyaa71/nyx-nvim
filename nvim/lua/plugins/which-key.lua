-- FILE: lua/plugins/which-key.lua

return {
  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    opts = {
      preset = "modern",
      delay  = 400,
      win = {
        border = "rounded",
      },
      spec = {
        -- Register leader group prefixes so which-key shows labels
        { "<leader>b", group = "Buffer" },
        { "<leader>f", group = "Find" },       -- Telescope later
        { "<leader>g", group = "Git" },        -- Gitsigns later
        { "<leader>l", group = "LSP" },        -- LSP later
        { "<leader>s", group = "Swap/Search" },
        { "<leader>z", group = "Zk / Notes" }, -- zk later
      },
    },
    keys = {
      {
        "<leader>?",
        function() require("which-key").show({ global = false }) end,
        desc = "Buffer keymaps",
      },
    },
  },
}
