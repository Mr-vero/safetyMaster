#!/usr/bin/env python3
"""
Advanced Safety Monitor Web Interface
Real-time safety equipment detection with web dashboard
"""

import cv2
import base64
import json
import time
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
from datetime import datetime
import os

from safety_detector import SafetyDetector
from camera_manager import CameraManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'safety_monitor_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables
detector = None
camera_manager = None
monitoring_active = False
violation_log = []

def initialize_components():
    """Initialize the safety detector and camera manager."""
    global detector
    try:
        detector = SafetyDetector()
        print("Safety detector initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing components: {e}")
        return False

def process_video_stream():
    """Process video stream and emit results to connected clients."""
    global monitoring_active, violation_log
    
    frame_count = 0
    last_detection_results = None
    
    while monitoring_active:
        try:
            if camera_manager and camera_manager.is_connected():
                frame_data = camera_manager.get_latest_frame()
                if frame_data is not None:
                    frame, timestamp = frame_data
                    frame_count += 1
                    
                    # Run AI detection every 3rd frame for higher FPS (20 FPS AI, 60 FPS video)
                    if frame_count % 3 == 0 or last_detection_results is None:
                        # Get safety detection results
                        results = detector.detect_safety_violations(frame)
                        last_detection_results = results
                    else:
                        # Use previous detection results for intermediate frames
                        results = last_detection_results
                    
                    # Draw detections on frame
                    annotated_frame = detector.draw_detections(frame, results)
                    
                    # Convert frame to base64 for web transmission (optimized for speed)
                    _, buffer = cv2.imencode('.jpg', annotated_frame, 
                                           [cv2.IMWRITE_JPEG_QUALITY, 75])  # Reduced quality for speed
                    frame_base64 = base64.b64encode(buffer).decode('utf-8')
                    
                    # Log violations (optimized - only log new violations)
                    if results['violations']:
                        current_time = datetime.now().isoformat()
                        for violation in results['violations']:
                            violation_entry = {
                                'timestamp': current_time,
                                'type': violation['type'],
                                'description': violation['description'],
                                'severity': violation['severity'],
                                'count': violation.get('count', 1)
                            }
                            violation_log.append(violation_entry)
                            
                            # Keep only last 50 violations (reduced for performance)
                            if len(violation_log) > 50:
                                violation_log.pop(0)
                    
                    # Prepare data for web client
                    stream_data = {
                        'frame': frame_base64,
                        'people_count': results['people_count'],
                        'safety_equipment': results['safety_equipment'],
                        'violations': results['violations'],
                        'fps': results['fps'],
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Emit to all connected clients
                    socketio.emit('video_frame', stream_data)
                    
                    # Reduced delay for higher FPS
                    time.sleep(0.033)  # ~30 FPS target
            else:
                time.sleep(0.5)  # Wait if camera is not active
                
        except Exception as e:
            print(f"Error in video processing: {e}")
            time.sleep(1)

@app.route('/')
def dashboard():
    """Serve the main dashboard."""
    return render_template('dashboard.html')

@app.route('/test')
def test_page():
    """Serve the WebSocket test page."""
    return open('test_websocket.html').read()

@app.route('/api/start_monitoring', methods=['POST'])
def start_monitoring():
    """Start the safety monitoring."""
    global monitoring_active, camera_manager
    
    try:
        data = request.get_json() or {}
        camera_source = data.get('camera_source', 0)  # Default to webcam
        
        # Initialize camera
        camera_manager = CameraManager(source=camera_source)
        
        if camera_manager.start_capture():
            monitoring_active = True
            
            # Start video processing thread
            video_thread = threading.Thread(target=process_video_stream, daemon=True)
            video_thread.start()
            
            return jsonify({
                'success': True,
                'message': 'Monitoring started successfully',
                'camera_info': camera_manager.get_properties()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to start camera'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting monitoring: {str(e)}'
        }), 500

@app.route('/api/stop_monitoring', methods=['POST'])
def stop_monitoring():
    """Stop the safety monitoring."""
    global monitoring_active, camera_manager
    
    try:
        monitoring_active = False
        
        if camera_manager:
            camera_manager.stop_capture()
        
        return jsonify({
            'success': True,
            'message': 'Monitoring stopped successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error stopping monitoring: {str(e)}'
        }), 500

@app.route('/api/violations')
def get_violations():
    """Get recent violations."""
    try:
        return jsonify({
            'success': True,
            'violations': violation_log[-20:],  # Last 20 violations
            'total_count': len(violation_log)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting violations: {str(e)}'
        }), 500

@app.route('/api/model_info')
def get_model_info():
    """Get information about the loaded model."""
    try:
        if detector:
            return jsonify({
                'success': True,
                'model_classes': detector.get_model_classes(),
                'device': detector.device
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Detector not initialized'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting model info: {str(e)}'
        }), 500

@app.route('/api/capture_violation', methods=['POST'])
def capture_violation():
    """Manually capture and save a violation image."""
    try:
        if camera_manager and camera_manager.is_connected():
            frame_data = camera_manager.get_latest_frame()
            if frame_data is not None:
                frame, timestamp = frame_data
                
                # Get detection results
                results = detector.detect_safety_violations(frame)
                annotated_frame = detector.draw_detections(frame, results)
                
                # Save image with timestamp
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"violation_capture_{timestamp_str}.jpg"
                filepath = os.path.join("captures", filename)
                
                # Create captures directory if it doesn't exist
                os.makedirs("captures", exist_ok=True)
                
                cv2.imwrite(filepath, annotated_frame)
                
                return jsonify({
                    'success': True,
                    'message': f'Violation captured and saved as {filename}',
                    'filepath': filepath,
                    'detections': results['detections'],
                    'violations': results['violations']
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No frame available from camera'
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': 'Camera not active'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error capturing violation: {str(e)}'
        }), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('status', {'message': 'Connected to Safety Monitor'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')

@socketio.on('request_model_info')
def handle_model_info_request():
    """Send model information to client."""
    try:
        if detector:
            model_info = {
                'classes': detector.get_model_classes(),
                'device': detector.device
            }
            emit('model_info', model_info)
        else:
            emit('error', {'message': 'Detector not initialized'})
    except Exception as e:
        emit('error', {'message': f'Error getting model info: {str(e)}'})

def main():
    """Main function to run the web application."""
    print("🤖 Loading AI model (this may take a moment on first run)...")
    print("   Downloading PPE detection model if not already cached...")
    
    if not initialize_components():
        print("❌ Failed to initialize components")
        return
    
    print("🚀 Starting Safety Monitor Web Application...")
    print("   Access dashboard at: http://localhost:8080")
    print("   Press Ctrl+C to stop")
    
    try:
        socketio.run(app, 
                    host='0.0.0.0', 
                    port=8080, 
                    debug=True, 
                    use_reloader=True,
                    allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Safety Monitor...")
        global monitoring_active
        monitoring_active = False
        if camera_manager:
            camera_manager.stop_capture()
        print("   Safety Monitor stopped")

if __name__ == '__main__':
    main() 