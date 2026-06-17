# TOOLS.md — Nyx's Tool Reference

## Available Tools

As an OpenClaw agent, you have direct access to these built-in tools:

### File Operations
- **read** — Read files (text + images)
- **write** — Write/overwrite files (creates parent dirs)
- **edit** — Targeted text replacement in files
- **apply_patch** — Apply multi-file diffs

### Shell
- **exec** — Run shell commands (bash, background processes, PTY for interactive CLIs)
- **process** — Manage running exec sessions (list, poll, log, write, kill)

### Web / Research
- **web_search** — Search web (configurable provider, country, recency)
- **web_fetch** — Extract readable content from URLs
- **tavily_search** — Deep web search via Tavily
- **tavily_extract** — Extract content from specific URLs

### Browser
- **browser** — Control web browser (status, open, navigate, snapshot, screenshot, act)
- Uses Playwright under the hood

### Vault (zk)
- Use `exec` with `zk` CLI commands:
  - `zk list --match "keyword"` — full text search
  - `zk list --tag "tag"` — by tag
  - `zk list --link-to "path"` — backlinks
  - `zk list --linked-by "path"` — forward links
  - `zk index` — refresh graph

### Agent Management
- **sessions_spawn** — Launch sub-agents for isolated work
- **sessions_send** — Send messages to other agents/sessions
- **sessions_history** — Check conversation history
- **message** — Send messages, reactions, polls across channels

### System
- **gateway** — Config read/write, restart gateway
- **cron** — Schedule reminders and recurring tasks
- **canvas** — Present HTML content on connected devices

## Nyx MCP Tool Layer

Neovim-integrated code tooling layer. Only `mcp/mcp_client.py` calls Neovim directly — all other layers import from it.

### Files

| Layer | Path | Purpose |
|-------|------|---------|
| **Core MCP** | `mcp/mcp_client.py` | pynvim connection, buffer read/write, command exec, Lua eval |
| **Socket** | `mcp/get_nvim_socket.sh` | Auto-discovers Neovim socket (`/tmp/nvim-*.sock`) |
| **Navigation** | `tools/navigation.py` | open file, goto line, definition, references, splits |
| **Analysis** | `tools/analysis.py` | symbols, diagnostics, module structure, context |
| **Search** | `tools/search.py` | project grep, file find, workspace symbols, TODOs |
| **Refactor** | `tools/refactor.py` | safe edit, replace, format, rename, code actions |
| **_lsp** | `tools/internal/_lsp.py` | LSP: definitions, references, hover, diagnostics, symbols |
| **_treesitter** | `tools/internal/_treesitter.py` | Treesitter: node, function/class context, all functions |
| **_git** | `tools/internal/_git.py` | Git: status, log, diff, blame, stage, commit |
| **_telescope** | `tools/internal/_telescope.py` | Telescope: file picker, live grep, symbol search |
| **Skill: summarize** | `skills/summarize_file.py` | Full file summary (structure + diags + git + health) |

### Requirements
- Neovim must be running (auto-configures socket in `options.lua`)
- `npm install -g mcp-neovim-server` (v0.5.5 installed)
- `pynvim` Python package (`pip install pynvim`)

### Usage Pattern
```python
import sys
sys.path.insert(0, '/mnt/Obsidian/zk/Nyx/agent')

from tools.navigation import open_file, get_current_location
open_file('target.py')
loc = get_current_location()  # {file, line, col, function_context}

from tools.analysis import get_file_symbols, summarize_diagnostics
syms = get_file_symbols()       # LSP symbols
health = summarize_diagnostics()  # error/warn count

from tools.search import search_project
results = search_project('def handle')

from tools.refactor import safe_edit
safe_edit('file.py', 10, 15, '# new content')
```

## Skills (Procedures)

Skills in `skills/` provide step-by-step workflows. When you need to:
- **Code / build** → Check `skills/coding-agent/SKILL.md` for delegate-to-worker patterns
- **File summarization** → `skills/summarize_file.py`
- **Research / prototype** → `skills/spike/SKILL.md`
- **Debug Python** → `skills/python-debugpy/SKILL.md`
- **Debug Node.js** → `skills/node-inspect-debugger/SKILL.md`

## Platform Formatting

- **Discord/WhatsApp:** No markdown tables — use bullet lists
- **Discord:** Wrap multiple links in `<>` to suppress embeds
- **WhatsApp:** No headers — use **bold** or CAPS for emphasis
