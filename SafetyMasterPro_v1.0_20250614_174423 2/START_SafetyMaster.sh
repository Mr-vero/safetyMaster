#!/bin/bash
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
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "✅ Python found!"
echo
echo "Installing dependencies (first time only)..."
pip3 install -r requirements.txt > /dev/null 2>&1

echo
echo "🚀 Starting SafetyMaster Pro..."
echo "🌐 Web interface will open at: http://localhost:8080"
echo "📹 Make sure your camera is connected"
echo
echo "Press Ctrl+C to stop the application"
echo

python3 web_interface.py
