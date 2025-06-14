#!/usr/bin/env python3
"""
Test script for PPE detection model
"""

import cv2
import time
from safety_detector import SafetyDetector

def test_ppe_detection():
    """Test the PPE detection system."""
    print("🔍 Testing PPE Detection System")
    print("=" * 50)
    
    # Initialize detector
    print("📦 Initializing PPE detector...")
    detector = SafetyDetector()
    
    # Show available classes
    classes = detector.get_model_classes()
    print(f"🏷️  Available model classes: {classes}")
    print(f"🖥️  Using device: {detector.device}")
    
    # Test with webcam
    print("\n📹 Starting webcam test...")
    print("   Press 'q' to quit, 'c' to capture violation")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return
    
    frame_count = 0
    total_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame")
            break
        
        start_time = time.time()
        
        # Run PPE detection
        results = detector.detect_safety_violations(frame)
        
        # Draw results
        annotated_frame = detector.draw_detections(frame, results)
        
        processing_time = time.time() - start_time
        frame_count += 1
        total_time += processing_time
        
        # Show results in terminal every 30 frames
        if frame_count % 30 == 0:
            avg_fps = frame_count / total_time if total_time > 0 else 0
            print(f"\n📊 Frame {frame_count} Results:")
            print(f"   People detected: {results['people_count']}")
            print(f"   Safety equipment: {results['safety_equipment']}")
            print(f"   Violations: {len(results['violations'])}")
            print(f"   Average FPS: {avg_fps:.1f}")
            
            if results['violations']:
                for violation in results['violations']:
                    print(f"   ⚠️  {violation['description']}")
        
        # Display frame
        cv2.imshow('PPE Detection Test', annotated_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            # Capture current frame
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"ppe_test_capture_{timestamp}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"📸 Captured frame saved as {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Final statistics
    avg_fps = frame_count / total_time if total_time > 0 else 0
    print(f"\n📈 Final Statistics:")
    print(f"   Total frames processed: {frame_count}")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Average FPS: {avg_fps:.1f}")
    print(f"   Average processing time: {(total_time/frame_count)*1000:.1f}ms per frame")

if __name__ == "__main__":
    test_ppe_detection() 