# SafetyMaster Pro v1.0 - User Guide

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
