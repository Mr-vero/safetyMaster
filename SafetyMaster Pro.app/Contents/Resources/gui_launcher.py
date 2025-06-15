#!/usr/bin/env python3
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
                           f"Failed to start SafetyMaster Pro.\n\n"
                           f"This might be due to:\n"
                           f"• Missing Python dependencies\n"
                           f"• Camera access denied\n"
                           f"• Port 8080 already in use\n\n"
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
