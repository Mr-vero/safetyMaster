#!/bin/bash

echo "🔒 Starting Safety Monitor Application..."
echo "============================================"

# Check if virtual environment exists
if [ ! -d "safety_monitor_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source safety_monitor_env/bin/activate

# Check if required packages are installed
echo "🔍 Checking dependencies..."
if ! python -c "import flask, cv2, ultralytics" &> /dev/null; then
    echo "❌ Some packages are missing. Installing..."
    pip install -r requirements.txt
fi

echo "🤖 Loading AI model (this may take a moment on first run)..."
echo "   Downloading YOLOv8 model (~6MB) if not already cached..."
echo ""

# Start the application
echo "🚀 Starting Safety Monitor Web Application..."
echo "   Access dashboard at: http://localhost:8080"
echo "   Press Ctrl+C to stop"
echo ""

python web_interface.py 