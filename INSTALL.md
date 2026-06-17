# 🛠️ Nyx-Nvim Installation Guide

## 📋 Prerequisites

Before installing Nyx-Nvim, ensure you have the following:

### System Requirements
- **Neovim 0.9+** (recommended: latest stable)
- **Python 3.11+** (for MCP tools)
- **Node.js 18+** (for MCP server)
- **Git 2.0+**
- **Linux/macOS/Windows** (with WSL support for Windows)

### Required Tools
```bash
# Install Neovim (Ubuntu/Debian)
sudo apt install neovim

# Install Python dependencies
sudo apt install python3 python3-pip python3-venv

# Install Node.js (if not installed)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Git
sudo apt install git
```

## 📦 Repository Setup

### 1. Clone the Repository
```bash
# Clone the Nyx-Nvim repository
git clone https://github.com/Adithyaa71/nyx-nvim.git
cd nyx-nvim
```

### 2. Virtual Environment Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install Python dependencies
pip install -r requirements.txt
```

## 🧩 MCP Integration Setup

### 1. Install MCP Neovim Server
```bash
# Install globally via npm
npm install -g mcp-neovim-server

# Verify installation
mcp-neovim-server --version
```

### 2. Configure MCP
```bash
# Create MCP configuration directory
mkdir -p ~/.config/mcp

# Copy default configuration
cp mcp/mcp-config.json ~/.config/mcp/config.json
```

## 🚀 Neovim Setup

### 1. Install Neovim Configuration
```bash
# Create symbolic links for Neovim config
mkdir -p ~/.config/nvim
ln -sf $(pwd)/nvim/init.lua ~/.config/nvim/init.lua

# For full plugin configuration
ln -sf $(pwd)/nvim/lua/ ~/.config/nvim/lua
```

### 2. Install Plugins
```bash
# Using lazy.nvim (recommended)
nvim +LazySync +qall
```

## 🧪 Testing Installation

### 1. Verify MCP Connection
```bash
# Test MCP server
mcp-neovim-server --version

# Test Neovim
nvim --version
```

### 2. Run Basic Tests
```bash
# Test MCP tools
python -m mcp.test

# Verify Neovim configuration
nvim -c "MCPStatus" -c "q"
```

## 📁 Directory Structure Explanation

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
├── INSTALL.md         # This file
└── README.md          # Project overview
```

## 🔧 Troubleshooting

### Common Issues

1. **MCP Connection Problems**:
   ```bash
   # Test SSH connection
   ssh -T git@github.com
   
   # Restart MCP server
   mcp-neovim-server restart
   ```

2. **Python Dependencies Issues**:
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Plugin Installation Issues**:
   ```bash
   # Clean plugin cache
   rm -rf ~/.cache/nvim/plugin
   nvim +LazySync +qall
   ```

### Debugging Commands

```bash
# Check installed packages
pip list

# Print Python version
python3 --version

# Verify Neovim
nvim --version
```

## 📚 Required Dependencies

### Python Packages:
```txt
requests>=2.28.0
pyyaml>=6.0
openai>=0.27.0
jinja2>=3.1.0
neovim>=0.3.1
```

### Node.js Packages:
```json
{
  "dependencies": {
    "mcp-neovim-server": "^1.0.0"
  }
}
```

## 🔒 Security Best Practices

1. **Keep Secrets Secure**: Never commit tokens or credentials to repository
2. **Use Virtual Environments**: Always isolate project dependencies
3. **Update Regularly**: Keep dependencies and system software up to date
4. **Network Security**: Protect server communications with SSL/TLS when needed

## 📝 Support and Resources

- **Documentation**: Read the `nvim/` directory for configuration guides
- **GitHub Issues**: Report bugs at https://github.com/Adithyaa71/nyx-nvim/issues
- **Neovim Community**: Join Neovim user communities
- **Version Control**: Use Git for all changes and backups

---
*Installation complete. Nyx-Nvim is ready for AI-assisted development!*