#!/bin/bash
# Simple launcher for the 3MF Tools visual app

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "3MF Tools Visual App"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: ./install.sh"
    exit 1
fi

# Activate venv
echo "Activating environment..."
source venv/bin/activate

# Check if Gradio is installed
if ! python -c "import gradio" 2>/dev/null; then
    echo "Installing Gradio..."
    pip install gradio --quiet
fi

# Check port
PORT=7860
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port $PORT is already in use"
    echo "Trying alternative port 7861..."
    PORT=7861
fi

echo ""
echo "Starting app on http://127.0.0.1:$PORT"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

# Launch app with proper port
python -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')

# Import the app
exec(open('app.py').read())
" --server-port $PORT

echo ""
echo "App stopped."
