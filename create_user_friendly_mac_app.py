#!/usr/bin/env python3
"""
Create a User-Friendly Mac App Bundle for SafetyMaster Pro
with proper GUI interface and clear user guidance
"""

import os
import shutil
import stat
import plistlib
from pathlib import Path

def create_user_friendly_mac_app():
    """Create a Mac app bundle with proper user interface."""
    
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
    
    # Create a Python GUI launcher script
    gui_launcher_script = '''#!/usr/bin/env python3
"""
SafetyMaster Pro - Mac GUI Launcher
Provides a proper user interface with status window and controls
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import webbrowser
import sys
import os
import signal
from pathlib import Path

class SafetyMasterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SafetyMaster Pro")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Set app icon and styling
        self.setup_styling()
        
        # Variables
        self.server_process = None
        self.is_running = False
        self.status_var = tk.StringVar(value="Ready to start")
        
        # Create GUI
        self.create_widgets()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_styling(self):
        """Setup the GUI styling."""
        self.root.configure(bg='#2c3e50')
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Status.TLabel', 
                       background='#2c3e50', 
                       foreground='#3498db', 
                       font=('Arial', 10))
        
        style.configure('Action.TButton', 
                       font=('Arial', 12, 'bold'))
        
    def create_widgets(self):
        """Create the GUI widgets."""
        # Title
        title_label = ttk.Label(self.root, 
                               text="SafetyMaster Pro", 
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ttk.Label(self.root, 
                                  text="Real-time AI Safety Equipment Detection", 
                                  background='#2c3e50', 
                                  foreground='#95a5a6', 
                                  font=('Arial', 10))
        subtitle_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#34495e', relief='sunken', bd=2)
        status_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(status_frame, 
                 text="Status:", 
                 background='#34495e', 
                 foreground='#ecf0f1', 
                 font=('Arial', 10, 'bold')).pack(side='left', padx=10, pady=5)
        
        ttk.Label(status_frame, 
                 textvariable=self.status_var, 
                 style='Status.TLabel').pack(side='left', padx=10, pady=5)
        
        # Main buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(pady=20)
        
        # Start/Stop button
        self.start_button = ttk.Button(buttons_frame, 
                                      text="🚀 Start Safety Monitoring", 
                                      command=self.toggle_monitoring,
                                      style='Action.TButton')
        self.start_button.pack(pady=10)
        
        # Open Dashboard button
        self.dashboard_button = ttk.Button(buttons_frame, 
                                          text="🌐 Open Dashboard", 
                                          command=self.open_dashboard,
                                          state='disabled')
        self.dashboard_button.pack(pady=5)
        
        # Info frame
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Instructions
        instructions = """
📋 How to use SafetyMaster Pro:

1. Click "Start Safety Monitoring" to begin
2. Grant camera permissions when prompted
3. Click "Open Dashboard" to view the web interface
4. The system will detect:
   • Hard hats and helmets
   • Safety vests and high-vis clothing
   • Face masks and protective equipment
   • Safety violations in real-time

🎯 Features:
• Real-time AI detection (30+ FPS)
• Web-based dashboard with statistics
• Violation tracking and alerts
• Cross-platform compatibility

⚠️ Requirements:
• Camera/webcam connected
• Python 3.8+ (auto-installed if needed)
• macOS 10.14+ (Mojave or later)
        """
        
        info_text = tk.Text(info_frame, 
                           wrap='word', 
                           bg='#34495e', 
                           fg='#ecf0f1', 
                           font=('Arial', 9),
                           relief='flat',
                           state='disabled')
        info_text.pack(fill='both', expand=True)
        info_text.config(state='normal')
        info_text.insert('1.0', instructions)
        info_text.config(state='disabled')
        
        # Footer
        footer_label = ttk.Label(self.root, 
                                text="SafetyMaster Pro v1.1 - Professional Safety Monitoring", 
                                background='#2c3e50', 
                                foreground='#7f8c8d', 
                                font=('Arial', 8))
        footer_label.pack(side='bottom', pady=10)
        
    def toggle_monitoring(self):
        """Start or stop the monitoring system."""
        if not self.is_running:
            self.start_monitoring()
        else:
            self.stop_monitoring()
            
    def start_monitoring(self):
        """Start the SafetyMaster Pro monitoring system."""
        self.status_var.set("Starting system...")
        self.start_button.config(text="⏳ Starting...", state='disabled')
        
        # Start in a separate thread
        threading.Thread(target=self._start_monitoring_thread, daemon=True).start()
        
    def _start_monitoring_thread(self):
        """Thread function to start monitoring."""
        try:
            # Check Python and dependencies
            self.root.after(0, lambda: self.status_var.set("Checking Python installation..."))
            
            # Start the web interface
            self.root.after(0, lambda: self.status_var.set("Starting web server..."))
            
            # Run the web interface
            self.server_process = subprocess.Popen([
                sys.executable, 'web_interface.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if process is still running
            if self.server_process.poll() is None:
                self.is_running = True
                self.root.after(0, self._monitoring_started)
            else:
                self.root.after(0, self._monitoring_failed)
                
        except Exception as e:
            self.root.after(0, lambda: self._monitoring_failed(str(e)))
            
    def _monitoring_started(self):
        """Called when monitoring starts successfully."""
        self.status_var.set("✅ SafetyMaster Pro is running!")
        self.start_button.config(text="🛑 Stop Monitoring", state='normal')
        self.dashboard_button.config(state='normal')
        
        # Auto-open dashboard
        self.open_dashboard()
        
    def _monitoring_failed(self, error=None):
        """Called when monitoring fails to start."""
        error_msg = f"Failed to start: {error}" if error else "Failed to start monitoring"
        self.status_var.set(f"❌ {error_msg}")
        self.start_button.config(text="🚀 Start Safety Monitoring", state='normal')
        
        messagebox.showerror("Error", 
                           f"Failed to start SafetyMaster Pro.\\n\\n"
                           f"This might be due to:\\n"
                           f"• Missing Python dependencies\\n"
                           f"• Camera access denied\\n"
                           f"• Port 8080 already in use\\n\\n"
                           f"Error: {error if error else 'Unknown error'}")
        
    def stop_monitoring(self):
        """Stop the monitoring system."""
        self.status_var.set("Stopping system...")
        self.start_button.config(text="⏳ Stopping...", state='disabled')
        
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
            
        self.is_running = False
        self.status_var.set("Stopped")
        self.start_button.config(text="🚀 Start Safety Monitoring", state='normal')
        self.dashboard_button.config(state='disabled')
        
    def open_dashboard(self):
        """Open the web dashboard in the default browser."""
        if self.is_running:
            webbrowser.open('http://localhost:8080')
        else:
            messagebox.showwarning("Warning", 
                                 "Please start the monitoring system first.")
            
    def on_closing(self):
        """Handle window closing."""
        if self.is_running:
            if messagebox.askokcancel("Quit", 
                                    "SafetyMaster Pro is still running. Do you want to stop it and quit?"):
                self.stop_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()

if __name__ == "__main__":
    # Change to the Resources directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Create and run the GUI
    app = SafetyMasterGUI()
    app.run()
'''
    
    # Write the GUI launcher script
    gui_launcher_path = os.path.join(resources_dir, "gui_launcher.py")
    with open(gui_launcher_path, 'w') as f:
        f.write(gui_launcher_script)
    
    # Create the main executable script
    executable_script = '''#!/bin/bash
# SafetyMaster Pro - User-Friendly Mac App Launcher
# Provides proper GUI interface instead of floating in background

# Get the app bundle directory - Fixed path resolution
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"
RESOURCES_DIR="$APP_DIR/Contents/Resources"

# Function to show error dialog
show_error() {
    osascript -e "display dialog \\"$1\\" with title \\"SafetyMaster Pro - Error\\" buttons {\\"OK\\"} default button \\"OK\\" with icon caution"
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
        if command -v bc &> /dev/null; then
            # Use bc if available
            if [[ $(echo "$version >= 3.8" | bc -l 2>/dev/null || echo "0") == "1" ]]; then
                PYTHON_CMD="$cmd"
                break
            fi
        else
            # Fallback comparison without bc
            major=$(echo "$version" | cut -d. -f1)
            minor=$(echo "$version" | cut -d. -f2)
            if [[ "$major" -gt 3 ]] || [[ "$major" -eq 3 && "$minor" -ge 8 ]]; then
                PYTHON_CMD="$cmd"
                break
            fi
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

# Check if we're in a virtual environment, if not try to create one
if [[ -z "$VIRTUAL_ENV" ]]; then
    VENV_DIR="$HOME/.safetymaster_venv"
    
    if [[ ! -d "$VENV_DIR" ]]; then
        # Show progress dialog
        osascript -e 'display dialog "Setting up SafetyMaster Pro for first use...\\n\\nThis may take a few minutes." with title "SafetyMaster Pro - Setup" buttons {"OK"} default button "OK" with icon note giving up after 3'
        
        "$PYTHON_CMD" -m venv "$VENV_DIR" || {
            echo "Warning: Could not create virtual environment, using system Python"
        }
    fi
    
    if [[ -d "$VENV_DIR" ]]; then
        source "$VENV_DIR/bin/activate"
        PYTHON_CMD="python"
    fi
fi

# Install/upgrade dependencies with progress indication
if [[ ! -f "$HOME/.safetymaster_deps_installed" ]]; then
    osascript -e 'display dialog "Installing required dependencies...\\n\\nThis is a one-time setup." with title "SafetyMaster Pro - Installing" buttons {"OK"} default button "OK" with icon note giving up after 3'
    
    "$PYTHON_CMD" -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1 || true
    
    # Install requirements with fallback options
    if "$PYTHON_CMD" -m pip install -r requirements.txt > /dev/null 2>&1; then
        touch "$HOME/.safetymaster_deps_installed"
    elif "$PYTHON_CMD" -m pip install --user -r requirements.txt > /dev/null 2>&1; then
        touch "$HOME/.safetymaster_deps_installed"
    else
        show_error "Failed to install required dependencies.

Please try installing manually:
1. Open Terminal
2. Run: pip3 install opencv-python ultralytics flask flask-socketio torch torchvision

Then restart SafetyMaster Pro."
        exit 1
    fi
fi

# Install tkinter if not available (for GUI)
"$PYTHON_CMD" -c "import tkinter" 2>/dev/null || {
    show_error "GUI components not available.

Please install tkinter:
1. If using Homebrew Python: brew install python-tk
2. If using system Python: Install from python.org

Then restart SafetyMaster Pro."
    exit 1
}

# Launch the GUI application
"$PYTHON_CMD" gui_launcher.py
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
        'CFBundleVersion': '1.1.0',
        'CFBundleShortVersionString': '1.1.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'SMPR',
        'LSMinimumSystemVersion': '10.14',
        'LSRequiresNativeExecution': True,
        'NSCameraUsageDescription': 'SafetyMaster Pro needs camera access to detect safety equipment and monitor workplace compliance in real-time.',
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.business',
        'NSRequiresAquaSystemAppearance': False,
        'LSMultipleInstancesProhibited': True,
        'NSSupportsAutomaticGraphicsSwitching': True,
        'LSArchitecturePriority': ['arm64', 'x86_64'],
        'NSAppTransportSecurity': {
            'NSAllowsLocalNetworking': True,
            'NSExceptionDomains': {
                'localhost': {
                    'NSExceptionAllowsInsecureHTTPLoads': True
                }
            }
        },
        'LSUIElement': False,  # Show in Dock and App Switcher
        'NSPrincipalClass': 'NSApplication'
    }
    
    # Write Info.plist
    plist_path = os.path.join(contents_dir, "Info.plist")
    with open(plist_path, 'wb') as f:
        plistlib.dump(plist_data, f)
    
    print(f"\n✅ User-Friendly Mac app bundle created: {app_dir}")
    print(f"📁 Size: {get_directory_size(app_dir):.1f} MB")
    print(f"🎯 New Features:")
    print(f"   - Proper GUI interface with status window")
    print(f"   - Clear start/stop controls")
    print(f"   - Built-in dashboard launcher")
    print(f"   - User-friendly instructions and guidance")
    print(f"   - No more 'floating' background processes")
    print(f"   - Professional appearance in Dock and App Switcher")
    print(f"\n🚀 User Experience:")
    print(f"   1. Double-click app → GUI window opens")
    print(f"   2. Click 'Start Monitoring' → System starts")
    print(f"   3. Click 'Open Dashboard' → Browser opens")
    print(f"   4. Clear status updates and controls")
    print(f"   5. Proper app lifecycle management")

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
    create_user_friendly_mac_app() 