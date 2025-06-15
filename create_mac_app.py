#!/usr/bin/env python3
"""
Create a Mac .app bundle for SafetyMaster Pro
This creates a double-clickable application for Mac users
"""

import os
import shutil
import stat
from pathlib import Path

def create_mac_app():
    """Create a Mac .app bundle for SafetyMaster Pro."""
    print("🍎 Creating SafetyMaster Pro Mac App Bundle")
    print("=" * 45)
    
    app_name = "SafetyMaster Pro"
    app_bundle = f"{app_name}.app"
    
    # Remove existing app bundle
    if os.path.exists(app_bundle):
        shutil.rmtree(app_bundle)
    
    # Create app bundle structure
    contents_dir = os.path.join(app_bundle, "Contents")
    macos_dir = os.path.join(contents_dir, "MacOS")
    resources_dir = os.path.join(contents_dir, "Resources")
    
    os.makedirs(macos_dir)
    os.makedirs(resources_dir)
    
    print(f"📁 Created app bundle structure: {app_bundle}")
    
    # Create Info.plist
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>SafetyMasterPro</string>
    <key>CFBundleIdentifier</key>
    <string>com.safetymaster.pro</string>
    <key>CFBundleName</key>
    <string>SafetyMaster Pro</string>
    <key>CFBundleDisplayName</key>
    <string>SafetyMaster Pro</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>SMPR</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSCameraUsageDescription</key>
    <string>SafetyMaster Pro needs camera access to detect safety equipment and monitor compliance.</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.business</string>
</dict>
</plist>"""
    
    with open(os.path.join(contents_dir, "Info.plist"), "w") as f:
        f.write(info_plist)
    
    print("✅ Created Info.plist")
    
    # Create the main executable script
    executable_script = f"""#!/bin/bash
# SafetyMaster Pro - Mac App Bundle Launcher

# Get the app bundle directory
APP_DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )/.." && pwd )"
RESOURCES_DIR="$APP_DIR/Contents/Resources"

# Change to resources directory
cd "$RESOURCES_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 is required but not installed.\\n\\nPlease install Python 3.8+ from:\\nhttps://www.python.org/downloads/macos/\\n\\nOr install using Homebrew:\\nbrew install python3" with title "SafetyMaster Pro - Python Required" buttons {{"OK"}} default button "OK" with icon caution'
    exit 1
fi

# Install dependencies silently
python3 -m pip install --user -r requirements.txt > /dev/null 2>&1

# Start the application
python3 web_interface.py &

# Wait a moment then open browser
sleep 3
open http://localhost:8080

# Show success message
osascript -e 'display dialog "SafetyMaster Pro is starting!\\n\\nThe web interface will open in your browser at:\\nhttp://localhost:8080\\n\\nMake sure your camera is connected." with title "SafetyMaster Pro Started" buttons {{"OK"}} default button "OK" with icon note'

# Keep the process running
wait
"""
    
    executable_path = os.path.join(macos_dir, "SafetyMasterPro")
    with open(executable_path, "w") as f:
        f.write(executable_script)
    
    # Make executable
    os.chmod(executable_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    print("✅ Created executable launcher")
    
    # Copy all necessary files to Resources
    files_to_copy = [
        'web_interface.py',
        'safety_detector.py', 
        'camera_manager.py',
        'config.py',
        'requirements.txt',
        'README.md',
    ]
    
    print("📄 Copying Python files...")
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, resources_dir)
            print(f"   ✅ {file}")
    
    # Copy model files
    print("🤖 Copying AI models...")
    for model_file in Path('.').glob('*.pt'):
        shutil.copy2(model_file, resources_dir)
        print(f"   ✅ {model_file.name}")
    
    # Copy templates
    if os.path.exists('templates'):
        shutil.copytree('templates', os.path.join(resources_dir, 'templates'))
        print("   ✅ templates/ folder")
    
    print(f"\n🎉 Mac app bundle created: {app_bundle}")
    print(f"📱 Users can now double-click '{app_bundle}' to run SafetyMaster Pro")
    print(f"📦 App bundle size: {get_folder_size(app_bundle):.1f} MB")
    
    return app_bundle

def get_folder_size(folder_path):
    """Get the size of a folder in MB."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)

def create_installer_dmg():
    """Create a DMG installer for the Mac app."""
    print("\n💿 Creating DMG installer...")
    
    # This would require additional tools like create-dmg
    # For now, just provide instructions
    print("💡 To create a DMG installer:")
    print("   1. Install create-dmg: brew install create-dmg")
    print("   2. Run: create-dmg --volname 'SafetyMaster Pro' --window-pos 200 120 --window-size 600 300 --icon-size 100 --icon 'SafetyMaster Pro.app' 175 120 --hide-extension 'SafetyMaster Pro.app' --app-drop-link 425 120 'SafetyMaster Pro.dmg' 'SafetyMaster Pro.app'")

def main():
    """Main function."""
    try:
        app_bundle = create_mac_app()
        
        print(f"\n📋 Mac Distribution Summary:")
        print(f"   🍎 App Bundle: {app_bundle}")
        print(f"   📱 Double-clickable: Yes")
        print(f"   🔒 Camera permissions: Handled automatically")
        print(f"   🌐 Auto-opens browser: Yes")
        
        print(f"\n✅ Ready for Mac users!")
        print(f"   Users can simply double-click '{app_bundle}' to start")
        
        # Also update the distribution package
        dist_folder = "SafetyMasterPro_v1.0_20250614_174423"
        if os.path.exists(dist_folder):
            print(f"\n📦 Adding to distribution package...")
            shutil.copytree(app_bundle, os.path.join(dist_folder, app_bundle))
            print(f"   ✅ Added {app_bundle} to {dist_folder}/")
        
        create_installer_dmg()
        
    except Exception as e:
        print(f"❌ Error creating Mac app: {e}")

if __name__ == "__main__":
    main() 