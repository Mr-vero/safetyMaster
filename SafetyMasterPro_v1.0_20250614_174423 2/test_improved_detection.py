#!/usr/bin/env python3
"""
Test script for improved SafetyMaster Pro detection with stricter confidence thresholds
"""

import cv2
import numpy as np
from safety_detector import SafetyDetector
import time

def test_improved_detection():
    """Test the improved detection logic with stricter thresholds."""
    print("🧪 Testing SafetyMaster Pro - Improved Detection Logic")
    print("=" * 60)
    
    # Initialize detector
    detector = SafetyDetector()
    
    print(f"\n📊 Confidence Thresholds:")
    for equipment, threshold in detector.equipment_confidence_thresholds.items():
        print(f"   {equipment}: {threshold}")
    
    print(f"\n🎯 Available Model Classes:")
    classes = detector.get_model_classes()
    for i, cls in enumerate(classes):
        print(f"   {i}: {cls}")
    
    # Test with webcam
    print(f"\n📹 Starting webcam test...")
    print("   Press 'q' to quit")
    print("   Press 's' to save current frame")
    print("   Watch for improved accuracy with stricter thresholds")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return
    
    frame_count = 0
    total_processing_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame")
            break
        
        frame_count += 1
        
        # Run detection
        start_time = time.time()
        results = detector.detect_safety_violations(frame)
        processing_time = time.time() - start_time
        total_processing_time += processing_time
        
        # Draw detections
        annotated_frame = detector.draw_detections(frame, results)
        
        # Add performance info
        avg_fps = frame_count / total_processing_time if total_processing_time > 0 else 0
        cv2.putText(annotated_frame, f"Avg FPS: {avg_fps:.1f}", 
                   (10, annotated_frame.shape[0] - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.putText(annotated_frame, f"Frame: {frame_count}", 
                   (10, annotated_frame.shape[0] - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Print detection summary every 30 frames
        if frame_count % 30 == 0:
            print(f"\n📊 Frame {frame_count} Summary:")
            print(f"   People: {results['people_count']}")
            print(f"   Equipment detected: {results['safety_equipment']}")
            print(f"   Violations: {len(results['violations'])}")
            if results['violations']:
                for violation in results['violations']:
                    print(f"     - {violation['description']}")
            print(f"   Processing time: {processing_time:.3f}s")
        
        # Display frame
        cv2.imshow('SafetyMaster Pro - Improved Detection', annotated_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save current frame
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"test_detection_{timestamp}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"💾 Saved frame as {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✅ Test completed!")
    print(f"   Total frames processed: {frame_count}")
    print(f"   Average FPS: {frame_count / total_processing_time:.1f}")

if __name__ == "__main__":
    test_improved_detection() 