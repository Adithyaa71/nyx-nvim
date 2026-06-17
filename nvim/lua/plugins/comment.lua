-- FILE: lua/plugins/comment.lua

return {
  {
    "numToStr/Comment.nvim",
    event = { "BufReadPost", "BufNewFile" },
    opts = {
      -- gcc  = toggle line comment
      -- gbc  = toggle block comment
      -- gc   = line comment operator (visual + motion)
      -- gb   = block comment operator (visual + motion)
      padding   = true,
      sticky    = true,
      ignore    = nil,
      toggler   = { line = "gcc", block = "gbc" },
      opleader  = { line = "gc",  block = "gb" },
      extra     = {
        above = "gcO",
        below = "gco",
        eol   = "gcA",
      },
      mappings  = { basic = true, extra = true },
    },
  },
}
