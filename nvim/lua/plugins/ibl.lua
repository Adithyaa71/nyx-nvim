-- FILE: lua/plugins/ibl.lua
-- PLUGIN: indent-blankline v3 (module name is "ibl", not "indent_blankline")

return {
  {
    "lukas-reineke/indent-blankline.nvim",
    main = "ibl",
    event = { "BufReadPost", "BufNewFile" },
    opts = {
      indent = {
        char      = "│",
        tab_char  = "│",
      },
      scope = {
        enabled    = true,
        show_start = true,
        show_end   = false,
      },
      exclude = {
        filetypes = {
          "help", "dashboard", "lazy", "mason",
          "neo-tree", "trouble", "Trouble",
          "notify", "toggleterm",
        },
      },
    },
  },
}
