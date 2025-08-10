"""
CharacterCut Backend API - Process Endpoint
Dedicated Vercel Python function for background removal
"""

from http.server import BaseHTTPRequestHandler
import json
import time
import uuid
import base64
from datetime import datetime, timedelta
import logging
import cgi
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global session cache
_rembg_session = None

def get_rembg_session():
    """Initialize and cache rembg session"""
    global _rembg_session
    if _rembg_session is None:
        try:
            from rembg import new_session
            # Use u2net model for good quality
            _rembg_session = new_session("u2net")
            logger.info("Initialized rembg session with u2net model")
        except Exception as e:
            logger.error(f"Failed to initialize rembg: {e}")
            raise Exception(f"Model initialization failed: {str(e)}")
    return _rembg_session

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
        
    def do_POST(self):
        """Handle image processing requests"""
        start_time = time.time()
        processing_id = str(uuid.uuid4())
        
        try:
            # Validate content type
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self.send_error_response(400, "Content-Type must be multipart/form-data")
                return
            
            # Check content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 10 * 1024 * 1024:  # 10MB limit
                self.send_error_response(400, "File too large. Maximum size is 10MB.")
                return
            
            # Read and parse form data
            post_data = self.rfile.read(content_length)
            form_data = cgi.FieldStorage(
                fp=BytesIO(post_data),
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            # Extract file
            if 'file' not in form_data:
                self.send_error_response(400, "No file provided")
                return
            
            file_item = form_data['file']
            if not file_item.file:
                self.send_error_response(400, "Invalid file")
                return
            
            image_data = file_item.file.read()
            filename = getattr(file_item, 'filename', 'unknown')
            
            logger.info(f"Processing image: {filename}, size: {len(image_data)} bytes")
            
            # Process image with rembg
            try:
                from rembg import remove
                session = get_rembg_session()
                
                processed_image_bytes = remove(
                    image_data,
                    session=session,
                    force_return_bytes=True
                )
                
                logger.info("Image processing completed successfully")
                
            except Exception as e:
                logger.error(f"rembg processing failed: {e}")
                self.send_error_response(503, f"Background removal failed: {str(e)}")
                return
            
            processing_time = time.time() - start_time
            
            # Convert to base64 for response
            processed_image_b64 = base64.b64encode(processed_image_bytes).decode('utf-8')
            data_url = f"data:image/png;base64,{processed_image_b64}"
            
            # Create response
            response_data = {
                "processing_id": processing_id,
                "session_id": str(uuid.uuid4()),
                "download_url": data_url,
                "processing_time": processing_time,
                "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z",
                "model": "u2net",
                "status": "completed"
            }
            
            # Send successful response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()
            
            response_json = json.dumps(response_data)
            self.wfile.write(response_json.encode('utf-8'))
            
            logger.info(f"Successfully processed in {processing_time:.2f}s")
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Request failed after {processing_time:.2f}s: {str(e)}")
            self.send_error_response(500, f"Processing failed: {str(e)}")
    
    def send_error_response(self, status_code, message):
        """Send JSON error response with CORS headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        error_data = {
            "detail": message,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "error"
        }
        
        error_json = json.dumps(error_data)
        self.wfile.write(error_json.encode('utf-8'))