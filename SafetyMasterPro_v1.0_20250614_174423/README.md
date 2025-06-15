# 🔒 Safety Monitor - Real-time Safety Compliance Detection

A comprehensive computer vision application that uses AI to detect safety violations in real-time. The system monitors people in video feeds and checks if they're wearing required safety equipment like hard hats, safety vests, and other protective gear.

## ✨ Features

- **Real-time Detection**: Live monitoring of safety compliance using webcam or IP cameras
- **AI-Powered**: Uses YOLOv8 for accurate object detection and person tracking
- **Safety Equipment Detection**: Detects hard hats, safety vests, safety glasses, gloves, and boots
- **Web Dashboard**: Modern web interface with live video feed and statistics
- **Violation Alerts**: Automatic detection and logging of safety violations
- **Image Capture**: Automatically saves images when violations are detected
- **Multi-Camera Support**: Monitor multiple camera feeds simultaneously
- **Configurable**: Customizable safety requirements and detection parameters
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Installation

1. **Clone or download** this repository
2. **Install Python 3.8+** if not already installed
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

#### Option 1: Web Dashboard (Recommended)
```bash
python web_interface.py
```
Then open your browser to `http://localhost:5000`

#### Option 2: Command Line Demo
```bash
python demo.py
```

#### Option 3: Custom Script
```python
from safety_detector import SafetyDetector
from camera_manager import CameraManager

# Initialize detector
detector = SafetyDetector()

# Setup camera
camera = CameraManager(0)  # 0 for webcam
camera.start_capture()

# Process frames
while True:
    frame_data = camera.get_latest_frame()
    if frame_data:
        frame, timestamp = frame_data
        annotated_frame, analysis = detector.process_frame(frame)
        # Display or process results...
```

## 📖 Detailed Usage

### Web Interface

The web dashboard provides the most user-friendly experience:

1. **Start the web server**:
   ```bash
   python web_interface.py
   ```

2. **Open your browser** to `http://localhost:5000`

3. **Configure settings**:
   - Camera source (0 for webcam, URL for IP camera)
   - Detection confidence threshold
   - Click "Start Monitoring"

4. **Monitor in real-time**:
   - Live video feed with bounding boxes
   - Real-time statistics
   - Violation alerts and logs

### Command Line Demo

For testing and development:

```bash
# Basic usage with webcam
python demo.py

# Use video file
python demo.py --source path/to/video.mp4

# Use IP camera
python demo.py --source "http://192.168.1.100:8080/video"

# Adjust confidence threshold
python demo.py --confidence 0.7

# Save violation images
python demo.py --save-violations

# Full screen mode
python demo.py --fullscreen
```

**Demo Controls**:
- `SPACE`: Pause/Resume
- `S`: Save current frame
- `Q` or `ESC`: Quit

### Camera Sources

The system supports various input sources:

- **Webcam**: `0` (default), `1`, `2`, etc.
- **Video File**: `path/to/video.mp4`
- **IP Camera**: `http://192.168.1.100:8080/video`
- **RTSP Stream**: `rtsp://username:password@192.168.1.100:554/stream`

## ⚙️ Configuration

### Basic Configuration

Edit `config.py` or create `safety_config.json`:

```python
# Required safety equipment
REQUIRED_SAFETY_EQUIPMENT = [
    'hard_hat',      # Hard hats/helmets
    'safety_vest',   # High-visibility safety vests
    # 'safety_glasses',  # Uncomment if required
    # 'gloves',          # Uncomment if required
]

# Detection parameters
MODEL_CONFIDENCE_THRESHOLD = 0.5
PROXIMITY_THRESHOLD = 0.3
```

### Advanced Configuration

Create `safety_config.json` for persistent settings:

```json
{
  "required_safety_equipment": ["hard_hat", "safety_vest"],
  "model_confidence_threshold": 0.6,
  "camera_resolution_width": 1280,
  "camera_resolution_height": 720,
  "violation_capture_enabled": true,
  "web_port": 5000
}
```

