"""
tools/internal/_telescope.py
Technology layer — Telescope search operations.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from mcp.mcp_client import send_command, eval_lua, grep_project


def find_files(query: str = "", path: str = None) -> list[str]:
    """
    Find files matching query. Uses fd via Telescope.
    Returns list of file paths from quickfix after search.
    path defaults to cwd.
    """
    cwd = path or ""
    cwd_arg = f", cwd = '{cwd}'" if cwd else ""
    send_command(f":lua require('telescope.builtin').find_files({{ search_file = '{query}'{cwd_arg} }})")
    return []  # Interactive — results appear in Telescope UI


def live_grep(pattern: str, path: str = None) -> list[dict]:
    """
    Grep across project using ripgrep via Telescope.
    Falls back to direct grep_project for programmatic use.
    """
    return grep_project(pattern, path)


def search_document_symbols(query: str = "") -> None:
    """Open Telescope LSP document symbols picker."""
    send_command(f":Telescope lsp_document_symbols")


def search_workspace_symbols(query: str = "") -> None:
    """Open Telescope LSP workspace symbols picker."""
    q = query.replace("'", "\\'")
    send_command(f":lua require('telescope.builtin').lsp_workspace_symbols({{ query = '{q}' }})")


def search_buffers() -> None:
    """Open Telescope buffer picker."""
    send_command(":Telescope buffers")


def search_quickfix() -> None:
    """Open Telescope quickfix picker."""
    send_command(":Telescope quickfix")


def grep_string_under_cursor() -> None:
    """Grep for word under cursor across project."""
    send_command(":Telescope grep_string")
