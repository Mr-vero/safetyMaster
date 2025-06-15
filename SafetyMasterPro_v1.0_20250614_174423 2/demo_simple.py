#!/usr/bin/env python3
"""
Simple Safety Monitor Demo - Just Person Detection
Tests basic camera and person detection functionality.
"""

import cv2
import time
import sys
from ultralytics import YOLO
import numpy as np

def main():
    print("🔒 Simple Safety Monitor Demo")
    print("============================")
    print("This demo just detects people to test basic functionality")
    print("Controls: SPACE=pause, S=save, Q=quit")
    print("-" * 50)
    
    try:
        # Initialize YOLO model
        print("Loading YOLO model...")
        model = YOLO('yolov8n.pt')
        print("✅ Model loaded")
        
        # Print available classes
        print("📋 Available detection classes:")
        for i, class_name in model.names.items():
            if i < 10:  # Show first 10 classes
                print(f"   {i}: {class_name}")
        print("   ... and more")
        print()
        
        # Initialize camera
        print("🎥 Connecting to camera...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Could not open camera")
            return 1
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("✅ Camera connected")
        print("🔍 Starting detection... Press Q to quit")
        print()
        
        # Stats
        frame_count = 0
        fps_start = time.time()
        people_detected = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            frame_count += 1
            
            # Run detection
            results = model(frame, conf=0.5, verbose=False)
            
            # Process results
            people_count = 0
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get class info
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]
                        confidence = float(box.conf[0])
                        
                        # Only process people
                        if class_name == 'person' and confidence > 0.5:
                            people_count += 1
                            people_detected += 1
                            
                            # Get bounding box
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            
                            # Draw green box for person
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            
                            # Add label
                            label = f"Person: {confidence:.2f}"
                            cv2.putText(frame, label, (x1, y1-10), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Add stats to frame
            stats_text = [
                f"People in frame: {people_count}",
                f"Total detected: {people_detected}",
                f"Press Q to quit, SPACE to pause"
            ]
            
            for i, text in enumerate(stats_text):
                cv2.putText(frame, text, (10, 30 + i * 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Calculate FPS
            if frame_count % 30 == 0:
                fps = 30 / (time.time() - fps_start)
                fps_start = time.time()
                print(f"\r📊 FPS: {fps:.1f} | People: {people_count} | Total: {people_detected}", 
                      end='', flush=True)
            
            # Show frame
            cv2.imshow('Simple Safety Monitor - Person Detection', frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            elif key == ord('s'):
                filename = f"detection_capture_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                print(f"\n📸 Saved: {filename}")
            elif key == ord(' '):
                print("\n⏸️  Paused - press any key to continue")
                cv2.waitKey(0)
                print("▶️  Resumed")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    finally:
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        print(f"\n\n✅ Demo completed!")
        print(f"   Total people detected: {people_detected}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 