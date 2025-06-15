# SafetyMaster Pro - Mac Setup Guide 🍎

## 🚀 Quick Start for Mac Users

There are now **4 easy ways** to run SafetyMaster Pro on your Mac:

---

## 🎯 Method 1: Double-Click App Bundle (EASIEST)

### ✅ **Recommended for most Mac users**

1. **Find the app**: Look for `SafetyMaster Pro.app` in your download folder
2. **Double-click**: Just double-click the app icon
3. **Grant permissions**: Allow camera access when prompted
4. **Wait**: The app will automatically open your browser to http://localhost:8080

### 🔒 **If you get a security warning:**
- Right-click the app → "Open" → "Open" (this bypasses Gatekeeper)
- Or go to System Preferences → Security & Privacy → "Open Anyway"

---

## 🖥️ Method 2: Terminal Command File

### ✅ **For users comfortable with Terminal**

1. **Find the file**: Look for `START_SafetyMaster_Mac.command`
2. **Double-click**: This will open Terminal and start the app
3. **Follow prompts**: The script will guide you through setup

---

## 💻 Method 3: Manual Terminal (Advanced)

### ✅ **For developers and advanced users**

1. **Open Terminal** (Applications → Utilities → Terminal)
2. **Navigate to folder**:
   ```bash
   cd /path/to/SafetyMasterPro_folder
   ```
3. **Install dependencies**:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python3 web_interface.py
   ```
5. **Open browser**: Go to http://localhost:8080

---

## 🐳 Method 4: Docker (IT/Enterprise)

### ✅ **For IT teams and containerized deployment**

1. **Install Docker Desktop** from https://docker.com
2. **Open Terminal** and navigate to the project folder
3. **Build and run**:
   ```bash
   docker-compose up --build
   ```
4. **Access**: Open http://localhost:8080

---

## 🔧 Prerequisites

### **Required:**
- **macOS 10.14+** (Mojave or newer)
- **Python 3.8+** - Install from https://python.org/downloads/macos/
- **Webcam or USB camera**
- **4GB RAM minimum** (8GB recommended)

### **Optional but recommended:**
- **Homebrew** for easier Python management: https://brew.sh
  ```bash
  brew install python3
  ```

---

## 🎥 Camera Permissions

### **First time setup:**
1. When you first run the app, macOS will ask for camera permission
2. Click **"OK"** to allow camera access
3. If you accidentally denied it:
   - Go to **System Preferences** → **Security & Privacy** → **Camera**
   - Check the box next to **Terminal** or **SafetyMaster Pro**

---

## 🐛 Troubleshooting

### **"Python not found" error:**
```bash
# Install Python 3
brew install python3
# Or download from python.org
```

### **"Permission denied" error:**
```bash
# Make the script executable
chmod +x START_SafetyMaster_Mac.command
```

### **"App can't be opened" security warning:**
1. Right-click the app
2. Select "Open"
3. Click "Open" in the dialog

### **Camera not working:**
1. Check System Preferences → Security & Privacy → Camera
2. Make sure SafetyMaster Pro has permission
3. Try a different camera source in the web interface

### **Dependencies won't install:**
```bash
# Upgrade pip first
python3 -m pip install --upgrade pip
# Then try installing requirements again
python3 -m pip install -r requirements.txt
```

### **Port 8080 already in use:**
```bash
# Kill any existing processes
sudo lsof -ti:8080 | xargs kill -9
# Or use a different port
python3 web_interface.py --port 8081
```

---

## 🎮 Using SafetyMaster Pro

### **Once running:**
1. **Open browser**: Go to http://localhost:8080
2. **Start monitoring**: Click "Start Monitoring" button
3. **Grant camera access**: Allow when prompted
4. **Position camera**: Make sure people and safety equipment are visible
5. **Monitor compliance**: Watch real-time detection and statistics

### **Features:**
- ✅ **Real-time PPE detection**: Hard hats, safety vests, face masks
- ✅ **High performance**: 30+ FPS optimized
- ✅ **Clean interface**: Only shows equipment when worn
- ✅ **Violation tracking**: Real-time compliance monitoring
- ✅ **Statistics**: People count, compliance rate, violation log

---

## 🔒 Privacy & Security

### **Your data stays local:**
- ✅ All AI processing happens on your Mac
- ✅ No data sent to external servers
- ✅ Camera feed never leaves your device
- ✅ Optional violation image storage (local only)

---

## 📞 Support

### **If you need help:**
1. **Check the console**: Look for error messages in Terminal
2. **Verify requirements**: Make sure Python 3.8+ is installed
3. **Test camera**: Try other camera apps to verify hardware
4. **Restart**: Close and restart the application

### **Common solutions:**
- Update to latest macOS version
- Install latest Python from python.org
- Grant all necessary permissions
- Check internet connection for first-time model download

---

## 🎯 Performance Tips

### **For best results:**
- **Close other applications** to free up resources
- **Use good lighting** for better AI detection accuracy
- **Position camera** to clearly see people and safety equipment
- **Stable internet** for initial model downloads (first run only)

---

## ✅ Quick Checklist

Before running SafetyMaster Pro:
- [ ] Python 3.8+ installed
- [ ] Camera connected and working
- [ ] Camera permissions granted
- [ ] Internet connection available (first run)
- [ ] At least 4GB free RAM

---

**SafetyMaster Pro v1.0** - Professional AI-powered safety monitoring for Mac
🍎 Optimized for macOS with native app bundle support 