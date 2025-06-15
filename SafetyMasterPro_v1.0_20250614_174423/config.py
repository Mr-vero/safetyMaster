"""
Configuration file for Safety Monitor Application
Customize safety requirements, detection parameters, and system settings.
"""

import os
from typing import Dict, List

class SafetyConfig:
    """Configuration class for safety monitoring system."""
    
    # Detection Model Settings
    MODEL_CONFIDENCE_THRESHOLD = 0.5
    MODEL_PATH = None  # Set to path for custom model, None for default YOLOv8
    DEVICE = 'auto'  # 'auto', 'cpu', or 'cuda'
    
    # Required Safety Equipment
    # Customize this list based on your workplace requirements
    REQUIRED_SAFETY_EQUIPMENT = [
        'hard_hat',      # Hard hats/helmets
        'safety_vest',   # High-visibility safety vests
        # 'safety_glasses',  # Uncomment if safety glasses are required
        # 'gloves',          # Uncomment if gloves are required
        # 'boots'            # Uncomment if safety boots are required
    ]
    
    # Safety Equipment Detection Classes
    # Maps equipment types to possible class names in detection model
    SAFETY_EQUIPMENT_CLASSES = {
        'hard_hat': [
            'hard hat', 'helmet', 'safety helmet', 'construction helmet',
            'hardhat', 'hard_hat', 'safety_helmet'
        ],
        'safety_vest': [
            'safety vest', 'high vis vest', 'reflective vest', 'hi-vis vest',
            'safety_vest', 'high_vis_vest', 'reflective_vest', 'vest'
        ],
        'safety_glasses': [
            'safety glasses', 'goggles', 'eye protection', 'safety goggles',
            'safety_glasses', 'protective_glasses', 'eyewear'
        ],
        'gloves': [
            'gloves', 'safety gloves', 'work gloves', 'protective gloves',
            'safety_gloves', 'work_gloves'
        ],
        'boots': [
            'safety boots', 'work boots', 'steel toe boots', 'protective boots',
            'safety_boots', 'work_boots', 'steel_toe_boots'
        ]
    }
    
    # Detection Parameters
    PROXIMITY_THRESHOLD = 0.3  # How close equipment must be to person (relative to person height)
    PERSON_MIN_CONFIDENCE = 0.4  # Minimum confidence for person detection
    EQUIPMENT_MIN_CONFIDENCE = 0.3  # Minimum confidence for equipment detection
    
    # Camera Settings
    DEFAULT_CAMERA_SOURCE = 0  # Default camera (0 for built-in webcam)
    CAMERA_RESOLUTION_WIDTH = 640
    CAMERA_RESOLUTION_HEIGHT = 480
    CAMERA_FPS = 30
    CAMERA_BUFFER_SIZE = 10
    
    # Image Capture Settings
    VIOLATION_CAPTURE_ENABLED = True
    VIOLATION_IMAGES_DIR = "violation_captures"
    VIOLATION_IMAGE_QUALITY = 95  # JPEG quality (1-100)
    MAX_VIOLATION_IMAGES = 1000  # Maximum number of violation images to keep
    
    # Web Interface Settings
    WEB_HOST = '0.0.0.0'
    WEB_PORT = 5000
    WEB_DEBUG = False
    SECRET_KEY = 'safety_monitor_secret_key_change_in_production'
    
    # Alert Settings
    VIOLATION_ALERT_ENABLED = True
    VIOLATION_ALERT_COOLDOWN = 5.0  # Seconds between alerts for same person
    VIOLATION_SOUND_ENABLED = False  # Enable sound alerts (requires audio libraries)
    
    # Logging Settings
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_TO_FILE = True
    LOG_FILE = 'safety_monitor.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Performance Settings
    MAX_PROCESSING_FPS = 30  # Limit processing FPS to reduce CPU usage
    FRAME_SKIP_THRESHOLD = 5  # Skip frames if processing falls behind
    MULTI_THREADING_ENABLED = True
    
    # Notification Settings (for future extensions)
    EMAIL_NOTIFICATIONS = False
    EMAIL_SMTP_SERVER = ''
    EMAIL_PORT = 587
    EMAIL_USERNAME = ''
    EMAIL_PASSWORD = ''
    EMAIL_RECIPIENTS = []
    
    WEBHOOK_NOTIFICATIONS = False
    WEBHOOK_URL = ''
    
    # Zone-based Detection (for future extensions)
    DETECTION_ZONES = []  # List of polygons defining detection areas
    ZONE_BASED_REQUIREMENTS = {}  # Different requirements per zone
    
    # Reporting Settings
    GENERATE_DAILY_REPORTS = False
    REPORT_OUTPUT_DIR = "reports"
    REPORT_FORMAT = "pdf"  # "pdf", "html", "csv"
    
    @classmethod
    def load_from_file(cls, config_file: str = 'safety_config.json'):
        """Load configuration from JSON file."""
        import json
        
        if not os.path.exists(config_file):
            return cls()
        
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # Update class attributes with loaded values
            for key, value in config_data.items():
                if hasattr(cls, key.upper()):
                    setattr(cls, key.upper(), value)
                    
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
        
        return cls()
    
    @classmethod
    def save_to_file(cls, config_file: str = 'safety_config.json'):
        """Save current configuration to JSON file."""
        import json
        
        config_data = {}
        for attr_name in dir(cls):
            if attr_name.isupper() and not attr_name.startswith('_'):
                config_data[attr_name.lower()] = getattr(cls, attr_name)
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            print(f"Configuration saved to {config_file}")
        except Exception as e:
            print(f"Error saving config file {config_file}: {e}")
    
    @classmethod
    def get_equipment_requirements_text(cls) -> str:
        """Get human-readable text of equipment requirements."""
        if not cls.REQUIRED_SAFETY_EQUIPMENT:
            return "No specific safety equipment required"
        
        equipment_names = {
            'hard_hat': 'Hard Hat/Helmet',
            'safety_vest': 'Safety Vest',
            'safety_glasses': 'Safety Glasses',
            'gloves': 'Safety Gloves',
            'boots': 'Safety Boots'
        }
        
        required_items = [equipment_names.get(item, item) for item in cls.REQUIRED_SAFETY_EQUIPMENT]
        
        if len(required_items) == 1:
            return f"Required: {required_items[0]}"
        elif len(required_items) == 2:
            return f"Required: {required_items[0]} and {required_items[1]}"
        else:
            return f"Required: {', '.join(required_items[:-1])}, and {required_items[-1]}"
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return list of warnings/errors."""
        warnings = []
        
        # Validate confidence thresholds
        if not (0.1 <= cls.MODEL_CONFIDENCE_THRESHOLD <= 1.0):
            warnings.append("MODEL_CONFIDENCE_THRESHOLD should be between 0.1 and 1.0")
        
        if not (0.1 <= cls.PERSON_MIN_CONFIDENCE <= 1.0):
            warnings.append("PERSON_MIN_CONFIDENCE should be between 0.1 and 1.0")
        
        if not (0.1 <= cls.EQUIPMENT_MIN_CONFIDENCE <= 1.0):
            warnings.append("EQUIPMENT_MIN_CONFIDENCE should be between 0.1 and 1.0")
        
        # Validate proximity threshold
        if not (0.1 <= cls.PROXIMITY_THRESHOLD <= 2.0):
            warnings.append("PROXIMITY_THRESHOLD should be between 0.1 and 2.0")
        
        # Validate camera settings
        if cls.CAMERA_RESOLUTION_WIDTH < 320 or cls.CAMERA_RESOLUTION_HEIGHT < 240:
            warnings.append("Camera resolution too low, may affect detection accuracy")
        
        if cls.CAMERA_FPS > 60:
            warnings.append("High FPS may impact performance")
        
        # Validate required equipment
        valid_equipment = set(cls.SAFETY_EQUIPMENT_CLASSES.keys())
        for item in cls.REQUIRED_SAFETY_EQUIPMENT:
            if item not in valid_equipment:
                warnings.append(f"Unknown safety equipment type: {item}")
        
        # Check directories
        if cls.VIOLATION_CAPTURE_ENABLED:
            os.makedirs(cls.VIOLATION_IMAGES_DIR, exist_ok=True)
        
        if cls.GENERATE_DAILY_REPORTS:
            os.makedirs(cls.REPORT_OUTPUT_DIR, exist_ok=True)
        
        return warnings


# Create a default configuration instance
config = SafetyConfig()

# Validate configuration on import
validation_warnings = config.validate_config()
if validation_warnings:
    print("Configuration Warnings:")
    for warning in validation_warnings:
        print(f"  - {warning}")

# Load custom configuration if available
if os.path.exists('safety_config.json'):
    config = SafetyConfig.load_from_file('safety_config.json')
    print("Loaded configuration from safety_config.json")
else:
    print("Using default configuration. Create 'safety_config.json' to customize settings.") 