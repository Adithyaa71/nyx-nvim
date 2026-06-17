"""
tools/search.py — Capability layer.
All search operations. Nyx imports from here.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mcp.mcp_client import grep_project, send_command, read_buffer
from tools.internal._lsp import get_references, get_workspace_symbols
from tools.internal._telescope import live_grep, find_files


def search_project(pattern: str, path: str = None) -> list[dict]:
    """
    Search for pattern across entire project.
    Returns [{file, line, text}].
    """
    return grep_project(pattern, path)


def find_files_by_name(query: str, path: str = None) -> list[str]:
    """
    Find files by name pattern using fd.
    Returns list of matching paths.
    """
    import subprocess
    from mcp.mcp_client import get_status
    cwd = path or get_status()["cwd"]
    result = subprocess.run(
        ["fd", "--type", "f", query, cwd],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # fallback to find
        result = subprocess.run(
            ["find", cwd, "-name", f"*{query}*", "-type", "f"],
            capture_output=True, text=True
        )
    return [p.strip() for p in result.stdout.splitlines() if p.strip()]


def find_symbol_in_workspace(query: str) -> list[dict]:
    """
    Find symbol across entire workspace via LSP.
    Returns [{name, kind, file, line}].
    """
    return get_workspace_symbols(query)


def find_references_to(symbol: str = None) -> list[dict]:
    """
    Find all references to symbol under cursor (or navigate to symbol first).
    Returns [{file, line, text}].
    """
    if symbol:
        # Try to navigate to symbol first via workspace symbol search
        syms = get_workspace_symbols(symbol)
        if syms:
            from mcp.mcp_client import send_command
            first = syms[0]
            send_command(f":e {first['file']}")
            send_command(f":{first['line']}")
    return get_references()


def search_in_file(pattern: str, file: str = None) -> list[dict]:
    """
    Search pattern within a single file.
    Returns [{line_number, text}].
    """
    content = read_buffer(file)
    results = []
    for i, line in enumerate(content.splitlines(), 1):
        if pattern.lower() in line.lower():
            results.append({"line": i, "text": line.strip()})
    return results


def find_todos(path: str = None) -> list[dict]:
    """Find all TODO/FIXME/HACK/NOTE comments in project."""
    results = []
    for marker in ["TODO", "FIXME", "HACK", "NOTE", "XXX"]:
        found = grep_project(marker, path)
        for f in found:
            f["marker"] = marker
            results.append(f)
    return results
