-- FILE: lua/plugins/lsp.lua
-- Sets up mason-lspconfig to auto-install and auto-enable servers
-- Uses new vim.lsp.config API for any customizations
-- nvim-lspconfig provides server definitions (no require('lspconfig') needed)

return {
  {
    "mason-org/mason-lspconfig.nvim",
    dependencies = {
      { "mason-org/mason.nvim" },
      { "neovim/nvim-lspconfig" },
    },
    opts = {
      -- Auto-install these servers via Mason
      ensure_installed = {
        "lua_ls",
        "pyright",
        "bashls",
        "ts_ls",
        "jsonls",
        "yamlls",
        "dockerls",
        "marksman",
        "taplo",
      },
      -- mason-lspconfig v2 auto-enables all installed servers by default
      -- You can exclude servers here if you want manual control:
      -- automatic_enable = { exclude = { "ts_ls" } }
      automatic_enable = true,
    },
    config = function(_, opts)
      -- Must call setup with opts
      require("mason-lspconfig").setup(opts)

      -- ============================================================
      -- SERVER CUSTOMIZATIONS via new vim.lsp.config API
      -- Only add overrides here. Defaults come from nvim-lspconfig lsp/*.lua
      -- ============================================================

      -- lua_ls: tell it about Neovim's globals
      vim.lsp.config("lua_ls", {
        settings = {
          Lua = {
            runtime   = { version = "LuaJIT" },
            workspace = {
              checkThirdParty = false,
              library = vim.api.nvim_get_runtime_file("", true),
            },
            diagnostics = {
              globals = { "vim" },
            },
            telemetry = { enable = false },
          },
        },
      })

      -- pyright: basic settings
      vim.lsp.config("pyright", {
        settings = {
          python = {
            analysis = {
              autoSearchPaths      = true,
              useLibraryCodeForTypes = true,
              diagnosticMode       = "workspace",
            },
          },
        },
      })

      -- yamlls: enable schema store
      vim.lsp.config("yamlls", {
        settings = {
          yaml = {
            schemaStore = { enable = true },
            validate    = true,
          },
        },
      })

      -- ============================================================
      -- LSP KEYMAPS — set on LspAttach
      -- ============================================================
      vim.api.nvim_create_autocmd("LspAttach", {
        group = vim.api.nvim_create_augroup("LspKeymaps", { clear = true }),
        callback = function(event)
          local map = function(mode, lhs, rhs, desc)
            vim.keymap.set(mode, lhs, rhs, {
              buffer  = event.buf,
              silent  = true,
              desc    = desc,
            })
          end

          -- Navigation
          map("n", "gd",         vim.lsp.buf.definition,       "Go to definition")
          map("n", "gD",         vim.lsp.buf.declaration,      "Go to declaration")
          map("n", "gi",         vim.lsp.buf.implementation,   "Go to implementation")
          map("n", "gr",         vim.lsp.buf.references,       "References")
          map("n", "gt",         vim.lsp.buf.type_definition,  "Type definition")
          map("n", "K",          vim.lsp.buf.hover,            "Hover docs")
          map("n", "<C-k>",      vim.lsp.buf.signature_help,   "Signature help")

          -- Actions
          map("n",  "<leader>lr", vim.lsp.buf.rename,          "Rename")
          map("n",  "<leader>la", vim.lsp.buf.code_action,     "Code action")
          map("v",  "<leader>la", vim.lsp.buf.code_action,     "Code action")
          map("n",  "<leader>lf", function()
            require("conform").format({ async = true, lsp_fallback = true })
          end, "Format file")

          -- Diagnostics
          map("n", "<leader>ld", vim.diagnostic.open_float,    "Line diagnostics")
          map("n", "]d",         vim.diagnostic.goto_next,     "Next diagnostic")
          map("n", "[d",         vim.diagnostic.goto_prev,     "Prev diagnostic")
          map("n", "<leader>lq", vim.diagnostic.setloclist,    "Diagnostic list")
        end,
      })

      -- ============================================================
      -- DIAGNOSTIC APPEARANCE
      -- ============================================================
      vim.diagnostic.config({
        virtual_text = {
          spacing = 4,
          prefix  = "●",
        },
        signs            = true,
        underline        = true,
        update_in_insert = false,
        severity_sort    = true,
        float = {
          border = "rounded",
          source = true,
        },
      })
    end,
  },
}
