#!/usr/bin/env python3
"""
Build script for creating SafetyMaster Pro standalone executable
Uses PyInstaller to create a distributable executable
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def create_spec_file():
    """Create PyInstaller spec file for SafetyMaster Pro."""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['web_interface.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('*.pt', '.'),
        ('*.html', '.'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'engineio.async_drivers.threading',
        'socketio',
        'flask_socketio',
        'ultralytics',
        'torch',
        'torchvision',
        'cv2',
        'numpy',
        'PIL',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SafetyMasterPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('SafetyMasterPro.spec', 'w') as f:
        f.write(spec_content.strip())
    
    print("✅ Created PyInstaller spec file")

def build_executable():
    """Build the standalone executable."""
    print("🔨 Building SafetyMaster Pro executable...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build executable
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'SafetyMasterPro.spec'
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        print(f"📁 Executable location: {os.path.abspath('dist/SafetyMasterPro')}")
        
        # Create distribution folder
        dist_folder = "SafetyMasterPro_Distribution"
        if os.path.exists(dist_folder):
            shutil.rmtree(dist_folder)
        
        os.makedirs(dist_folder)
        
        # Copy executable
        if os.path.exists('dist/SafetyMasterPro'):
            if sys.platform == "win32":
                shutil.copy2('dist/SafetyMasterPro.exe', dist_folder)
            else:
                shutil.copy2('dist/SafetyMasterPro', dist_folder)
        
        # Copy additional files
        files_to_copy = [
            'README.md',
            'requirements.txt',
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, dist_folder)
        
        # Copy model files
        for model_file in Path('.').glob('*.pt'):
            shutil.copy2(model_file, dist_folder)
        
        # Copy templates if they exist
        if os.path.exists('templates'):
            shutil.copytree('templates', os.path.join(dist_folder, 'templates'))
        
        print(f"📦 Distribution package created: {dist_folder}/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def create_installer_script():
    """Create installation script for users."""
    
    # Windows batch script
    windows_script = '''@echo off
echo SafetyMaster Pro - Installation Script
echo =====================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Installing SafetyMaster Pro dependencies...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run SafetyMaster Pro:
echo   python web_interface.py
echo.
echo Or use the executable:
echo   SafetyMasterPro.exe
echo.
pause
'''
    
    # Unix shell script
    unix_script = '''#!/bin/bash
echo "SafetyMaster Pro - Installation Script"
echo "====================================="
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "Installing SafetyMaster Pro dependencies..."
pip3 install -r requirements.txt

echo
echo "Installation complete!"
echo
echo "To run SafetyMaster Pro:"
echo "  python3 web_interface.py"
echo
echo "Or use the executable:"
echo "  ./SafetyMasterPro"
echo
'''
    
    # Write scripts
    with open('SafetyMasterPro_Distribution/install.bat', 'w') as f:
        f.write(windows_script)
    
    with open('SafetyMasterPro_Distribution/install.sh', 'w') as f:
        f.write(unix_script)
    
    # Make shell script executable
    if sys.platform != "win32":
        os.chmod('SafetyMasterPro_Distribution/install.sh', 0o755)
    
    print("✅ Installation scripts created")

def main():
    """Main build process."""
    print("🚀 SafetyMaster Pro - Build Script")
    print("=" * 40)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if build_executable():
        create_installer_script()
        
        print("\n🎉 Build completed successfully!")
        print("\n📦 Distribution package contents:")
        print("   - SafetyMasterPro executable")
        print("   - Model files (*.pt)")
        print("   - Templates folder")
        print("   - README.md")
        print("   - requirements.txt")
        print("   - install.bat (Windows)")
        print("   - install.sh (Unix/Linux/Mac)")
        
        print(f"\n📁 Package location: {os.path.abspath('SafetyMasterPro_Distribution')}")
        print("\n✅ Ready for distribution!")
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 