## 🎯 Safety Equipment Detection

The system can detect the following safety equipment:

| Equipment | Detection Classes |
|-----------|-------------------|
| **Hard Hat** | hard hat, helmet, safety helmet, construction helmet |
| **Safety Vest** | safety vest, high vis vest, reflective vest, hi-vis vest |
| **Safety Glasses** | safety glasses, goggles, eye protection, safety goggles |
| **Gloves** | gloves, safety gloves, work gloves, protective gloves |
| **Safety Boots** | safety boots, work boots, steel toe boots, protective boots |

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Camera**: USB webcam or IP camera

### Recommended Requirements
- **CPU**: Intel i5 or AMD Ryzen 5 (for real-time processing)
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)
- **RAM**: 8GB or more
- **Network**: Stable connection for IP cameras

## 🔧 Installation Options

### Option 1: pip install (Standard)
```bash
pip install -r requirements.txt
```

### Option 2: Conda Environment
```bash
conda create -n safety-monitor python=3.9
conda activate safety-monitor
pip install -r requirements.txt
```

### Option 3: Docker (Coming Soon)
```bash
docker build -t safety-monitor .
docker run -p 5000:5000 --device=/dev/video0 safety-monitor
```

## 📊 Output and Logging

### Violation Images
- Saved to `violation_captures/` directory
- Includes timestamp and metadata
- Configurable image quality and retention

### Log Files
- Application logs in `safety_monitor.log`
- Violation records with timestamps
- Performance metrics

### Web API Endpoints
- `GET /api/status` - System status
- `POST /api/start_monitoring` - Start monitoring
- `POST /api/stop_monitoring` - Stop monitoring
- `GET /api/violations` - Recent violations

## 🔍 Troubleshooting

### Common Issues

**Camera not detected**:
```bash
# List available cameras (Linux/macOS)
ls /dev/video*

# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera works!' if cap.isOpened() else 'Camera failed')"
```

**Low detection accuracy**:
- Ensure good lighting conditions
- Check camera resolution and focus
- Adjust confidence threshold in configuration
- Consider training a custom model for your specific environment

**Performance issues**:
- Reduce camera resolution in `config.py`
- Lower the FPS limit
- Enable GPU acceleration if available
- Close other resource-intensive applications

**Module import errors**:
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

### Getting Help

1. Check the [troubleshooting section](#-troubleshooting)
2. Review the configuration in `config.py`
3. Check the log files for error messages
4. Ensure your camera and lighting setup is optimal

## 🛠️ Development

### Project Structure
```
safety-monitor/
├── safety_detector.py      # Core detection logic
├── camera_manager.py       # Camera handling
├── web_interface.py        # Web dashboard
├── demo.py                 # Command-line demo
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── templates/
│   └── dashboard.html      # Web dashboard template
├── violation_captures/     # Saved violation images
└── README.md              # This file
```

### Adding Custom Models

1. Train a custom YOLO model with your safety equipment
2. Save the model as `.pt` file
3. Update `config.py` with the model path:
   ```python
   MODEL_PATH = "path/to/your/custom_model.pt"
   ```

### Extending Functionality

- Add new safety equipment types in `config.py`
- Implement email/SMS notifications
- Add database integration for violation tracking
- Create mobile app interface
- Implement zone-based detection

## 📝 License

This project is provided as-is for educational and commercial use. Please ensure compliance with local privacy laws when deploying camera-based monitoring systems.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional safety equipment detection
- Better web interface features
- Mobile app development
- Performance optimizations
- Documentation improvements

## 📞 Support

For technical support or questions:
- Check the troubleshooting section above
- Review the configuration options
- Ensure proper hardware setup
- Test with the demo script first

---

## 🎉 Get Started Now!

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Run the web interface**: `python web_interface.py`
3. **Open your browser**: `http://localhost:5000`
4. **Start monitoring**: Click "Start Monitoring" in the dashboard

**Stay safe and compliant with AI-powered monitoring!** 🔒👷‍♂️ 