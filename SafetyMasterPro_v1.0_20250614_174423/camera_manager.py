import cv2
import threading
import queue
import time
from typing import Optional, Callable, Union
import numpy as np

class CameraManager:
    """
    Manages video capture from various sources including webcams, IP cameras, and video files.
    Provides threaded video capture for real-time processing.
    """
    
    def __init__(self, source: Union[int, str] = 0, buffer_size: int = 10):
        """
        Initialize camera manager.
        
        Args:
            source: Camera source (0 for default webcam, URL for IP camera, path for video file)
            buffer_size: Size of frame buffer for threading
        """
        self.source = source
        self.buffer_size = buffer_size
        self.cap = None
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        self.capture_thread = None
        self.is_running = False
        self.fps = 60  # Higher FPS target
        self.frame_width = 640
        self.frame_height = 480
        
    def connect(self) -> bool:
        """
        Connect to the video source.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.source)
            
            if not self.cap.isOpened():
                print(f"Error: Could not open video source: {self.source}")
                return False
            
            # Set camera properties for higher performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer to minimize delay
            
            # Additional optimizations for higher FPS
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  # Use MJPEG for speed
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Disable auto exposure for consistent timing
            
            # Get actual properties
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            print(f"Connected to camera: {self.frame_width}x{self.frame_height} @ {self.fps}fps")
            return True
            
        except Exception as e:
            print(f"Error connecting to camera: {e}")
            return False
    
    def start_capture(self) -> bool:
        """
        Start threaded video capture.
        
        Returns:
            True if capture started successfully, False otherwise
        """
        if not self.cap or not self.cap.isOpened():
            if not self.connect():
                return False
        
        if self.is_running:
            print("Capture is already running")
            return True
        
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.capture_thread.start()
        
        print("Video capture started")
        return True
    
    def stop_capture(self):
        """Stop video capture and clean up resources."""
        self.is_running = False
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2.0)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # Clear the frame queue
        while not self.frame_queue.empty():
            try:
                self.frame_queue.get_nowait()
            except queue.Empty:
                break
        
        print("Video capture stopped")
    
    def _capture_frames(self):
        """Internal method to capture frames in a separate thread."""
        while self.is_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Failed to capture frame")
                    if isinstance(self.source, str) and not self.source.isdigit():
                        # For video files, we might have reached the end
                        print("Reached end of video file")
                        break
                    continue
                
                # Add timestamp to frame
                timestamp = time.time()
                
                # If queue is full, remove oldest frame
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except queue.Empty:
                        pass
                
                # Add new frame to queue
                self.frame_queue.put((frame, timestamp), block=False)
                
            except Exception as e:
                print(f"Error in frame capture: {e}")
                time.sleep(0.1)
        
        self.is_running = False
    
    def get_frame(self) -> Optional[tuple]:
        """
        Get the latest frame from the capture queue.
        
        Returns:
            Tuple of (frame, timestamp) or None if no frame available
        """
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_latest_frame(self) -> Optional[tuple]:
        """
        Get the most recent frame, discarding any older frames in the queue.
        
        Returns:
            Tuple of (frame, timestamp) or None if no frame available
        """
        latest_frame = None
        
        # Get all frames and keep only the latest
        while True:
            try:
                frame_data = self.frame_queue.get_nowait()
                latest_frame = frame_data
            except queue.Empty:
                break
        
        return latest_frame
    
    def is_connected(self) -> bool:
        """
        Check if camera is connected and capturing.
        
        Returns:
            True if connected and running, False otherwise
        """
        return self.is_running and self.cap is not None and self.cap.isOpened()
    
    def get_properties(self) -> dict:
        """
        Get camera properties.
        
        Returns:
            Dictionary of camera properties
        """
        if not self.cap:
            return {}
        
        return {
            'width': self.frame_width,
            'height': self.frame_height,
            'fps': self.fps,
            'source': self.source,
            'is_running': self.is_running,
            'buffer_size': self.buffer_size
        }
    
    def set_resolution(self, width: int, height: int) -> bool:
        """
        Set camera resolution.
        
        Args:
            width: Frame width
            height: Frame height
            
        Returns:
            True if successful, False otherwise
        """
        if not self.cap:
            return False
        
        try:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            # Verify the change
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            self.frame_width = actual_width
            self.frame_height = actual_height
            
            print(f"Resolution set to: {actual_width}x{actual_height}")
            return True
            
        except Exception as e:
            print(f"Error setting resolution: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        self.start_capture()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_capture()


class MultiCameraManager:
    """
    Manages multiple camera sources simultaneously.
    """
    
    def __init__(self):
        self.cameras = {}
        self.is_running = False
    
    def add_camera(self, camera_id: str, source: Union[int, str], 
                   buffer_size: int = 10) -> bool:
        """
        Add a camera to the manager.
        
        Args:
            camera_id: Unique identifier for the camera
            source: Camera source
            buffer_size: Frame buffer size
            
        Returns:
            True if camera added successfully, False otherwise
        """
        try:
            camera = CameraManager(source, buffer_size)
            if camera.connect():
                self.cameras[camera_id] = camera
                print(f"Camera '{camera_id}' added successfully")
                return True
            else:
                print(f"Failed to add camera '{camera_id}'")
                return False
        except Exception as e:
            print(f"Error adding camera '{camera_id}': {e}")
            return False
    
    def remove_camera(self, camera_id: str):
        """Remove a camera from the manager."""
        if camera_id in self.cameras:
            self.cameras[camera_id].stop_capture()
            del self.cameras[camera_id]
            print(f"Camera '{camera_id}' removed")
    
    def start_all(self):
        """Start capture for all cameras."""
        for camera_id, camera in self.cameras.items():
            if camera.start_capture():
                print(f"Started capture for camera '{camera_id}'")
            else:
                print(f"Failed to start capture for camera '{camera_id}'")
        self.is_running = True
    
    def stop_all(self):
        """Stop capture for all cameras."""
        for camera_id, camera in self.cameras.items():
            camera.stop_capture()
            print(f"Stopped capture for camera '{camera_id}'")
        self.is_running = False
    
    def get_frame(self, camera_id: str) -> Optional[tuple]:
        """Get frame from specific camera."""
        if camera_id in self.cameras:
            return self.cameras[camera_id].get_frame()
        return None
    
    def get_all_frames(self) -> dict:
        """Get frames from all cameras."""
        frames = {}
        for camera_id, camera in self.cameras.items():
            frame_data = camera.get_latest_frame()
            if frame_data:
                frames[camera_id] = frame_data
        return frames
    
    def get_camera_list(self) -> list:
        """Get list of all camera IDs."""
        return list(self.cameras.keys()) 