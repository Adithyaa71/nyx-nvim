"""
tools/refactor.py — Capability layer.
All code modification operations. Nyx imports from here.
RULE: Always read before edit. Always verify after edit.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mcp.mcp_client import (
    read_buffer, edit_buffer, send_command,
    search_replace, get_status, NyxCommandError
)


def safe_edit(file: str, start_line: int, end_line: int, new_content: str) -> dict:
    """
    Safe edit pattern: read → validate lines → edit → save → verify.
    new_content is a string (may contain newlines).
    Returns {success, lines_changed, file}.
    """
    # Read current state
    original = read_buffer(file)
    orig_lines = original.splitlines()
    total = len(orig_lines)

    if start_line < 1 or end_line > total:
        raise NyxCommandError(
            f"Line range {start_line}-{end_line} out of bounds (file has {total} lines)"
        )

    new_lines = new_content.splitlines()
    edit_buffer(start_line, end_line, new_lines, file)

    # Verify file saved
    status = get_status()
    return {
        "success": not status["modified"],
        "lines_changed": len(new_lines) - (end_line - start_line + 1),
        "file": file,
    }


def replace_in_file(pattern: str, replacement: str, file: str = None) -> int:
    """
    Regex replace across entire buffer. Returns count of replacements.
    """
    if file:
        send_command(f":e {file}")
    return search_replace(pattern, replacement)


def format_file(file: str = None) -> dict:
    """
    Format current or given file via conform.nvim.
    """
    if file:
        send_command(f":e {file}")
    send_command(":lua require('conform').format({ async = false, lsp_fallback = true })")
    send_command(":w")
    return {"formatted": True, "file": file or get_status()["file"]}


def rename_symbol() -> None:
    """
    Rename symbol under cursor via LSP. Opens rename prompt in Neovim.
    """
    send_command(":lua vim.lsp.buf.rename()")


def apply_code_action() -> None:
    """
    Open LSP code actions menu for symbol/diagnostic under cursor.
    """
    send_command(":lua vim.lsp.buf.code_action()")


def insert_lines_after(line: int, new_content: str, file: str = None) -> dict:
    """
    Insert new_content after given line number.
    """
    if file:
        send_command(f":e {file}")
    current = read_buffer()
    lines = current.splitlines()
    new_lines = new_content.splitlines()
    # Insert after line (0-indexed: line)
    updated = lines[:line] + new_lines + lines[line:]
    edit_buffer(1, len(lines), updated)
    return {"inserted_at": line + 1, "lines_added": len(new_lines)}


def delete_lines(start_line: int, end_line: int, file: str = None) -> dict:
    """Delete lines from start_line to end_line inclusive."""
    if file:
        send_command(f":e {file}")
    edit_buffer(start_line, end_line, [])
    return {"deleted_lines": end_line - start_line + 1}
