#!/bin/bash

# Quick setup script for AI Agent Platform on macOS/Linux

echo ""
echo "========================================"
echo "AI Agent Platform - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10+ first"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv || exit 1

echo "[2/4] Activating virtual environment..."
source venv/bin/activate || exit 1

echo "[3/4] Installing dependencies..."
pip install -r requirements.txt || exit 1

echo "[4/4] Initializing database..."
python init.py || exit 1

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. In terminal 1, run:"
echo "   source venv/bin/activate"
echo "   python backend/runtime.py"
echo ""
echo "2. In terminal 2, run:"
echo "   source venv/bin/activate"
echo "   streamlit run frontend/app.py"
echo ""
echo "3. Open http://localhost:8501 in your browser"
echo ""
