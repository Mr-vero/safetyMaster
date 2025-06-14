#!/usr/bin/env python3
"""
Test camera access directly
"""

import cv2
import time

def test_camera():
    print("🔍 Testing camera access...")
    
    # Try to open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        print("   Possible causes:")
        print("   - Camera is being used by another application")
        print("   - Camera permissions not granted")
        print("   - No camera available")
        return False
    
    print("✅ Camera opened successfully")
    
    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    
    # Try to read a frame
    ret, frame = cap.read()
    
    if not ret:
        print("❌ Error: Could not read frame from camera")
        cap.release()
        return False
    
    print("✅ Successfully read frame from camera")
    print(f"   Frame shape: {frame.shape}")
    
    # Test reading a few frames
    frames_read = 0
    start_time = time.time()
    
    for i in range(10):
        ret, frame = cap.read()
        if ret:
            frames_read += 1
        time.sleep(0.1)
    
    elapsed = time.time() - start_time
    actual_fps = frames_read / elapsed
    
    print(f"   Read {frames_read}/10 frames successfully")
    print(f"   Actual FPS: {actual_fps:.1f}")
    
    cap.release()
    
    if frames_read >= 8:  # Allow for some dropped frames
        print("✅ Camera test PASSED")
        return True
    else:
        print("❌ Camera test FAILED - too many dropped frames")
        return False

if __name__ == "__main__":
    test_camera() 