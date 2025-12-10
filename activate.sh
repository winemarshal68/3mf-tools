#!/bin/bash
# Quick activation script for 3MF tools environment

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate Python virtual environment
source "$TOOLS_DIR/venv/bin/activate"

# Add bin directory to PATH
export PATH="$TOOLS_DIR/bin:$PATH"

# Add lib3mf to library path
export DYLD_LIBRARY_PATH="$TOOLS_DIR/lib3mf/build:$DYLD_LIBRARY_PATH"

# Set environment variable for scripts to find tools
export TOOLS_3MF_DIR="$TOOLS_DIR"

echo "✓ 3MF Tools environment activated"
echo "  Python: $(which python)"
echo "  MeshFix: $(which meshfix)"
echo ""
echo "Available commands:"
echo "  meshfix <input.stl>         - Repair mesh"
echo "  python self_test.py         - Run tests"
echo "  python mcp_server/server.py - Start MCP server"
echo ""
echo "To deactivate: deactivate"
