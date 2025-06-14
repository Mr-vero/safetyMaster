#!/usr/bin/env python3
"""
Test script for mask detection and violation logic
"""

from safety_detector import SafetyDetector
import cv2
import numpy as np

def test_violation_logic():
    """Test the violation detection logic."""
    print("🧪 Testing SafetyMaster Pro Mask Detection & Violation Logic")
    print("=" * 60)
    
    # Initialize detector
    detector = SafetyDetector()
    
    # Test 1: Empty frame (no people, no equipment)
    print("\n📋 Test 1: Empty frame")
    empty_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    results = detector.detect_safety_violations(empty_frame)
    print(f"   People: {results['people_count']}")
    print(f"   Violations: {len(results['violations'])}")
    print(f"   Expected: 0 people, 0 violations ✅")
    
    # Test 2: Check model classes
    print("\n📋 Test 2: Model Classes")
    classes = detector.get_model_classes()
    mask_classes = [cls for cls in classes if 'mask' in cls.lower()]
    print(f"   Total classes: {len(classes)}")
    print(f"   Mask-related classes: {mask_classes}")
    print(f"   Expected: ['Mask', 'NO-Mask'] ✅")
    
    # Test 3: Check PPE class mappings
    print("\n📋 Test 3: PPE Class Mappings")
    for category, variations in detector.ppe_classes.items():
        if 'mask' in category:
            print(f"   {category}: {variations}")
    
    # Test 4: Test with webcam (if available)
    print("\n📋 Test 4: Live Camera Test")
    print("   Starting webcam test - press 'q' to quit")
    print("   Look for:")
    print("   - Blue boxes around masks")
    print("   - Red boxes around people without PPE")
    print("   - Violation indicators on non-compliant people")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("   ❌ Could not open webcam")
        return
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame
        results = detector.detect_safety_violations(frame)
        annotated_frame = detector.draw_detections(frame, results)
        
        # Add test info overlay
        cv2.putText(annotated_frame, "SafetyMaster Pro - Mask Detection Test", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(annotated_frame, "Press 'q' to quit", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show detection info every 30 frames
        if frame_count % 30 == 0:
            print(f"\n   Frame {frame_count}:")
            print(f"   - People detected: {results['people_count']}")
            print(f"   - Violations: {len(results['violations'])}")
            print(f"   - Equipment: {results['safety_equipment']}")
            
            if results['violations']:
                for violation in results['violations']:
                    print(f"     ⚠️  {violation['description']}")
        
        cv2.imshow('Mask Detection Test', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n✅ Test completed!")
    print("\nExpected behavior:")
    print("- People without masks should show 'VIOLATION' status")
    print("- People with masks should show 'COMPLIANT' status")
    print("- Masks should be detected with blue bounding boxes")
    print("- Violation alerts should appear for missing PPE")

if __name__ == "__main__":
    test_violation_logic() 