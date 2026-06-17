"""
tools/internal/_treesitter.py
Technology layer — Treesitter operations via Neovim.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from mcp.mcp_client import eval_lua, send_command, get_status


def get_node_at_cursor() -> dict:
    """Get the treesitter node type at current cursor position."""
    raw = eval_lua("""
        (function()
          local node = vim.treesitter.get_node()
          if not node then return {type="none", text=""} end
          return {
            type   = node:type(),
            text   = vim.treesitter.get_node_text(node, 0) or "",
            start  = {node:start()},
            finish = {node:end_()},
          }
        end)()
    """)
    return raw or {"type": "none", "text": ""}


def get_current_function() -> dict:
    """
    Get the function containing the cursor.
    Uses treesitter textobject @function.outer.
    Returns {name, start_line, end_line, text}.
    """
    raw = eval_lua("""
        (function()
          local ts_utils = require("nvim-treesitter.ts_utils")
          local node = ts_utils.get_node_at_cursor()
          while node do
            local t = node:type()
            if t == "function_definition" or t == "function_declaration"
              or t == "method_definition" or t == "arrow_function" then
              local sl, _, el, _ = node:range()
              local lines = vim.api.nvim_buf_get_lines(0, sl, el+1, false)
              return {
                start_line = sl + 1,
                end_line   = el + 1,
                text       = table.concat(lines, "\\n"),
              }
            end
            node = node:parent()
          end
          return nil
        end)()
    """)
    return raw or {}


def get_current_class() -> dict:
    """Get the class containing the cursor."""
    raw = eval_lua("""
        (function()
          local ts_utils = require("nvim-treesitter.ts_utils")
          local node = ts_utils.get_node_at_cursor()
          while node do
            local t = node:type()
            if t == "class_definition" or t == "class_declaration" then
              local sl, _, el, _ = node:range()
              local lines = vim.api.nvim_buf_get_lines(0, sl, el+1, false)
              return {
                start_line = sl + 1,
                end_line   = el + 1,
                text       = table.concat(lines, "\\n"),
              }
            end
            node = node:parent()
          end
          return nil
        end)()
    """)
    return raw or {}


def get_all_functions(file: str = None) -> list[dict]:
    """
    List all functions in current buffer or given file.
    Returns [{name, start_line, end_line}]
    """
    if file:
        send_command(f":e {file}")
    raw = eval_lua("""
        (function()
          local parser = vim.treesitter.get_parser(0)
          if not parser then return {} end
          local tree = parser:parse()[1]
          local root  = tree:root()
          local out   = {}
          local function walk(node)
            local t = node:type()
            if t == "function_definition" or t == "function_declaration"
              or t == "method_definition" then
              local sl, _, el, _ = node:range()
              -- try to get name
              local name_node = node:field("name")[1]
              local name = name_node and vim.treesitter.get_node_text(name_node, 0) or "?"
              table.insert(out, {name=name, start_line=sl+1, end_line=el+1})
            end
            for child in node:iter_children() do
              walk(child)
            end
          end
          walk(root)
          return out
        end)()
    """)
    return raw or []
