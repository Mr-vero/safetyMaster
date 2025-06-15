import cv2
import numpy as np
from ultralytics import YOLO
import torch
import time
from datetime import datetime
import os
import json
from threading import Thread
import queue
from typing import Dict, List, Tuple, Optional
import requests

class SafetyDetector:
    """
    Real-time safety compliance detection system using YOLO for object detection.
    Detects people and safety equipment like hard hats, safety vests, and safety glasses.
    """
    
    def __init__(self, model_path: Optional[str] = None, confidence_threshold: float = 0.5):
        """
        Initialize the safety detector with a specialized PPE detection model.
        
        Args:
            model_path: Path to custom model, if None will download PPE model
            confidence_threshold: Minimum confidence for detections
        """
        self.confidence_threshold = confidence_threshold
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Stricter confidence thresholds for different equipment types to reduce false positives
        self.equipment_confidence_thresholds = {
            'hardhat': 0.7,      # Higher threshold for hard hats (hair confusion)
            'safety_vest': 0.75,  # Higher threshold for safety vests (clothing confusion)
            'mask': 0.6,         # Moderate threshold for masks
            'person': 0.5,       # Standard threshold for people
            'no_hardhat': 0.6,   # Moderate threshold for NO- detections
            'no_safety_vest': 0.6,
            'no_mask': 0.6
        }
        
        # Try to load a specialized PPE detection model
        self.model = self._load_ppe_model(model_path)
        
        # PPE class names - these are the actual classes we expect from PPE models
        self.ppe_classes = {
            'hardhat': ['Hardhat', 'hardhat', 'helmet', 'hard hat'],
            'safety_vest': ['Safety Vest', 'safety vest', 'vest', 'safety-vest', 'Safety-Vest'],
            'no_hardhat': ['NO-Hardhat', 'no-hardhat', 'no hardhat', 'NO-Helmet'],
            'no_safety_vest': ['NO-Safety Vest', 'no-safety-vest', 'no safety vest', 'NO-Safety-Vest'],
            'person': ['Person', 'person'],
            'mask': ['Mask', 'mask'],
            'no_mask': ['NO-Mask', 'no-mask', 'no mask'],
            'safety_gloves': ['Safety Gloves', 'safety-gloves', 'gloves', 'Gloves'],
            'safety_glasses': ['Safety Glasses', 'safety-glasses', 'glasses', 'Safety-Glasses'],
            'hearing_protection': ['Hearing Protection', 'hearing-protection', 'ear protection']
        }
        
        print(f"Using device: {self.device}")
        print(f"Loaded PPE detection model with stricter confidence thresholds")
        print(f"Equipment thresholds: {self.equipment_confidence_thresholds}")
        
        # Colors for bounding boxes
        self.colors = {
            'person': (0, 255, 0),          # Green for compliant person
            'violation': (0, 0, 255),       # Red for safety violation
            'equipment': (255, 255, 0),     # Yellow for safety equipment
            'warning': (0, 165, 255)        # Orange for warnings
        }
        
        # Violation tracking
        self.violations = []
        self.violation_images_dir = "violation_captures"
        os.makedirs(self.violation_images_dir, exist_ok=True)
        
    def _load_ppe_model(self, model_path: Optional[str] = None) -> YOLO:
        """Load a specialized PPE detection model."""
        if model_path and os.path.exists(model_path):
            print(f"Loading custom model from {model_path}")
            return YOLO(model_path)
        
        # Try to download YOLOv8-compatible PPE models
        ppe_model_urls = [
            # Try the snehilsanyal YOLOv8 PPE model (best.pt)
            "https://github.com/snehilsanyal/Construction-Site-Safety-PPE-Detection/raw/main/models/best.pt",
            # Try mayank13-01 YOLOv8 PPE model
            "https://github.com/mayank13-01/Yolov8-PPE/raw/main/YOLO-Weights/ppe.pt"
        ]
        
        for i, url in enumerate(ppe_model_urls):
            try:
                model_filename = f"ppe_yolov8_model_{i}.pt"
                if not os.path.exists(model_filename):
                    print(f"Downloading PPE detection model from {url}...")
                    response = requests.get(url, timeout=60)
                    if response.status_code == 200:
                        with open(model_filename, 'wb') as f:
                            f.write(response.content)
                        print(f"Downloaded PPE model successfully as {model_filename}")
                
                if os.path.exists(model_filename):
                    print(f"Loading YOLOv8 PPE model from {model_filename}")
                    model = YOLO(model_filename)
                    
                    # Test if the model loads properly
                    classes = self._get_model_classes(model)
                    print(f"Model classes: {classes}")
                    
                    # Check if it has PPE-related classes
                    ppe_related = any(
                        any(keyword in str(cls).lower() for keyword in ['hardhat', 'vest', 'helmet', 'mask', 'person'])
                        for cls in classes
                    )
                    
                    if ppe_related:
                        print(f"✅ Found PPE-capable model with {len(classes)} classes")
                        return model
                    else:
                        print(f"⚠️  Model doesn't seem to have PPE classes: {classes}")
                        
            except Exception as e:
                print(f"Failed to download/load from {url}: {e}")
                continue
        
        # Fallback to YOLOv8 with a warning
        print("⚠️  Warning: Could not load specialized PPE model, falling back to YOLOv8n")
        print("   Note: YOLOv8n can detect people but not safety equipment")
        return YOLO('yolov8n.pt')
    
    def _get_model_classes(self, model=None) -> List[str]:
        """Get the list of classes the model can detect."""
        if model is None:
            model = self.model
        if hasattr(model, 'names'):
            return list(model.names.values())
        return []
    
    def _get_class_category(self, class_name: str) -> str:
        """Map detected class name to our safety categories."""
        class_name_lower = class_name.lower()
        
        for category, variations in self.ppe_classes.items():
            for variation in variations:
                if variation.lower() in class_name_lower or class_name_lower in variation.lower():
                    return category
        
        return class_name_lower
    
    def detect_safety_violations(self, frame: np.ndarray) -> Dict:
        """
        Detect safety violations in the given frame with improved accuracy.
        
        Returns:
            Dictionary containing detection results and violations
        """
        start_time = time.time()
        
        # Run detection with optimized settings for speed
        results = self.model(frame, conf=0.3, verbose=False, imgsz=640, half=False)
        
        detections = []
        people_count = 0
        safety_equipment_detected = {
            'hardhat': 0,
            'safety_vest': 0,
            'safety_gloves': 0,
            'safety_glasses': 0,
            'hearing_protection': 0,
            'mask': 0
        }
        violations = []
        no_equipment_detections = []  # Track NO- detections separately
        
        # Process detections with stricter filtering
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    # Get detection info
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    
                    # Get class name
                    if hasattr(self.model, 'names'):
                        class_name = self.model.names[class_id]
                    else:
                        class_name = f"class_{class_id}"
                    
                    # Map to our categories
                    category = self._get_class_category(class_name)
                    
                    # Apply stricter confidence thresholds based on equipment type
                    required_confidence = self.equipment_confidence_thresholds.get(category, self.confidence_threshold)
                    
                    # Skip detections that don't meet the stricter threshold
                    if confidence < required_confidence:
                        continue
                    
                    detection = {
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': float(confidence),
                        'class': class_name,
                        'category': category
                    }
                    detections.append(detection)
                    
                    # Count people and safety equipment
                    if category == 'person':
                        people_count += 1
                    elif category in safety_equipment_detected:
                        safety_equipment_detected[category] += 1
                    elif category in ['hardhat', 'safety_vest', 'mask'] and not category.startswith('no_'):
                        safety_equipment_detected[category] += 1
                    
                    # Handle negative detections (NO-Hardhat, NO-Mask, etc.)
                    # These indicate violations - a person without required equipment
                    if category.startswith('no_'):
                        equipment_type = category.replace('no_', '')
                        if equipment_type in ['hardhat', 'safety_vest', 'mask']:
                            no_equipment_detections.append({
                                'type': f'missing_{equipment_type}',
                                'severity': 'high',
                                'description': f'Person detected without {equipment_type.replace("_", " ").title()}',
                                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                'confidence': float(confidence),
                                'equipment_type': equipment_type
                            })
        
        # Create violations based on NO- detections (these are more reliable)
        violations.extend(no_equipment_detections)
        
        # If we have people but no NO- detections, check equipment ratios
        if people_count > 0 and len(no_equipment_detections) == 0:
            required_equipment = ['hardhat', 'safety_vest', 'mask']
            
            for equipment in required_equipment:
                detected_count = safety_equipment_detected[equipment]
                
                # If significantly fewer equipment than people, assume violations
                if detected_count < people_count * 0.8:  # Allow some tolerance
                    missing_count = people_count - detected_count
                    equipment_name = equipment.replace("_", " ").title()
                    violations.append({
                        'type': f'missing_{equipment}',
                        'severity': 'high',
                        'description': f'{missing_count} person(s) likely missing {equipment_name}',
                        'count': missing_count
                    })
        
        # Special handling for masks - they're often not detected well
        mask_detected = safety_equipment_detected['mask']
        no_mask_detected = len([v for v in no_equipment_detections if v['equipment_type'] == 'mask'])
        
        if people_count > 0 and mask_detected == 0 and no_mask_detected == 0:
            # No mask detections at all - assume people are not wearing masks
            violations.append({
                'type': 'missing_mask',
                'severity': 'high',
                'description': f'{people_count} person(s) not wearing Face Mask',
                'count': people_count
            })
        
        processing_time = time.time() - start_time
        
        return {
            'detections': detections,
            'people_count': people_count,
            'safety_equipment': safety_equipment_detected,
            'violations': violations,
            'processing_time': processing_time,
            'fps': 1.0 / processing_time if processing_time > 0 else 0
        }
    
    def draw_detections(self, frame: np.ndarray, results: Dict) -> np.ndarray:
        """
        Draw premium bounding boxes only for POSITIVE equipment detections.
        No boxes for missing equipment - violations shown through person status only.
        
        Args:
            frame: Input frame
            results: Detection results containing detections, violations, etc.
            
        Returns:
            Annotated frame with premium styling
        """
        annotated_frame = frame.copy()
        height, width = annotated_frame.shape[:2]
        
        # Create overlay for semi-transparent effects
        overlay = annotated_frame.copy()
        
        # Premium color scheme
        colors = {
            'person_compliant': (46, 204, 113),      # Emerald green
            'person_violation': (231, 76, 60),       # Red
            'equipment': (52, 152, 219),             # Blue
            'hardhat': (46, 204, 113),               # Green
            'safety_vest': (241, 196, 15),           # Yellow
            'mask': (0, 191, 255),                   # Deep sky blue
            'violation_bg': (231, 76, 60),           # Red background
            'text_bg': (44, 62, 80),                 # Dark blue-gray
            'text_primary': (255, 255, 255),         # White
            'text_secondary': (149, 165, 166),       # Light gray
            'shadow': (0, 0, 0),                     # Black shadow
            'accent': (155, 89, 182),                # Purple accent
        }
        
        # Track people and their compliance status
        people_status = {}
        
        # First pass: categorize people
        for detection in results.get('detections', []):
            class_name = detection['class'].lower()
            bbox = detection['bbox']
            confidence = detection['confidence']
            
            if 'person' in class_name:
                person_id = f"person_{bbox[0]}_{bbox[1]}"
                people_status[person_id] = {
                    'bbox': bbox,
                    'confidence': confidence,
                    'violations': [],
                    'equipment': []
                }
        
        # Map violations to people
        for violation in results.get('violations', []):
            if 'bbox' in violation:
                # This is a specific violation with a bounding box (from NO- detections)
                violation_bbox = violation['bbox']
                # Find the closest person to this violation
                closest_person = None
                min_distance = float('inf')
                
                for person_id, person_data in people_status.items():
                    person_bbox = person_data['bbox']
                    # Calculate distance between violation and person
                    distance = abs(violation_bbox[0] - person_bbox[0]) + abs(violation_bbox[1] - person_bbox[1])
                    if distance < min_distance:
                        min_distance = distance
                        closest_person = person_id
                
                if closest_person and min_distance < 100:  # Within reasonable distance
                    violation_type = violation['type'].replace('missing_', '')
                    people_status[closest_person]['violations'].append(violation_type)
            else:
                # General violation - apply to all people (when equipment count < people count)
                violation_type = violation['type'].replace('missing_', '')
                for person_id in people_status:
                    people_status[person_id]['violations'].append(violation_type)
        
        # If no specific violations detected but people are present, assume they're missing all required equipment
        if len(people_status) > 0 and len(results.get('violations', [])) == 0:
            # Check if we have any positive equipment detections
            equipment_detected = any(
                detection['category'] in ['hardhat', 'safety_vest', 'mask'] 
                for detection in results.get('detections', [])
                if detection['category'] in ['hardhat', 'safety_vest', 'mask']
            )
            
            # If no equipment detected at all, mark all people as having violations
            if not equipment_detected:
                for person_id in people_status:
                    people_status[person_id]['violations'] = ['hardhat', 'safety_vest', 'mask']
        
        # ONLY draw POSITIVE equipment detections (when equipment IS being worn)
        for detection in results.get('detections', []):
            class_name = detection['class'].lower()
            category = detection.get('category', '')
            
            # Skip people and NO- detections - we only want positive equipment
            if 'person' in class_name or 'no-' in class_name or 'no_' in category:
                continue
            
            # Only draw positive equipment detections
            if category in ['hardhat', 'safety_vest', 'mask'] or any(equip in class_name for equip in ['hardhat', 'vest', 'helmet', 'safety', 'mask']):
                bbox = detection['bbox']
                confidence = detection['confidence']
                
                # Choose color and label based on equipment type
                if any(x in class_name for x in ['hardhat', 'helmet']) or category == 'hardhat':
                    color = colors['hardhat']
                    equipment_type = "Hard Hat ✓"
                elif 'vest' in class_name or category == 'safety_vest':
                    color = colors['safety_vest']
                    equipment_type = "Safety Vest ✓"
                elif 'mask' in class_name or category == 'mask':
                    color = colors['mask']
                    equipment_type = "Face Mask ✓"
                else:
                    color = colors['equipment']
                    equipment_type = "Safety Equipment ✓"
                
                # Draw equipment with premium styling
                self._draw_premium_bbox(overlay, annotated_frame, bbox, color, 
                                      equipment_type, confidence, 
                                      bbox_type="equipment", colors=colors)
        
        # Draw people with compliance status (no violation indicators on person boxes)
        for person_id, person_data in people_status.items():
            bbox = person_data['bbox']
            confidence = person_data['confidence']
            violations = person_data['violations']
            
            # Determine person status
            is_compliant = len(violations) == 0
            color = colors['person_compliant'] if is_compliant else colors['person_violation']
            status_text = "COMPLIANT" if is_compliant else "VIOLATION"
            
            # Draw person with premium styling (no violation details on the box)
            self._draw_premium_bbox(overlay, annotated_frame, bbox, color,
                                  f"Person - {status_text}", confidence,
                                  bbox_type="person", violations=None,  # Don't show violation details on person box
                                  colors=colors)
        
        # Blend overlay with original frame for semi-transparent effects
        alpha = 0.15
        cv2.addWeighted(overlay, alpha, annotated_frame, 1 - alpha, 0, annotated_frame)
        
        # Statistics are now handled by the web UI, no overlay needed on video feed
        
        return annotated_frame
    
    def _draw_premium_bbox(self, overlay, frame, bbox, color, label, confidence, 
                          bbox_type="default", violations=None, colors=None):
        """Draw a premium-styled bounding box with advanced visual effects."""
        x1, y1, x2, y2 = map(int, bbox)
        
        # Box dimensions
        box_width = x2 - x1
        box_height = y2 - y1
        
        # Draw shadow first (slightly offset)
        shadow_offset = 3
        shadow_color = colors['shadow']
        cv2.rectangle(overlay, 
                     (x1 + shadow_offset, y1 + shadow_offset), 
                     (x2 + shadow_offset, y2 + shadow_offset), 
                     shadow_color, 2)
        
        # Main bounding box with thinner lines
        box_thickness = 2 if bbox_type == "person" else 1
        
        # Draw main rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, box_thickness)
        
        # Draw corner accents for premium look
        corner_length = min(20, box_width // 4, box_height // 4)
        accent_thickness = box_thickness
        
        # Top-left corner
        cv2.line(frame, (x1, y1), (x1 + corner_length, y1), color, accent_thickness)
        cv2.line(frame, (x1, y1), (x1, y1 + corner_length), color, accent_thickness)
        
        # Top-right corner
        cv2.line(frame, (x2, y1), (x2 - corner_length, y1), color, accent_thickness)
        cv2.line(frame, (x2, y1), (x2, y1 + corner_length), color, accent_thickness)
        
        # Bottom-left corner
        cv2.line(frame, (x1, y2), (x1 + corner_length, y2), color, accent_thickness)
        cv2.line(frame, (x1, y2), (x1, y2 - corner_length), color, accent_thickness)
        
        # Bottom-right corner
        cv2.line(frame, (x2, y2), (x2 - corner_length, y2), color, accent_thickness)
        cv2.line(frame, (x2, y2), (x2, y2 - corner_length), color, accent_thickness)
        
        # Prepare label text
        confidence_text = f"{confidence:.1%}"
        main_text = f"{label}"
        
        # Calculate text dimensions
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        
        (main_w, main_h), _ = cv2.getTextSize(main_text, font, font_scale, thickness)
        (conf_w, conf_h), _ = cv2.getTextSize(confidence_text, font, font_scale - 0.1, thickness - 1)
        
        # Label background dimensions
        label_height = max(main_h, conf_h) + 12
        label_width = max(main_w, conf_w) + 16
        
        # Position label (above box if space available, otherwise below)
        if y1 - label_height - 5 > 0:
            label_y = y1 - label_height - 5
        else:
            label_y = y2 + 5
        
        label_x = x1
        
        # Ensure label stays within frame
        if label_x + label_width > frame.shape[1]:
            label_x = frame.shape[1] - label_width - 5
        if label_x < 0:
            label_x = 5
        
        # Draw label background with gradient effect
        bg_color = colors['text_bg']
        
        # Main background
        cv2.rectangle(overlay, 
                     (label_x, label_y), 
                     (label_x + label_width, label_y + label_height), 
                     bg_color, -1)
        
        # Colored top border
        cv2.rectangle(frame, 
                     (label_x, label_y), 
                     (label_x + label_width, label_y + 4), 
                     color, -1)
        
        # Add subtle border
        cv2.rectangle(frame, 
                     (label_x, label_y), 
                     (label_x + label_width, label_y + label_height), 
                     color, 1)
        
        # Draw main text
        text_y = label_y + main_h + 6
        cv2.putText(frame, main_text, 
                   (label_x + 8, text_y), 
                   font, font_scale, colors['text_primary'], thickness)
        
        # Draw confidence text
        conf_y = text_y + conf_h + 4
        cv2.putText(frame, confidence_text, 
                   (label_x + 8, conf_y), 
                   font, font_scale - 0.1, colors['text_secondary'], max(1, thickness - 1))
        
        # Draw violation indicators for people (only if violations are provided)
        if bbox_type == "person" and violations is not None and len(violations) > 0:
            self._draw_violation_indicators(frame, overlay, x1, y1, x2, y2, violations, colors)
    
    def _draw_violation_indicators(self, frame, overlay, x1, y1, x2, y2, violations, colors):
        """Draw violation indicators with premium styling."""
        # Warning icon position (top-right of bounding box)
        icon_size = 24
        icon_x = x2 - icon_size - 5
        icon_y = y1 + 5
        
        # Draw warning background circle
        cv2.circle(overlay, (icon_x + icon_size//2, icon_y + icon_size//2), 
                  icon_size//2, colors['violation_bg'], -1)
        cv2.circle(frame, (icon_x + icon_size//2, icon_y + icon_size//2), 
                  icon_size//2, colors['violation_bg'], 2)
        
        # Draw exclamation mark
        center_x = icon_x + icon_size//2
        center_y = icon_y + icon_size//2
        
        # Exclamation line
        cv2.line(frame, (center_x, center_y - 6), (center_x, center_y + 2), 
                colors['text_primary'], 2)
        # Exclamation dot
        cv2.circle(frame, (center_x, center_y + 5), 1, colors['text_primary'], -1)
        
        # Draw violation list below the person if space allows
        violation_text = "Missing: " + ", ".join(violations)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        
        (text_w, text_h), _ = cv2.getTextSize(violation_text, font, font_scale, thickness)
        
        # Position violation text
        viol_x = x1
        viol_y = y2 + text_h + 8
        
        # Ensure text stays within frame
        if viol_y + text_h > frame.shape[0]:
            viol_y = y1 - text_h - 8
        if viol_x + text_w > frame.shape[1]:
            viol_x = frame.shape[1] - text_w - 5
        
        # Draw violation text background
        padding = 4
        cv2.rectangle(overlay, 
                     (viol_x - padding, viol_y - text_h - padding), 
                     (viol_x + text_w + padding, viol_y + padding), 
                     colors['violation_bg'], -1)
        
        # Draw violation text
        cv2.putText(frame, violation_text, 
                   (viol_x, viol_y), 
                   font, font_scale, colors['text_primary'], thickness)
    
    def _draw_statistics_overlay(self, frame, results, colors, width, height):
        """Draw statistics overlay with premium styling."""
        # Statistics data
        people_count = results.get('people_count', 0)
        violations = results.get('violations', [])
        violation_count = len(violations)
        compliant_count = people_count - violation_count
        compliance_rate = (compliant_count / max(people_count, 1)) * 100
        
        # Statistics text
        stats = [
            f"People: {people_count}",
            f"Compliant: {compliant_count}",
            f"Violations: {violation_count}",
            f"Compliance: {compliance_rate:.1f}%"
        ]
        
        # Text properties
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        
        # Calculate background size
        max_text_width = 0
        total_height = 0
        line_heights = []
        
        for text in stats:
            (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
            max_text_width = max(max_text_width, text_w)
            line_heights.append(text_h)
            total_height += text_h + 8
        
        # Background dimensions
        bg_width = max_text_width + 24
        bg_height = total_height + 16
        
        # Position (top-left corner)
        bg_x = 20
        bg_y = 20
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, 
                     (bg_x, bg_y), 
                     (bg_x + bg_width, bg_y + bg_height), 
                     colors['text_bg'], -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Draw border
        cv2.rectangle(frame, 
                     (bg_x, bg_y), 
                     (bg_x + bg_width, bg_y + bg_height), 
                     colors['accent'], 2)
        
        # Draw statistics text
        current_y = bg_y + 24
        for i, text in enumerate(stats):
            # Choose color based on statistic type
            if "Violations:" in text and violation_count > 0:
                text_color = colors['person_violation']
            elif "Compliant:" in text:
                text_color = colors['person_compliant']
            elif "Compliance:" in text:
                if compliance_rate >= 80:
                    text_color = colors['person_compliant']
                elif compliance_rate >= 60:
                    text_color = colors['safety_vest']
                else:
                    text_color = colors['person_violation']
            else:
                text_color = colors['text_primary']
            
            cv2.putText(frame, text, 
                       (bg_x + 12, current_y), 
                       font, font_scale, text_color, thickness)
            current_y += line_heights[i] + 8
    
    def get_model_classes(self) -> List[str]:
        """Get the list of classes the model can detect."""
        return self._get_model_classes()
    
    def test_detection(self, test_image_path: str = None):
        """Test the detector with a sample image or webcam."""
        if test_image_path and os.path.exists(test_image_path):
            frame = cv2.imread(test_image_path)
            if frame is not None:
                results = self.detect_safety_violations(frame)
                output = self.draw_detections(frame, results)
                
                print(f"Detected classes: {[d['class'] for d in results['detections']]}")
                print(f"Available model classes: {self.get_model_classes()}")
                
                cv2.imshow('PPE Detection Test', output)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                return results
        else:
            print("Testing with webcam - press 'q' to quit")
            cap = cv2.VideoCapture(0)
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                results = self.detect_safety_violations(frame)
                output = self.draw_detections(frame, results)
                
                cv2.imshow('PPE Detection Test', output)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()

    def analyze_safety_compliance(self, detections: List[Dict]) -> Dict:
        """
        Analyze safety compliance based on detected objects.
        
        Args:
            detections: List of detected objects
            
        Returns:
            Dictionary with compliance analysis
        """
        people_detected = []
        safety_equipment = []
        
        # Separate people and safety equipment
        for detection in detections:
            if detection['class'].lower() == 'person':
                people_detected.append(detection)
            elif any(equipment in detection['class'].lower() 
                    for equipment in ['helmet', 'hardhat', 'vest', 'gloves', 'glasses']):
                safety_equipment.append(detection)
        
        # Analyze compliance for each person
        compliance_results = []
        for person in people_detected:
            person_bbox = person['bbox']
            
            # Check for nearby safety equipment
            nearby_equipment = self._find_nearby_equipment(person_bbox, safety_equipment)
            
            # Determine missing equipment
            required_equipment = ['hardhat', 'safety_vest']
            missing_equipment = []
            
            for equipment in required_equipment:
                if not any(equipment.lower() in item['class'].lower() 
                          for item in nearby_equipment):
                    missing_equipment.append(equipment)
            
            compliance_results.append({
                'person': person,
                'nearby_equipment': nearby_equipment,
                'missing_equipment': missing_equipment,
                'is_compliant': len(missing_equipment) == 0,
                'compliance_score': 1.0 - (len(missing_equipment) / len(required_equipment))
            })
        
        return {
            'total_people': len(people_detected),
            'compliant_people': sum(1 for result in compliance_results if result['is_compliant']),
            'violations': sum(len(result['missing_equipment']) for result in compliance_results),
            'compliance_results': compliance_results,
            'overall_compliance_rate': (
                sum(result['compliance_score'] for result in compliance_results) / 
                max(len(compliance_results), 1)
            )
        }
    
    def _find_nearby_equipment(self, person_bbox: List[int], equipment_list: List[Dict], 
                               proximity_threshold: float = 0.3) -> List[Dict]:
        """Find safety equipment near a person."""
        nearby_equipment = []
        
        person_center_x = (person_bbox[0] + person_bbox[2]) / 2
        person_center_y = (person_bbox[1] + person_bbox[3]) / 2
        
        for equipment in equipment_list:
            equip_bbox = equipment['bbox']
            equip_center_x = (equip_bbox[0] + equip_bbox[2]) / 2
            equip_center_y = (equip_bbox[1] + equip_bbox[3]) / 2
            
            # Calculate normalized distance
            distance = np.sqrt((person_center_x - equip_center_x)**2 + 
                             (person_center_y - equip_center_y)**2)
            
            # Normalize by image diagonal (assuming standard frame size)
            normalized_distance = distance / 1000  # Adjust based on typical frame size
            
            if normalized_distance < proximity_threshold:
                nearby_equipment.append(equipment)
        
        return nearby_equipment
    
    def draw_annotations(self, frame: np.ndarray, analysis: Dict) -> np.ndarray:
        """
        Draw bounding boxes and annotations on the frame.
        
        Args:
            frame: Input frame
            analysis: Safety compliance analysis results
            
        Returns:
            Annotated frame
        """
        annotated_frame = frame.copy()
        
        # Draw safety equipment
        for equipment in analysis['safety_equipment']:
            bbox = equipment['bbox']
            cv2.rectangle(annotated_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), 
                         self.colors['equipment'], 2)
            
            label = f"{equipment.get('equipment_type', equipment['class'])}: {equipment['confidence']:.2f}"
            cv2.putText(annotated_frame, label, (bbox[0], bbox[1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['equipment'], 2)
        
        # Draw people with compliance status
        for result in analysis['compliance_results']:
            person = result['person']
            bbox = person['bbox']
            
            # Choose color based on compliance
            color = self.colors['person'] if result['is_compliant'] else self.colors['violation']
            
            # Draw bounding box
            cv2.rectangle(annotated_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 3)
            
            # Create status label
            status = "COMPLIANT" if result['is_compliant'] else "VIOLATION"
            confidence_text = f"Person: {person['confidence']:.2f}"
            
            # Draw labels
            cv2.putText(annotated_frame, status, (bbox[0], bbox[1] - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(annotated_frame, confidence_text, (bbox[0], bbox[1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Show missing equipment
            if result['missing_equipment']:
                missing_text = f"Missing: {', '.join(result['missing_equipment'])}"
                cv2.putText(annotated_frame, missing_text, (bbox[0], bbox[3] + 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['violation'], 2)
        
        # Draw summary statistics
        summary_text = [
            f"Total People: {analysis['total_people']}",
            f"Compliant: {analysis['compliant_people']}",
            f"Violations: {analysis['violations']}",
            f"Compliance Rate: {(analysis['compliant_people']/max(analysis['total_people'],1)*100):.1f}%"
        ]
        
        for i, text in enumerate(summary_text):
            cv2.putText(annotated_frame, text, (10, 30 + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return annotated_frame
    
    def capture_violation(self, frame: np.ndarray, violation_data: Dict) -> str:
        """
        Capture and save an image when a safety violation is detected.
        
        Args:
            frame: Current frame
            violation_data: Information about the violation
            
        Returns:
            Path to saved image
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"violation_{timestamp}.jpg"
        filepath = os.path.join(self.violation_images_dir, filename)
        
        # Save the frame
        cv2.imwrite(filepath, frame)
        
        # Save violation metadata
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'filename': filename,
            'violation_data': violation_data
        }
        
        metadata_file = filepath.replace('.jpg', '_metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.violations.append(metadata)
        return filepath
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Process a single frame for safety monitoring.
        
        Args:
            frame: Input video frame
            
        Returns:
            Tuple of (annotated_frame, analysis_results)
        """
        # Detect objects and get safety violations
        results = self.detect_safety_violations(frame)
        
        # Draw detections on frame using the main drawing method
        annotated_frame = self.draw_detections(frame, results)
        
        return annotated_frame, {
            'detections': results['detections'],
            'people_count': results['people_count'],
            'safety_equipment': results['safety_equipment'],
            'violations': results['violations'],
            'violation_summary': self.get_violation_summary(),
            'frame_stats': {
                'processing_time': results['processing_time'],
                'fps': results['fps'],
                'detection_count': len(results['detections'])
            }
        }
    
    def get_violation_summary(self) -> Dict:
        """Get a summary of recent violations."""
        # This would typically connect to a database or log file
        # For now, return a placeholder
        return {
            'total_violations_today': 0,
            'most_common_violation': 'missing_hardhat',
            'compliance_trend': []  # Could track compliance over time
        }

if __name__ == "__main__":
    # Test the detector
    detector = SafetyDetector()
    print("Available classes:", detector.get_model_classes())
    detector.test_detection() 