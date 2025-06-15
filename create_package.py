#!/usr/bin/env python3
"""
Create distributable package for SafetyMaster Pro
Creates a ZIP file with all necessary components for easy sharing
"""

import os
import shutil
import zipfile
from pathlib import Path
import datetime

def create_distribution_package():
    """Create a complete distribution package."""
    print("📦 Creating SafetyMaster Pro Distribution Package")
    print("=" * 50)
    
    # Create distribution folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dist_name = f"SafetyMasterPro_v1.0_{timestamp}"
    dist_folder = f"{dist_name}"
    
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    
    os.makedirs(dist_folder)
    print(f"📁 Created distribution folder: {dist_folder}")
    
    # Files to include in distribution
    files_to_copy = [
        'web_interface.py',
        'safety_detector.py',
        'camera_manager.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'high_fps_test.py',
        'test_improved_detection.py',
        'test_camera.py',
    ]
    
    # Copy Python files
    print("📄 Copying Python files...")
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_folder)
            print(f"   ✅ {file}")
        else:
            print(f"   ⚠️  {file} not found")
    
    # Copy model files
    print("🤖 Copying AI model files...")
    model_files = list(Path('.').glob('*.pt'))
    for model_file in model_files:
        shutil.copy2(model_file, dist_folder)
        print(f"   ✅ {model_file.name}")
    
    # Copy templates folder
    if os.path.exists('templates'):
        print("🎨 Copying templates...")
        shutil.copytree('templates', os.path.join(dist_folder, 'templates'))
        print("   ✅ templates/ folder")
    
    # Copy test files
    test_files = [
        'test_websocket.html',
        'demo.py',
        'demo_simple.py',
    ]
    
    print("🧪 Copying test files...")
    for file in test_files:
        if os.path.exists(file):
            shutil.copy2(file, dist_folder)
            print(f"   ✅ {file}")
    
    # Create startup scripts
    create_startup_scripts(dist_folder)
    
    # Create user guide
    create_user_guide(dist_folder)
    
    # Create ZIP package
    zip_filename = f"{dist_name}.zip"
    print(f"🗜️  Creating ZIP package: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, dist_folder)
                zipf.write(file_path, arc_name)
    
    # Get package size
    zip_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
    
    print(f"\n🎉 Package created successfully!")
    print(f"📦 Package: {zip_filename}")
    print(f"📏 Size: {zip_size:.1f} MB")
    print(f"📁 Folder: {dist_folder}/")
    
    return zip_filename, dist_folder

def create_startup_scripts(dist_folder):
    """Create easy startup scripts for users."""
    print("🚀 Creating startup scripts...")
    
    # Windows batch script
    windows_script = '''@echo off
title SafetyMaster Pro
echo.
echo  ███████╗ █████╗ ███████╗███████╗████████╗██╗   ██╗
echo  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝╚██╗ ██╔╝
echo  ███████╗███████║█████╗  █████╗     ██║    ╚████╔╝ 
echo  ╚════██║██╔══██║██╔══╝  ██╔══╝     ██║     ╚██╔╝  
echo  ███████║██║  ██║██║     ███████╗   ██║      ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝   ╚═╝      ╚═╝   
echo.
echo                    MASTER PRO v1.0
echo           Real-time AI Safety Equipment Detection
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
echo.
echo Installing dependencies (first time only)...
pip install -r requirements.txt >nul 2>&1

echo.
echo 🚀 Starting SafetyMaster Pro...
echo 🌐 Web interface will open at: http://localhost:8080
echo 📹 Make sure your camera is connected
echo.
echo Press Ctrl+C to stop the application
echo.

python web_interface.py
pause
'''
    
    # Unix shell script
    unix_script = '''#!/bin/bash
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
'''
    
    # Write scripts
    with open(os.path.join(dist_folder, 'START_SafetyMaster.bat'), 'w') as f:
        f.write(windows_script)
    
    with open(os.path.join(dist_folder, 'START_SafetyMaster.sh'), 'w') as f:
        f.write(unix_script)
    
    # Make shell script executable
    os.chmod(os.path.join(dist_folder, 'START_SafetyMaster.sh'), 0o755)
    
    print("   ✅ START_SafetyMaster.bat (Windows)")
    print("   ✅ START_SafetyMaster.sh (Unix/Linux/Mac)")

def create_user_guide(dist_folder):
    """Create a comprehensive user guide."""
    print("📖 Creating user guide...")
    
    user_guide = '''# SafetyMaster Pro v1.0 - User Guide

## 🚀 Quick Start

### Windows Users:
1. Double-click `START_SafetyMaster.bat`
2. Wait for installation to complete
3. Open your web browser to: http://localhost:8080

### Mac/Linux Users:
1. Open terminal in this folder
2. Run: `./START_SafetyMaster.sh`
3. Open your web browser to: http://localhost:8080

## 📋 Requirements

- **Python 3.8+** (Download from https://python.org)
- **Webcam or USB camera**
- **Internet connection** (for first-time model download)
- **4GB RAM minimum** (8GB recommended)

## 🎯 Features

- **Real-time PPE Detection**: Hard hats, safety vests, face masks
- **High-Performance**: Optimized for 30+ FPS
- **Web Interface**: Modern, responsive dashboard
- **Violation Alerts**: Real-time safety compliance monitoring
- **Multi-Platform**: Windows, Mac, Linux support

## 🔧 Manual Installation

If the automatic scripts don't work:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python web_interface.py
```

## 🎮 Controls

- **Start Monitoring**: Click "Start Monitoring" in the web interface
- **Stop Monitoring**: Click "Stop Monitoring"
- **Fullscreen**: Click the fullscreen button for immersive view
- **Settings**: Adjust camera source and detection settings

## 🎨 Interface Features

- **Live Video Feed**: Real-time camera with AI detection overlays
- **Statistics Panel**: People count, compliance rate, violations
- **Violation Log**: Real-time alerts with timestamps
- **FPS Counter**: Performance monitoring
- **Responsive Design**: Works on desktop, tablet, mobile

## 🔍 Detection Classes

The AI model detects:
- ✅ **Hard Hat** (Green boxes when worn)
- ✅ **Safety Vest** (Yellow boxes when worn)  
- ✅ **Face Mask** (Blue boxes when worn)
- ❌ **Violations** (Red person boxes when equipment missing)

## ⚡ Performance Tips

- **Close other applications** for better performance
- **Use good lighting** for better detection accuracy
- **Position camera** to clearly see people and equipment
- **Stable internet** for model downloads

## 🐛 Troubleshooting

### Camera Issues:
- Check camera permissions
- Try different camera source (0, 1, 2...)
- Restart the application

### Performance Issues:
- Close other applications
- Lower camera resolution
- Check system requirements

### Installation Issues:
- Update Python to latest version
- Run as administrator (Windows)
- Check internet connection

## 📞 Support

For technical support or questions:
- Check the README.md file
- Review error messages in the console
- Ensure all requirements are met

## 🔒 Privacy

- All processing is done locally on your computer
- No data is sent to external servers
- Camera feed stays on your device

---

**SafetyMaster Pro v1.0** - Professional AI-powered safety monitoring
'''
    
    with open(os.path.join(dist_folder, 'USER_GUIDE.md'), 'w') as f:
        f.write(user_guide)
    
    print("   ✅ USER_GUIDE.md")

def main():
    """Main packaging process."""
    try:
        zip_file, dist_folder = create_distribution_package()
        
        print(f"\n📋 Distribution Package Summary:")
        print(f"   📦 ZIP File: {zip_file}")
        print(f"   📁 Folder: {dist_folder}/")
        print(f"   🚀 Startup: START_SafetyMaster.bat/.sh")
        print(f"   📖 Guide: USER_GUIDE.md")
        
        print(f"\n✅ Ready to share!")
        print(f"   Users can simply:")
        print(f"   1. Extract the ZIP file")
        print(f"   2. Run the startup script")
        print(f"   3. Open http://localhost:8080")
        
    except Exception as e:
        print(f"❌ Error creating package: {e}")

if __name__ == "__main__":
    main() 