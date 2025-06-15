#!/usr/bin/env python3
"""
High FPS test for SafetyMaster Pro
Tests the optimized detection pipeline for maximum performance
"""

import cv2
import time
from safety_detector import SafetyDetector
from camera_manager import CameraManager

def test_high_fps():
    """Test the system at high FPS."""
    print("🚀 SafetyMaster Pro - High FPS Performance Test")
    print("=" * 50)
    
    # Initialize components
    detector = SafetyDetector()
    camera_manager = CameraManager(source=0)
    
    if not camera_manager.start_capture():
        print("❌ Failed to start camera")
        return
    
    print(f"📹 Camera started: {camera_manager.get_properties()}")
    print("🎯 Testing high FPS performance...")
    print("   Press 'q' to quit, 's' to save frame")
    
    frame_count = 0
    detection_count = 0
    start_time = time.time()
    last_detection_results = None
    
    try:
        while True:
            frame_data = camera_manager.get_latest_frame()
            if frame_data is not None:
                frame, timestamp = frame_data
                frame_count += 1
                
                # Run detection every 3rd frame for optimal performance
                if frame_count % 3 == 0 or last_detection_results is None:
                    detection_start = time.time()
                    results = detector.detect_safety_violations(frame)
                    detection_time = time.time() - detection_start
                    last_detection_results = results
                    detection_count += 1
                else:
                    # Use cached results for intermediate frames
                    results = last_detection_results
                    detection_time = 0
                
                # Draw detections
                annotated_frame = detector.draw_detections(frame, results)
                
                # Calculate and display FPS
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    video_fps = frame_count / elapsed_time
                    detection_fps = detection_count / elapsed_time
                    
                    # Add FPS info to frame
                    cv2.putText(annotated_frame, f"Video FPS: {video_fps:.1f}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(annotated_frame, f"AI FPS: {detection_fps:.1f}", 
                               (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    cv2.putText(annotated_frame, f"Detection Time: {detection_time*1000:.1f}ms", 
                               (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                # Display frame
                cv2.imshow('SafetyMaster Pro - High FPS Test', annotated_frame)
                
                # Print stats every 60 frames
                if frame_count % 60 == 0:
                    print(f"📊 Frame {frame_count}: Video FPS: {video_fps:.1f}, AI FPS: {detection_fps:.1f}")
                    if results['violations']:
                        print(f"   ⚠️  {len(results['violations'])} violations detected")
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save frame
                    filename = f"high_fps_test_{int(time.time())}.jpg"
                    cv2.imwrite(filename, annotated_frame)
                    print(f"💾 Saved {filename}")
            
            else:
                time.sleep(0.001)  # Minimal delay when no frame available
                
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    
    finally:
        camera_manager.stop_capture()
        cv2.destroyAllWindows()
        
        # Final statistics
        total_time = time.time() - start_time
        print(f"\n📈 Final Performance Statistics:")
        print(f"   Total frames: {frame_count}")
        print(f"   Total detections: {detection_count}")
        print(f"   Test duration: {total_time:.1f}s")
        print(f"   Average video FPS: {frame_count / total_time:.1f}")
        print(f"   Average AI FPS: {detection_count / total_time:.1f}")
        print(f"   Frame skip ratio: {(frame_count - detection_count) / frame_count * 100:.1f}%")

if __name__ == "__main__":
    test_high_fps() 