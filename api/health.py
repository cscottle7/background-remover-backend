"""
Health check endpoint for CharacterCut Backend
"""

from http.server import BaseHTTPRequestHandler
import json
import time

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def do_GET(self):
        """Health check handler"""
        response_data = {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "2.0.0-backend-dedicated",
            "environment": "vercel-backend",
            "service": "charactercut-backend"
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_json = json.dumps(response_data)
        self.wfile.write(response_json.encode('utf-8'))