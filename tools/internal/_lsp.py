"""
tools/internal/_lsp.py
Technology layer — LSP operations via Neovim.
Not imported by Nyx directly. Only imported by tools/ capability layer.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from mcp.mcp_client import send_command, eval_lua, get_status, NyxCommandError


def get_definition() -> dict:
    """Jump to definition of symbol under cursor. Returns new location."""
    before = get_status()
    send_command(":lua vim.lsp.buf.definition()")
    after = get_status()
    return {
        "file": after["file"],
        "line": after["cursor"]["line"],
        "col": after["cursor"]["col"],
        "jumped": after["file"] != before["file"] or after["cursor"] != before["cursor"],
    }


def get_references() -> list[dict]:
    """Get all references to symbol under cursor via LSP."""
    send_command(":lua vim.lsp.buf.references()")
    # References populate quickfix list
    result = eval_lua("vim.fn.getqflist()")
    refs = []
    if result:
        for item in result:
            refs.append({
                "file": item.get("filename", ""),
                "line": item.get("lnum", 0),
                "text": item.get("text", "").strip(),
            })
    return refs


def get_hover() -> str:
    """Get hover documentation for symbol under cursor."""
    send_command(":lua vim.lsp.buf.hover()")
    return "hover window opened in Neovim"


def get_diagnostics(file: str = None) -> list[dict]:
    """Get LSP diagnostics for current buffer or given file."""
    if file:
        send_command(f":e {file}")
    raw = eval_lua("""
        (function()
          local d = vim.diagnostic.get(0)
          local out = {}
          for _, item in ipairs(d) do
            table.insert(out, {
              line = item.lnum + 1,
              col  = item.col,
              severity = item.severity,
              message  = item.message,
              source   = item.source or "",
            })
          end
          return out
        end)()
    """)
    if not raw:
        return []
    severity_map = {1: "ERROR", 2: "WARN", 3: "INFO", 4: "HINT"}
    return [
        {
            "line": d["line"],
            "col": d["col"],
            "severity": severity_map.get(d["severity"], "?"),
            "message": d["message"],
            "source": d["source"],
        }
        for d in raw
    ]


def get_symbols(query: str = "") -> list[dict]:
    """Get document symbols for current buffer."""
    raw = eval_lua("""
        (function()
          local params = vim.lsp.util.make_position_params()
          local result = vim.lsp.buf_request_sync(0, 'textDocument/documentSymbol', params, 2000)
          if not result then return {} end
          local out = {}
          for _, res in pairs(result) do
            if res.result then
              for _, sym in ipairs(res.result) do
                table.insert(out, {
                  name  = sym.name,
                  kind  = sym.kind,
                  line  = sym.range and sym.range.start.line + 1 or 0,
                })
              end
            end
          end
          return out
        end)()
    """)
    if not raw:
        return []
    kind_map = {
        1:"File",2:"Module",3:"Namespace",4:"Package",5:"Class",
        6:"Method",7:"Property",8:"Field",9:"Constructor",10:"Enum",
        11:"Interface",12:"Function",13:"Variable",14:"Constant",
    }
    results = [
        {"name": s["name"], "kind": kind_map.get(s["kind"], "?"), "line": s["line"]}
        for s in raw
    ]
    if query:
        results = [s for s in results if query.lower() in s["name"].lower()]
    return results


def get_workspace_symbols(query: str) -> list[dict]:
    """Search workspace symbols via LSP."""
    raw = eval_lua(f"""
        (function()
          local params = {{query = {query!r}}}
          local result = vim.lsp.buf_request_sync(0, 'workspace/symbol', params, 3000)
          if not result then return {{}} end
          local out = {{}}
          for _, res in pairs(result) do
            if res.result then
              for _, sym in ipairs(res.result) do
                local loc = sym.location
                table.insert(out, {{
                  name = sym.name,
                  kind = sym.kind,
                  file = loc and loc.uri:gsub("file://", "") or "",
                  line = loc and loc.range.start.line + 1 or 0,
                }})
              end
            end
          end
          return out
        end)()
    """)
    return raw or []
