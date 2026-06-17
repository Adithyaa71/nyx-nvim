"""
tools/navigation.py — Capability layer.
All location/movement operations. Nyx imports from here.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mcp.mcp_client import send_command, get_status, read_buffer, NyxConnectionError
from tools.internal._lsp import get_definition, get_references


def goto_definition() -> dict:
    """
    Jump to definition of symbol under cursor.
    Returns {file, line, jumped}.
    """
    return get_definition()


def find_references() -> list[dict]:
    """
    Find all references to symbol under cursor.
    Returns [{file, line, text}].
    """
    return get_references()


def open_file(path: str) -> dict:
    """
    Open a file in Neovim. Returns status after opening.
    """
    send_command(f":e {path}")
    return get_status()


def goto_line(line: int, file: str = None) -> dict:
    """
    Jump to a specific line, optionally in a given file.
    """
    if file:
        send_command(f":e {file}")
    send_command(f":{line}")
    return get_status()


def get_current_location() -> dict:
    """
    Return current cursor location: file, line, col, function context.
    """
    from tools.internal._treesitter import get_current_function
    status = get_status()
    func = get_current_function()
    return {
        "file": status["file"],
        "line": status["cursor"]["line"],
        "col": status["cursor"]["col"],
        "filetype": status["filetype"],
        "current_function": func.get("text", "")[:80] if func else None,
    }


def list_open_files() -> list[dict]:
    """List all open buffers."""
    from mcp.mcp_client import get_buffers
    return get_buffers()


def split_open(path: str, vertical: bool = True) -> None:
    """Open file in a split."""
    cmd = "vsp" if vertical else "sp"
    send_command(f":{cmd} {path}")
