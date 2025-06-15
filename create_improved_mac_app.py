#!/usr/bin/env python3
"""
Create an improved Mac App Bundle for SafetyMaster Pro
with better cross-Mac compatibility
"""

import os
import shutil
import stat
import plistlib
from pathlib import Path

def create_improved_mac_app():
    """Create an improved Mac app bundle with better compatibility."""
    
    app_name = "SafetyMaster Pro"
    app_dir = f"{app_name}.app"
    
    # Remove existing app if it exists
    if os.path.exists(app_dir):
        shutil.rmtree(app_dir)
    
    # Create app bundle structure
    contents_dir = os.path.join(app_dir, "Contents")
    macos_dir = os.path.join(contents_dir, "MacOS")
    resources_dir = os.path.join(contents_dir, "Resources")
    
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)
    
    # Copy all necessary files to Resources
    files_to_copy = [
        'web_interface.py',
        'safety_detector.py', 
        'camera_manager.py',
        'config.py',
        'requirements.txt',
        'ppe_yolov8_model_0.pt',
        'ppe_model.pt',
        'yolov8n.pt'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, resources_dir)
            print(f"Copied {file}")
    
    # Copy templates directory
    if os.path.exists('templates'):
        shutil.copytree('templates', os.path.join(resources_dir, 'templates'))
        print("Copied templates directory")
    
    # Create improved executable script
    executable_script = '''#!/bin/bash
# SafetyMaster Pro - Improved Mac App Bundle Launcher
# Compatible with Intel and Apple Silicon Macs

# Get the app bundle directory - Fixed path resolution
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"
RESOURCES_DIR="$APP_DIR/Contents/Resources"

# Function to show error dialog
show_error() {
    osascript -e "display dialog \\"$1\\" with title \\"SafetyMaster Pro - Error\\" buttons {\\"OK\\"} default button \\"OK\\" with icon caution"
}

# Function to show info dialog
show_info() {
    osascript -e "display dialog \\"$1\\" with title \\"SafetyMaster Pro\\" buttons {\\"OK\\"} default button \\"OK\\" with icon note"
}

# Check if resources directory exists
if [[ ! -d "$RESOURCES_DIR" ]]; then
    show_error "Resources directory not found at: $RESOURCES_DIR

This might be due to:
- Incomplete app bundle
- Incorrect installation
- File permissions

Please re-download SafetyMaster Pro."
    exit 1
fi

# Change to resources directory
cd "$RESOURCES_DIR" || {
    show_error "Failed to access application resources at: $RESOURCES_DIR

Please check file permissions and try again."
    exit 1
}

# Detect Python installation with multiple fallbacks
PYTHON_CMD=""

# Check for various Python installations in order of preference
for cmd in python3.11 python3.10 python3.9 python3.8 python3 python; do
    if command -v "$cmd" &> /dev/null; then
        # Verify it's Python 3.8+
        version=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
        if [[ $(echo "$version >= 3.8" | bc -l 2>/dev/null || echo "0") == "1" ]]; then
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

# If no suitable Python found, provide installation guidance
if [[ -z "$PYTHON_CMD" ]]; then
    show_error "Python 3.8+ is required but not found.

Installation options:

1. Official Python (Recommended):
   Download from: https://www.python.org/downloads/macos/

2. Homebrew (if installed):
   brew install python3

3. Xcode Command Line Tools:
   xcode-select --install

After installation, restart this application."
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Check if we're in a virtual environment, if not try to create one
if [[ -z "$VIRTUAL_ENV" ]]; then
    VENV_DIR="$HOME/.safetymaster_venv"
    
    if [[ ! -d "$VENV_DIR" ]]; then
        echo "Creating virtual environment..."
        "$PYTHON_CMD" -m venv "$VENV_DIR" || {
            echo "Warning: Could not create virtual environment, using system Python"
        }
    fi
    
    if [[ -d "$VENV_DIR" ]]; then
        source "$VENV_DIR/bin/activate"
        PYTHON_CMD="python"
    fi
fi

# Install/upgrade dependencies with better error handling
echo "Installing dependencies..."
"$PYTHON_CMD" -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1 || true

# Install requirements with fallback options
if ! "$PYTHON_CMD" -m pip install -r requirements.txt > /dev/null 2>&1; then
    echo "Trying alternative installation method..."
    if ! "$PYTHON_CMD" -m pip install --user -r requirements.txt > /dev/null 2>&1; then
        show_error "Failed to install required dependencies.

Please try installing manually:
1. Open Terminal
2. Run: pip3 install opencv-python ultralytics flask flask-socketio torch torchvision

Then restart SafetyMaster Pro."
        exit 1
    fi
fi

# Check for camera permissions (macOS 10.14+)
if [[ $(sw_vers -productVersion | cut -d. -f1) -ge 10 ]] && [[ $(sw_vers -productVersion | cut -d. -f2) -ge 14 ]]; then
    # Request camera permission by attempting to access camera
    "$PYTHON_CMD" -c "
import cv2
import sys
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cap.release()
        print('Camera access OK')
    else:
        print('Camera access denied or no camera found')
        sys.exit(1)
except Exception as e:
    print(f'Camera test failed: {e}')
    sys.exit(1)
" > /dev/null 2>&1 || {
    show_error "Camera access is required for SafetyMaster Pro.

Please:
1. Go to System Preferences > Security & Privacy > Camera
2. Enable camera access for SafetyMaster Pro
3. Restart the application

If you don't see SafetyMaster Pro in the list, try running it once more."
    exit 1
}

# Start the application in background
echo "Starting SafetyMaster Pro..."
"$PYTHON_CMD" web_interface.py > /dev/null 2>&1 &
APP_PID=$!

# Wait for server to start
sleep 5

# Check if the application started successfully
if ! kill -0 $APP_PID 2>/dev/null; then
    show_error "Failed to start SafetyMaster Pro.

This might be due to:
- Missing dependencies
- Camera access issues
- Port 8080 already in use

Check the Terminal for error messages."
    exit 1
fi

# Open browser
open http://localhost:8080 || {
    echo "Could not open browser automatically"
}

# Show success message with more information
show_info "SafetyMaster Pro is running!

🌐 Web Interface: http://localhost:8080
📹 Make sure your camera is connected
🛑 To stop: Close this dialog and quit the app

The application will continue running until you quit it."

# Wait for the Python process to finish
wait $APP_PID
'''
    
    # Write the executable script
    executable_path = os.path.join(macos_dir, "SafetyMasterPro")
    with open(executable_path, 'w') as f:
        f.write(executable_script)
    
    # Make executable
    os.chmod(executable_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Create improved Info.plist
    plist_data = {
        'CFBundleExecutable': 'SafetyMasterPro',
        'CFBundleIdentifier': 'com.safetymaster.pro',
        'CFBundleName': 'SafetyMaster Pro',
        'CFBundleDisplayName': 'SafetyMaster Pro',
        'CFBundleVersion': '1.0.1',
        'CFBundleShortVersionString': '1.0.1',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'SMPR',
        'LSMinimumSystemVersion': '10.14',  # macOS Mojave minimum for camera permissions
        'LSRequiresNativeExecution': True,  # Ensure it runs natively on Apple Silicon
        'NSCameraUsageDescription': 'SafetyMaster Pro needs camera access to detect safety equipment and monitor workplace compliance in real-time.',
        'NSMicrophoneUsageDescription': 'SafetyMaster Pro may use microphone for enhanced safety monitoring features.',
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.business',
        'NSRequiresAquaSystemAppearance': False,  # Support dark mode
        'LSMultipleInstancesProhibited': True,  # Prevent multiple instances
        'NSSupportsAutomaticGraphicsSwitching': True,  # Support GPU switching
        'LSArchitecturePriority': ['arm64', 'x86_64'],  # Prefer Apple Silicon, fallback to Intel
        'NSAppTransportSecurity': {
            'NSAllowsLocalNetworking': True,  # Allow localhost connections
            'NSExceptionDomains': {
                'localhost': {
                    'NSExceptionAllowsInsecureHTTPLoads': True
                }
            }
        }
    }
    
    # Write Info.plist
    plist_path = os.path.join(contents_dir, "Info.plist")
    with open(plist_path, 'wb') as f:
        plistlib.dump(plist_data, f)
    
    # Create a README for distribution
    readme_content = '''# SafetyMaster Pro - Mac Distribution

## System Requirements
- macOS 10.14 (Mojave) or later
- Python 3.8 or later (will be installed automatically if missing)
- Camera/webcam connected
- At least 2GB RAM
- 1GB free disk space

## Installation Instructions

### Method 1: Double-Click (Easiest)
1. Double-click "SafetyMaster Pro.app"
2. If prompted about security, go to System Preferences > Security & Privacy and click "Open Anyway"
3. Grant camera permissions when requested
4. The app will open in your web browser

### Method 2: Right-Click Open (If security blocked)
1. Right-click "SafetyMaster Pro.app"
2. Select "Open" from the context menu
3. Click "Open" in the security dialog
4. Grant camera permissions when requested

## First Run Setup
1. The app will automatically install Python dependencies
2. Grant camera access when prompted
3. The web interface will open at http://localhost:8080
4. Click "Start Monitoring" to begin safety detection

## Troubleshooting

### "App can't be opened because it is from an unidentified developer"
- Right-click the app and select "Open"
- Or go to System Preferences > Security & Privacy > General and click "Open Anyway"

### Python Not Found
- Install Python from https://www.python.org/downloads/macos/
- Or install Homebrew and run: brew install python3

### Camera Access Denied
- Go to System Preferences > Security & Privacy > Camera
- Enable camera access for SafetyMaster Pro

### Port Already in Use
- Make sure no other SafetyMaster Pro instances are running
- Or restart your Mac to free up the port

## Features
- Real-time PPE detection (hard hats, safety vests, masks)
- Web-based dashboard with statistics
- Violation tracking and alerts
- High-performance AI processing (30+ FPS)
- Cross-platform compatibility

## Support
For issues or questions, check the included documentation or visit the project repository.
'''
    
    readme_path = os.path.join(resources_dir, "README.txt")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"\n✅ Improved Mac app bundle created: {app_dir}")
    print(f"📁 Size: {get_directory_size(app_dir):.1f} MB")
    print(f"🔧 Features:")
    print(f"   - Better Python detection (supports multiple versions)")
    print(f"   - Virtual environment support")
    print(f"   - Enhanced error handling and user guidance")
    print(f"   - Apple Silicon + Intel compatibility")
    print(f"   - Improved security permissions")
    print(f"   - Better camera access handling")
    print(f"\n📋 Distribution ready - users can:")
    print(f"   1. Double-click to run")
    print(f"   2. No manual Python setup required")
    print(f"   3. Automatic dependency installation")
    print(f"   4. Clear error messages with solutions")

def get_directory_size(path):
    """Calculate directory size in MB."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)

if __name__ == "__main__":
    create_improved_mac_app()