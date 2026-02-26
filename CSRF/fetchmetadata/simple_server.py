#!/usr/bin/env python3
"""
Simple HTTP Server
A basic HTTP server implementation using Python's built-in http.server module.
"""

import http.server
import socketserver
import os
import sys
import json
from urllib.parse import parse_qs

# In-memory state for demo transfers.
DEMO_ACCOUNT = {
    "owner": "victim_user",
    "balance": 5000.0,
    "transfers": [],
}

SAFE_HTTP_METHODS = {"GET", "HEAD", "OPTIONS"}

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
        if self.command == "GET" and self.path in ("/", "/index.html"):
            # Demo-only cookie issuance from server side.
            # Using Set-Cookie better reflects real auth/session handling.
            self.send_header(
                "Set-Cookie",
                "session=victim123; Path=/; HttpOnly; SameSite=None",
            )
        super().end_headers()

    def _send_json(self, status_code, payload):
        """Send JSON payload with status code."""
        response_body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def _log_fetch_metadata_headers(self):
        """Print Fetch Metadata headers for request inspection."""
        print("🔎 Fetch Metadata headers:")
        print(f"   Sec-Fetch-Site: {self.headers.get('Sec-Fetch-Site', '<missing>')}")
        print(f"   Sec-Fetch-Mode: {self.headers.get('Sec-Fetch-Mode', '<missing>')}")
        print(f"   Sec-Fetch-Dest: {self.headers.get('Sec-Fetch-Dest', '<missing>')}")
        print(f"   Sec-Fetch-User: {self.headers.get('Sec-Fetch-User', '<missing>')}")

    def _validate_fetch_metadata(self):
        """Validate Fetch Metadata headers to mitigate CSRF on unsafe methods."""
        if self.command in SAFE_HTTP_METHODS:
            return True, "Safe method"

        sec_fetch_site = self.headers.get("Sec-Fetch-Site", "").lower()
        sec_fetch_mode = self.headers.get("Sec-Fetch-Mode", "").lower()

        if not sec_fetch_site:
            return False, "Missing Sec-Fetch-Site header"

        if sec_fetch_site == "cross-site":
            return False, "Cross-site state-changing requests are blocked"

        if sec_fetch_site == "none" and sec_fetch_mode != "navigate":
            return False, "Sec-Fetch-Site=none is only allowed for navigations"

        return True, "Fetch Metadata validation passed"

    def do_POST(self):
        """Handle POST requests for transfer API protected by Fetch Metadata."""
        if self.path != "/transfer":
            self._send_json(404, {"status": "error", "message": "Unknown POST route"})
            return

        self._log_fetch_metadata_headers()

        is_valid_fetch, fetch_message = self._validate_fetch_metadata()
        if not is_valid_fetch:
            print(f"🛡️ Blocked request by Fetch Metadata policy: {fetch_message}")
            self._send_json(
                403,
                {
                    "status": "error",
                    "message": "Request blocked by Fetch Metadata policy",
                    "reason": fetch_message,
                },
            )
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(raw_body)

        recipient = form_data.get("to", [""])[0].strip()
        amount_raw = form_data.get("amount", [""])[0].strip()

        if not recipient:
            self._send_json(400, {"status": "error", "message": "Missing required field: to"})
            return

        try:
            amount = float(amount_raw)
        except ValueError:
            self._send_json(400, {"status": "error", "message": "Amount must be numeric"})
            return

        if amount <= 0:
            self._send_json(400, {"status": "error", "message": "Amount must be greater than 0"})
            return

        if amount > DEMO_ACCOUNT["balance"]:
            self._send_json(400, {"status": "error", "message": "Insufficient funds"})
            return

        # Demo auth model still uses a cookie, but requests are now gated with
        # Fetch Metadata header validation before state-changing actions.
        cookie_header = self.headers.get("Cookie", "")
        if "session=victim123" not in cookie_header:
            self._send_json(
                401,
                {
                    "status": "error",
                    "message": "Unauthorized: missing demo session cookie",
                },
            )
            return

        DEMO_ACCOUNT["balance"] -= amount
        transfer_record = {"to": recipient, "amount": amount}
        DEMO_ACCOUNT["transfers"].append(transfer_record)

        print(
            f"💸 Transfer processed: to={recipient}, amount={amount}, "
            f"remaining_balance={DEMO_ACCOUNT['balance']:.2f}"
        )
        self._send_json(
            200,
            {
                "status": "ok",
                "to": recipient,
                "amount": amount,
                "remaining_balance": round(DEMO_ACCOUNT["balance"], 2),
                "transfer_count": len(DEMO_ACCOUNT["transfers"]),
            },
        )

    def do_OPTIONS(self):
        """Allow preflight requests in local development demos."""
        self.send_response(204)
        self.end_headers()

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
