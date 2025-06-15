@echo off
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
