#!/bin/bash
# Returns the active Neovim socket path
# Usage: ./get_nvim_socket.sh
# Used by mcp_client.py to find the running Neovim instance

SOCKET=$(ls /tmp/nvim-*.sock 2>/dev/null | head -1)

if [ -z "$SOCKET" ]; then
  echo "ERROR: No Neovim socket found. Start nvim first." >&2
  exit 1
fi

echo "$SOCKET"
