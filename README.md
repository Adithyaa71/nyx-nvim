# Nyx-Nvim

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Neovim](https://img.shields.io/badge/Neovim-0.9%2B-green.svg)](https://neovim.io/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://www.python.org/)

> *"Ship it. Don't overthink — write code, test it, iterate."*  
> — The Nyx-Agent Philosophy (for Neovim)

## 🚀 Overview

**Nyx-Nvim** is a comprehensive Neovim configuration and MCP (Model Context Protocol) abstraction layer designed to create a powerful AI-assisted development environment. This repository contains the complete implementation for a production-ready Neovim setup with full MCP integration.

## 🏗️ Architecture

```
    ┌─────────────────────────────────────────────────────────────────────┐
    │                        Model Context Protocol (MCP)                 │
    └─────────────┬───────────────────────────────────────────────────────┘
                  │
    ┌─────────────▼─────────────┐          ┌──────────────────────────┐
    │    Nyx-Nvim Configuration   │◄─────────┤     AI Coding Agent      │
    │        (Neovim)             │          │   (MCP Client)           │
    └─────────┬───▲─────────────┘          └──────────────┬───────────┘
              │   │                              │
    ┌─────────▼───▼─────────────┐  ┌─────────────▼───────────────┐
    │   Neovim + Plugins        │  │  LLM Backends & Models      │
    │  (MCP Server + Tools)     │  │  (Qwen, LLaMA, Claude, etc.)│
    └─────────────┬─────────────┘  └─────────────────────────────┘
                  │
    ┌─────────────▼─────────────┐
    │     MCP Tools Layer         │
    │  (Python for Neovim)       │
    └─────────────────────────────┘
 ```

## 🌟 Features

- **Full MCP Integration**: Native Model Context Protocol implementation for AI-powered development
- **Modern Neovim Setup**: Professional configuration with productivity-enhancing plugins
- **MCP Abstraction Layer**: Python tools for seamless Neovim-AI communication
- **Code Analysis Tools**: Advanced refactoring, search, and analysis capabilities
- **Git Integration**: Seamless repository management within Neovim
- **Language Server Protocol**: Full LSP support for multiple languages 

## 📦 Prerequisites

- **Neovim 0.9+** (latest stable recommended)
- **Python 3.11+** (for MCP tools)
- **Node.js 18+** (MCP server)
- **Git 2.0+**

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Adithyaa71/nyx-nvim.git
   cd nyx-nvim
   ```

2. **Setup Neovim**:
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Node.js packages for MCP
   npm install -g mcp-neovim-server
   ```

3. **Install Neovim plugins**:
   ```bash
   # Using lazy.nvim (recommended)
   nvim +LazySync +qall
   ```

## 🚀 Quick Start

1. **Launch Neovim**:
   ```bash
   nvim
   ```

2. **Verify MCP Integration**:
   ```vim
   :MCPStatus
   ```

3. **Start AI Coding Session**:
   ```vim
   :NyxStart
   ```

## 📁 Directory Structure

```
nyx-nvim/
├── nvim/              # Neovim configuration
│   ├── init.lua       # Main configuration
│   └── lua/           # Lua modules
│       ├── core/      # Core configuration
│       ├── plugins/   # Plugin definitions
│       └── util/      # Utility modules  
├── mcp/               # MCP protocol implementation
│   ├── mcp_client.py   # Client for AI agent communication  
│   └── get_nvim_socket.sh # Socket connection helper
├── tools/             # Utility tools for development
│   ├── analysis.py     # Code analysis tools
│   ├── refactor.py     # Refactoring tools  
│   ├── search.py       # Code search tools
│   └── internal/       # Internal tools
│       ├── _lsp.py     # LSP integration
│       ├── _treesitter.py # Tree-sitter integration
│       ├── _git.py     # Git tools
│       └── _telescope.py # Telescope search
├── skills/            # Agent skills
│   └── summarize_file.py # File analysis skill
├── README.md          # This file
├── INSTALL.md         # Installation guide
└── .gitignore         # Git ignore rules
```

## 🔧 Configuration

Nyx-Nvim uses a modular configuration approach:

1. **Main Configuration**: `nvim/init.lua`
2. **Plugin Settings**: `nvim/lua/plugins/`
3. **Core Settings**: `nvim/lua/core/` 
4. **Utility Modules**: `nvim/lua/util/`

## 📚 Documentation

- **INSTALL.md** - Complete installation guide
- **nvim/lua/README.md** - Neovim configuration documentation

## 🤝 Contributing

1. Fork it
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 📬 Contact

Questions or issues? Open a [GitHub issue](https://github.com/Adithyaa71/nyx-nvim/issues) or reach out via [GitHub](https://github.com/Adithyaa71).

---

*Powered by AI-enabled development tools*
