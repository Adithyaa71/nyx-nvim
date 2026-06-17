"""
skills/summarize_file.py — First Nyx skill.
Produces a structured summary of any code file.
Combines: analysis.get_module_structure + diagnostics + git blame header.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.analysis import get_module_structure, summarize_diagnostics
from tools.internal._git import get_blame_line, get_current_branch


def summarize_file(file: str) -> dict:
    """
    Summarize a file completely.

    Returns:
    {
      file, language, line_count,
      function_count, functions: [{name, line}],
      imports: [str],
      diagnostics: {error_count, warn_count, top_errors},
      git: {branch, last_commit_author, last_commit_date, last_commit_message},
      health: "clean" | "has_warnings" | "has_errors"
    }
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"File not found: {file}")

    # Core structure
    structure = get_module_structure(file)

    # Diagnostics summary
    diag_summary = summarize_diagnostics(file)

    # Git info (best effort)
    git_info = {}
    try:
        branch = get_current_branch()
        blame = get_blame_line(file, 1)
        git_info = {
            "branch": branch,
            "last_commit_author": blame.get("author", ""),
            "last_commit_date": blame.get("date", ""),
            "last_commit_summary": blame.get("summary", ""),
        }
    except Exception:
        git_info = {"branch": "unknown", "note": "git info unavailable"}

    # Health status
    if diag_summary["error_count"] > 0:
        health = "has_errors"
    elif diag_summary["warn_count"] > 0:
        health = "has_warnings"
    else:
        health = "clean"

    return {
        "file": file,
        "language": structure["language"],
        "line_count": structure["line_count"],
        "function_count": structure["function_count"],
        "functions": structure["functions"],
        "imports": structure["imports"],
        "diagnostics": diag_summary,
        "git": git_info,
        "health": health,
    }


def summarize_file_text(file: str) -> str:
    """Human-readable version of summarize_file for Discord output."""
    s = summarize_file(file)
    lines = [
        f"**{os.path.basename(file)}** — {s['language']} | {s['line_count']} lines | {s['health']}",
        f"Functions ({s['function_count']}): {', '.join(f['name'] for f in s['functions'][:8])}",
    ]
    if s["imports"]:
        lines.append(f"Imports: {', '.join(s['imports'][:5])}...")
    d = s["diagnostics"]
    if d["error_count"] or d["warn_count"]:
        lines.append(f"Diagnostics: {d['error_count']} errors, {d['warn_count']} warnings")
    g = s["git"]
    if g.get("branch") and g["branch"] != "unknown":
        lines.append(f"Git: {g['branch']} | {g.get('last_commit_author','')} | {g.get('last_commit_summary','')}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 summarize_file.py <path>")
        sys.exit(1)
    import json
    result = summarize_file(sys.argv[1])
    print(json.dumps(result, indent=2))
