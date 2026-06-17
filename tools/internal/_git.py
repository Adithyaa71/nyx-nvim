"""
tools/internal/_git.py
Technology layer — Git operations via gitsigns + shell.
"""

import sys, os, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from mcp.mcp_client import send_command, eval_lua, get_status


def _run_git(args: list[str], cwd: str = None) -> str:
    """Run a git command in the project root. Returns stdout."""
    if not cwd:
        status = get_status()
        cwd = status["cwd"]
    result = subprocess.run(
        ["git"] + args,
        capture_output=True, text=True, cwd=cwd
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def get_status_git() -> str:
    """Return git status output."""
    return _run_git(["status", "--short"])


def get_log(n: int = 10) -> list[dict]:
    """Return last n commits as list of {hash, author, date, message}."""
    raw = _run_git(["log", f"-{n}", "--pretty=format:%H|%an|%ad|%s", "--date=short"])
    commits = []
    for line in raw.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash": parts[0][:8],
                "author": parts[1],
                "date": parts[2],
                "message": parts[3],
            })
    return commits


def get_diff(file: str = None) -> str:
    """Return git diff for file or entire working tree."""
    if file:
        return _run_git(["diff", file])
    return _run_git(["diff"])


def get_blame_line(file: str, line: int) -> dict:
    """Get git blame for a specific line."""
    raw = _run_git(["blame", "-L", f"{line},{line}", "--porcelain", file])
    result = {"hash": "", "author": "", "date": "", "summary": ""}
    for l in raw.splitlines():
        if l.startswith("author "):
            result["author"] = l[7:]
        elif l.startswith("author-time "):
            from datetime import datetime
            result["date"] = datetime.fromtimestamp(int(l[12:])).strftime("%Y-%m-%d")
        elif l.startswith("summary "):
            result["summary"] = l[8:]
        elif len(l) == 40 and l.isalnum():
            result["hash"] = l[:8]
    return result


def stage_file(file: str) -> None:
    """Stage a file for commit."""
    _run_git(["add", file])


def commit(message: str) -> str:
    """Create a commit with given message. Returns commit hash."""
    _run_git(["commit", "-m", message])
    return _run_git(["rev-parse", "--short", "HEAD"])


def get_branches() -> list[str]:
    """List all branches."""
    raw = _run_git(["branch", "-a"])
    return [b.strip().lstrip("* ") for b in raw.splitlines() if b.strip()]


def get_current_branch() -> str:
    """Return current branch name."""
    return _run_git(["rev-parse", "--abbrev-ref", "HEAD"])


def show_hunk_preview() -> None:
    """Preview current hunk via gitsigns in Neovim."""
    send_command(":lua require('gitsigns').preview_hunk()")


def stage_hunk() -> None:
    """Stage hunk at cursor via gitsigns."""
    send_command(":lua require('gitsigns').stage_hunk()")
