-- FILE: lua/plugins/treesitter-textobjects.lua
-- BRANCH: main (compatible with treesitter main + Nvim 0.12)
-- NOTE: master branch uses old configs.setup API — do NOT use master

return {
  {
    "nvim-treesitter/nvim-treesitter-textobjects",
    branch = "main",
    dependencies = {
      { "nvim-treesitter/nvim-treesitter", branch = "main" },
    },
    lazy = false,
    config = function()
      require("nvim-treesitter-textobjects").setup({
        select = {
          enable = true,
          lookahead = true,
          keymaps = {
            ["af"] = { query = "@function.outer", desc = "outer function" },
            ["if"] = { query = "@function.inner", desc = "inner function" },
            ["ac"] = { query = "@class.outer",    desc = "outer class" },
            ["ic"] = { query = "@class.inner",    desc = "inner class" },
            ["aa"] = { query = "@parameter.outer", desc = "outer argument" },
            ["ia"] = { query = "@parameter.inner", desc = "inner argument" },
            ["ab"] = { query = "@block.outer",     desc = "outer block" },
            ["ib"] = { query = "@block.inner",     desc = "inner block" },
          },
        },
        move = {
          enable = true,
          set_jumps = true,
          goto_next_start = {
            ["]f"] = { query = "@function.outer", desc = "Next function start" },
            ["]c"] = { query = "@class.outer",    desc = "Next class start" },
          },
          goto_next_end = {
            ["]F"] = { query = "@function.outer", desc = "Next function end" },
            ["]C"] = { query = "@class.outer",    desc = "Next class end" },
          },
          goto_previous_start = {
            ["[f"] = { query = "@function.outer", desc = "Prev function start" },
            ["[c"] = { query = "@class.outer",    desc = "Prev class start" },
          },
          goto_previous_end = {
            ["[F"] = { query = "@function.outer", desc = "Prev function end" },
            ["[C"] = { query = "@class.outer",    desc = "Prev class end" },
          },
        },
        swap = {
          enable = true,
          swap_next = {
            ["<leader>sa"] = { query = "@parameter.inner", desc = "Swap next param" },
          },
          swap_previous = {
            ["<leader>sA"] = { query = "@parameter.inner", desc = "Swap prev param" },
          },
        },
      })
    end,
  },
}
