#!/usr/bin/env python3
"""
Simple HTTP Server
A basic HTTP server implementation using Python's built-in http.server module.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

class SimpleHTTPServer(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with enhanced logging."""
    
    def log_message(self, format, *args):
        """Override to provide better logging."""
        print(f"[{self.log_date_time_string()}] {format % args}")
    
    def end_headers(self):
        """Add CORS headers for development."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def check_files(port):
    """Check what files are available to serve."""
    current_dir = os.getcwd()
    html_files = [f for f in os.listdir(current_dir) if f.endswith('.html')]
    
    if html_files:
        print(f"📄 Found HTML files: {', '.join(html_files)}")
        print(f"🌐 Main page: http://localhost:{port}/{html_files[0]}")
    else:
        print("📄 No HTML files found in current directory")
        print("💡 Create an index.html file to serve a main page")
    
    # Check for other common web files
    web_files = [f for f in os.listdir(current_dir) if f.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif'))]
    if web_files:
        print(f"🎨 Found web assets: {', '.join(web_files)}")

def main():
    """Main function to start the HTTP server."""
    PORT = 8000
    
    # Check for existing files instead of creating them
    check_files(PORT)
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleHTTPServer) as httpd:
            print(f"🌐 Server started at http://localhost:{PORT}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print(f"📂 Directory listing: http://localhost:{PORT}/")
            print("\nPress Ctrl+C to stop the server")
            print("-" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("Goodbye! 👋")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Try a different port or stop the existing service.")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
