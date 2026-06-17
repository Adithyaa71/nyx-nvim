"""
mcp_client.py — Thin wrapper over mcp-neovim-server primitives.
Only file that calls MCP directly. All other layers import from here.

Usage:
  python3 mcp_client.py test   → verify connection
"""

import subprocess
import sys
import os
import json
import logging
from datetime import datetime
from typing import Any

# ── Logging ──────────────────────────────────────────────────────────────────
LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "mcp.log")
LOG_PATH = os.path.abspath(LOG_PATH)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [MCP] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
    ],
)
log = logging.getLogger("mcp_client")


# ── Errors ────────────────────────────────────────────────────────────────────
class NyxConnectionError(Exception):
    pass

class NyxCommandError(Exception):
    pass


# ── Socket Discovery ──────────────────────────────────────────────────────────
def get_socket() -> str:
    """Return active Neovim socket path."""
    # Env var takes priority
    env_path = os.environ.get("NVIM_SOCKET_PATH")
    if env_path and os.path.exists(env_path):
        return env_path

    # Auto-detect
    script = os.path.join(os.path.dirname(__file__), "get_nvim_socket.sh")
    result = subprocess.run([script], capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        raise NyxConnectionError(
            "No Neovim socket found. Start nvim first.\n"
            "Hint: nvim is auto-configured to create a socket on startup."
        )
    return result.stdout.strip()


# ── Core: pynvim connection ───────────────────────────────────────────────────
def _get_nvim():
    """Return a connected pynvim instance."""
    try:
        import pynvim
    except ImportError:
        raise NyxConnectionError(
            "pynvim not installed. Run: pip install pynvim --break-system-packages"
        )
    socket = get_socket()
    try:
        nvim = pynvim.attach("socket", path=socket)
        return nvim
    except Exception as e:
        raise NyxConnectionError(f"Cannot connect to Neovim at {socket}: {e}")


# ── Primitives ────────────────────────────────────────────────────────────────
def read_buffer(path: str = None) -> str:
    """
    Read buffer contents.
    If path given, opens the file first. Returns full text as string.
    """
    log.info(f"read_buffer path={path}")
    nvim = _get_nvim()
    if path:
        nvim.command(f"e {path}")
    lines = nvim.current.buffer[:]
    return "\n".join(lines)


def send_command(cmd: str) -> str:
    """
    Send a vim ex command. Returns command output if any.
    Examples:
      send_command(":w")
      send_command(":lua vim.lsp.buf.definition()")
      send_command(":Telescope find_files")
    """
    log.info(f"send_command cmd={cmd!r}")
    nvim = _get_nvim()
    # Strip leading colon if present
    cmd = cmd.lstrip(":")
    try:
        result = nvim.command_output(cmd)
        return result or ""
    except Exception as e:
        raise NyxCommandError(f"Command failed: {cmd!r} → {e}")


def get_status() -> dict:
    """
    Return current editor state:
    file, cursor, mode, cwd, modified, lsp_clients
    """
    log.info("get_status")
    nvim = _get_nvim()
    buf = nvim.current.buffer
    win = nvim.current.window
    row, col = win.cursor
    return {
        "file": buf.name,
        "cursor": {"line": row, "col": col},
        "mode": nvim.api.get_mode()["mode"],
        "cwd": nvim.funcs.getcwd(),
        "modified": buf.options["modified"],
        "filetype": buf.options["filetype"],
        "line_count": len(buf),
    }


def edit_buffer(start_line: int, end_line: int, new_lines: list[str], path: str = None) -> None:
    """
    Replace lines [start_line, end_line] (1-indexed, inclusive) with new_lines.
    Always read_buffer first to know exact line numbers.
    """
    log.info(f"edit_buffer lines={start_line}-{end_line} path={path}")
    nvim = _get_nvim()
    if path:
        nvim.command(f"e {path}")
    buf = nvim.current.buffer
    # Convert to 0-indexed for nvim API
    buf[start_line - 1 : end_line] = new_lines
    nvim.command("w")


def grep_project(pattern: str, path: str = None) -> list[dict]:
    """
    Project-wide grep. Returns list of {file, line, text} dicts.
    Uses ripgrep via vim :grep if available.
    """
    log.info(f"grep_project pattern={pattern!r} path={path}")
    nvim = _get_nvim()
    search_path = path or nvim.funcs.getcwd()
    try:
        nvim.command(f"silent! grep! {pattern!r} {search_path}")
        qf = nvim.funcs.getqflist()
        results = []
        for item in qf:
            results.append({
                "file": nvim.funcs.bufname(item["bufnr"]),
                "line": item["lnum"],
                "text": item["text"].strip(),
            })
        return results
    except Exception as e:
        raise NyxCommandError(f"grep failed: {e}")


def search_replace(pattern: str, replacement: str, flags: str = "g") -> int:
    """
    Regex search and replace in current buffer.
    Returns count of replacements made.
    """
    log.info(f"search_replace pattern={pattern!r} replacement={replacement!r}")
    nvim = _get_nvim()
    cmd = f"%s/{pattern}/{replacement}/{flags}e"
    nvim.command(cmd)
    count = int(nvim.funcs.eval("v:count1"))
    nvim.command("w")
    return count


def get_buffers() -> list[dict]:
    """List all open buffers with metadata."""
    log.info("get_buffers")
    nvim = _get_nvim()
    bufs = []
    for buf in nvim.buffers:
        if buf.valid and buf.name:
            bufs.append({
                "id": buf.number,
                "name": buf.name,
                "modified": buf.options["modified"],
                "filetype": buf.options.get("filetype", ""),
            })
    return bufs


def eval_lua(expr: str) -> Any:
    """
    Evaluate a Lua expression in Neovim and return the result.
    Example: eval_lua("vim.lsp.get_clients()")
    """
    log.info(f"eval_lua expr={expr!r}")
    nvim = _get_nvim()
    return nvim.exec_lua(expr)


# ── CLI test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        try:
            socket = get_socket()
            status = get_status()
            print(f"connected to Neovim at {socket}")
            print(f"  file    : {status['file'] or '(no file)'}")
            print(f"  mode    : {status['mode']}")
            print(f"  cwd     : {status['cwd']}")
        except NyxConnectionError as e:
            print(f"FAIL: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python3 mcp_client.py test")
