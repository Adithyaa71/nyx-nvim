-- FILE: lua/plugins/autopairs.lua

return {
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",
    opts = {
      check_ts        = true,   -- use treesitter to check pairs
      ts_config       = {
        lua  = { "string", "source" },
        javascript = { "string", "template_string" },
      },
      disable_filetype = { "TelescopePrompt" },
      fast_wrap = {
        map     = "<M-e>",
        chars   = { "{", "[", "(", '"', "'" },
        pattern = [=[[%'%"%>%]%)%}%,]]=],
        offset  = 0,
        end_key = "$",
        keys    = "qwertyuiopzxcvbnmasdfghjkl",
        check_comma = true,
        highlight   = "PmenuSel",
      },
    },
  },
}
