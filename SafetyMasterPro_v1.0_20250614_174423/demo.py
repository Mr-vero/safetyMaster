#!/usr/bin/env python3
"""
Safety Monitor Demo Script
Real-time safety compliance detection using webcam or video file.
"""

import cv2
import argparse
import time
import sys
from safety_detector import SafetyDetector
from camera_manager import CameraManager

def main():
    parser = argparse.ArgumentParser(description='Safety Monitor Demo')
    parser.add_argument('--source', type=str, default='0', 
                       help='Video source (0 for webcam, path for video file, URL for IP camera)')
    parser.add_argument('--model', type=str, default=None,
                       help='Path to custom YOLO model (optional)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Detection confidence threshold (0.1-1.0)')
    parser.add_argument('--save-violations', action='store_true',
                       help='Save violation images to disk')
    parser.add_argument('--fullscreen', action='store_true',
                       help='Display in fullscreen mode')
    
    args = parser.parse_args()
    
    # Convert source to int if it's a digit (for webcam)
    source = int(args.source) if args.source.isdigit() else args.source
    
    print("🔒 Safety Monitor Demo Starting...")
    print(f"📹 Video Source: {source}")
    print(f"🎯 Confidence Threshold: {args.confidence}")
    print(f"🤖 Model: {'Custom' if args.model else 'YOLOv8 (default)'}")
    print("\nControls:")
    print("  SPACE - Pause/Resume")
    print("  S     - Save current frame")
    print("  Q/ESC - Quit")
    print("-" * 50)
    
    try:
        # Initialize safety detector
        print("Loading safety detection model...")
        detector = SafetyDetector(args.model, args.confidence)
        print("✅ Safety detector initialized")
        
        # Initialize camera
        print("Connecting to camera...")
        camera = CameraManager(source)
        
        if not camera.start_capture():
            print("❌ Failed to start camera capture")
            return 1
        
        print("✅ Camera connected and capturing")
        print("\n🔍 Starting real-time safety monitoring...\n")
        
        # Stats tracking
        frame_count = 0
        fps_start_time = time.time()
        total_violations = 0
        paused = False
        
        while True:
            if not paused:
                # Get latest frame
                frame_data = camera.get_latest_frame()
                if frame_data is None:
                    time.sleep(0.01)
                    continue
                
                frame, timestamp = frame_data
                frame_count += 1
                
                # Process frame for safety detection
                annotated_frame, analysis = detector.process_frame(frame)
                
                # Update stats
                total_violations += analysis['violations']
                
                # Calculate FPS
                current_time = time.time()
                if current_time - fps_start_time >= 1.0:
                    fps = frame_count / (current_time - fps_start_time)
                    frame_count = 0
                    fps_start_time = current_time
                    
                    # Print stats
                    print(f"\r📊 FPS: {fps:.1f} | People: {analysis['total_people']} | "
                          f"Compliant: {analysis['compliant_people']} | "
                          f"Violations: {analysis['violations']} | "
                          f"Total Violations: {total_violations}", end='', flush=True)
                
                # Display frame
                display_frame = annotated_frame
            else:
                # Use last frame when paused
                if 'display_frame' not in locals():
                    continue
                
                # Add pause indicator
                pause_frame = display_frame.copy()
                cv2.putText(pause_frame, "PAUSED - Press SPACE to resume", 
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                display_frame = pause_frame
            
            # Show the frame
            if args.fullscreen:
                cv2.namedWindow('Safety Monitor', cv2.WINDOW_NORMAL)
                cv2.setWindowProperty('Safety Monitor', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            
            cv2.imshow('Safety Monitor', display_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == 27:  # Q or ESC
                break
            elif key == ord(' '):  # SPACE
                paused = not paused
                if paused:
                    print("\n⏸️  PAUSED")
                else:
                    print("\n▶️  RESUMED")
            elif key == ord('s'):  # S
                timestamp_str = time.strftime("%Y%m%d_%H%M%S")
                filename = f"safety_monitor_capture_{timestamp_str}.jpg"
                cv2.imwrite(filename, display_frame)
                print(f"\n📸 Frame saved as {filename}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    finally:
        # Cleanup
        if 'camera' in locals():
            camera.stop_capture()
        cv2.destroyAllWindows()
        
        # Final stats
        print(f"\n\n📈 Final Statistics:")
        print(f"   Total Violations Detected: {total_violations}")
        if 'detector' in locals():
            violation_summary = detector.get_violation_summary()
            print(f"   Violations Saved: {violation_summary['total_violations']}")
        print("   Thank you for using Safety Monitor! 🔒")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())