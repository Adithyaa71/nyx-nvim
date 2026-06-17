-- FILE: lua/plugins/gitsigns.lua

return {
  {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPost", "BufNewFile" },
    opts = {
      signs = {
        add          = { text = "▎" },
        change       = { text = "▎" },
        delete       = { text = "" },
        topdelete    = { text = "" },
        changedelete = { text = "▎" },
        untracked    = { text = "▎" },
      },
      on_attach = function(buffer)
        local gs = package.loaded.gitsigns
        local map = function(mode, lhs, rhs, desc)
          vim.keymap.set(mode, lhs, rhs, { buffer = buffer, desc = desc })
        end

        -- Navigation
        map("n", "]h", gs.next_hunk,           "Next hunk")
        map("n", "[h", gs.prev_hunk,           "Prev hunk")

        -- Actions
        map("n", "<leader>gs", gs.stage_hunk,  "Stage hunk")
        map("n", "<leader>gr", gs.reset_hunk,  "Reset hunk")
        map("n", "<leader>gS", gs.stage_buffer,"Stage buffer")
        map("n", "<leader>gR", gs.reset_buffer,"Reset buffer")
        map("n", "<leader>gp", gs.preview_hunk,"Preview hunk")
        map("n", "<leader>gb", function()
          gs.blame_line({ full = true })
        end, "Blame line")
        map("n", "<leader>gd", gs.diffthis,    "Diff this")
        map("n", "<leader>gD", function()
          gs.diffthis("~")
        end, "Diff HEAD~")

        -- Toggle
        map("n", "<leader>gtb", gs.toggle_current_line_blame, "Toggle blame")
        map("n", "<leader>gtd", gs.toggle_deleted,            "Toggle deleted")
      end,
    },
  },
}
