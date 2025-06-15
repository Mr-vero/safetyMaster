#!/bin/bash
# SafetyMaster Pro - Mac Startup Script
# This file can be double-clicked on Mac to start the application

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

clear
echo
echo "  ███████╗ █████╗ ███████╗███████╗████████╗██╗   ██╗"
echo "  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝╚██╗ ██╔╝"
echo "  ███████╗███████║█████╗  █████╗     ██║    ╚████╔╝ "
echo "  ╚════██║██╔══██║██╔══╝  ██╔══╝     ██║     ╚██╔╝  "
echo "  ███████║██║  ██║██║     ███████╗   ██║      ██║   "
echo "  ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝   ╚═╝      ╚═╝   "
echo
echo "                    MASTER PRO v1.0"
echo "           Real-time AI Safety Equipment Detection"
echo "                        for Mac"
echo

echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo
    echo "📥 Please install Python 3.8+ from:"
    echo "   https://www.python.org/downloads/macos/"
    echo
    echo "Or install using Homebrew:"
    echo "   brew install python3"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found!"

echo
echo "📦 Installing dependencies (this may take a moment on first run)..."
python3 -m pip install --user -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "💡 Try running: python3 -m pip install --upgrade pip"
    read -p "Press Enter to exit..."
    exit 1
fi

echo
echo "🚀 Starting SafetyMaster Pro..."
echo "🌐 Web interface will open at: http://localhost:8080"
echo "📹 Make sure your camera is connected and permissions are granted"
echo
echo "💡 To stop the application, press Ctrl+C in this window"
echo "🔄 To restart, just double-click this file again"
echo

# Try to open the web browser automatically
sleep 3 && open http://localhost:8080 &

# Start the application
python3 web_interface.py

echo
echo "👋 SafetyMaster Pro has stopped"
read -p "Press Enter to close this window..." 