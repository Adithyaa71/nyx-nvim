"""
tools/analysis.py — Capability layer.
Code understanding operations. Nyx imports from here.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mcp.mcp_client import read_buffer, send_command, get_status
from tools.internal._lsp import get_symbols, get_diagnostics
from tools.internal._treesitter import get_all_functions, get_current_function, get_current_class


def get_file_symbols(file: str = None) -> list[dict]:
    """
    Get all symbols (functions, classes, vars) in a file via LSP.
    Falls back to treesitter if LSP unavailable.
    """
    if file:
        send_command(f":e {file}")
    syms = get_symbols()
    if syms:
        return syms
    # Treesitter fallback
    funcs = get_all_functions()
    return [{"name": f["name"], "kind": "Function", "line": f["start_line"]} for f in funcs]


def get_file_diagnostics(file: str = None) -> list[dict]:
    """Get all LSP diagnostics for a file."""
    return get_diagnostics(file)


def get_module_structure(file: str) -> dict:
    """
    Return high-level structure of a file:
    {language, line_count, functions, classes, imports, has_errors}
    """
    content = read_buffer(file)
    lines = content.splitlines()
    line_count = len(lines)

    # Detect language
    ext = os.path.splitext(file)[1].lstrip(".")
    lang_map = {
        "py":"python","lua":"lua","js":"javascript","ts":"typescript",
        "tsx":"tsx","sh":"bash","json":"json","yaml":"yaml","md":"markdown",
    }
    language = lang_map.get(ext, ext or "unknown")

    # Get functions and classes from treesitter
    send_command(f":e {file}")
    functions = get_all_functions()
    classes = []

    # Get LSP diagnostics
    diagnostics = get_diagnostics()
    has_errors = any(d["severity"] == "ERROR" for d in diagnostics)

    # Rough import detection
    imports = []
    for line in lines[:50]:
        stripped = line.strip()
        if stripped.startswith(("import ", "from ", "require(", "local ")):
            imports.append(stripped[:80])

    return {
        "file": file,
        "language": language,
        "line_count": line_count,
        "function_count": len(functions),
        "functions": [{"name": f["name"], "line": f["start_line"]} for f in functions],
        "imports": imports[:15],
        "has_errors": has_errors,
        "error_count": sum(1 for d in diagnostics if d["severity"] == "ERROR"),
        "diagnostics": diagnostics[:10],
    }


def get_current_context() -> dict:
    """
    Return what Nyx is currently looking at:
    file, cursor, current function, current class.
    """
    status = get_status()
    func = get_current_function()
    cls = get_current_class()
    return {
        "file": status["file"],
        "line": status["cursor"]["line"],
        "filetype": status["filetype"],
        "current_function": func,
        "current_class": cls,
    }


def summarize_diagnostics(file: str = None) -> dict:
    """Return diagnostic summary: error/warn/info counts + top messages."""
    diags = get_diagnostics(file)
    errors = [d for d in diags if d["severity"] == "ERROR"]
    warns  = [d for d in diags if d["severity"] == "WARN"]
    return {
        "error_count": len(errors),
        "warn_count": len(warns),
        "top_errors": errors[:5],
        "top_warnings": warns[:5],
    }
