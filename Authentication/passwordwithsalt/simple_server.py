#!/usr/bin/env python3
"""
Simple authentication demo server.
Provides:
  - POST /api/register
  - POST /api/login
  - Static file serving (index.html)
"""

import hashlib
import hmac
import http.server
import json
import os
import secrets
import socketserver
import sys


USERS = {}


def hash_password(password, salt):
    """Return a PBKDF2 hash for the password."""
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        # This is the number of iterations of the hash function. This is to slow down the attacker from brute forcing the password.
        120_000,
    )
    return hashed.hex()


class AuthHTTPServer(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with auth API endpoints."""

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def _send_json(self, status_code, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json_body(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/register":
            self.handle_register()
            return

        if self.path == "/api/login":
            self.handle_login()
            return

        self._send_json(404, {"status": "error", "message": "Unknown API route"})

    def handle_register(self):
        payload = self._read_json_body()
        if payload is None:
            self._send_json(400, {"status": "error", "message": "Invalid JSON body"})
            return

        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))

        if len(username) < 3:
            self._send_json(
                400,
                {
                    "status": "error",
                    "message": "Username must be at least 3 characters long",
                },
            )
            return

        if len(password) < 6:
            self._send_json(
                400,
                {
                    "status": "error",
                    "message": "Password must be at least 6 characters long",
                },
            )
            return

        if username in USERS:
            self._send_json(
                409,
                {"status": "error", "message": "Username already exists"},
            )
            return

        salt = secrets.token_hex(16)
        password_hash = hash_password(password, salt)
        USERS[username] = {"salt": salt, "password_hash": password_hash}

        self._send_json(
            201,
            {
                "status": "ok",
                "message": f"User '{username}' created",
            },
        )

    def handle_login(self):
        payload = self._read_json_body()
        if payload is None:
            self._send_json(400, {"status": "error", "message": "Invalid JSON body"})
            return

        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))

        user = USERS.get(username)
        if not user:
            self._send_json(
                401,
                {"status": "error", "message": "Invalid username or password"},
            )
            return

        computed_hash = hash_password(password, user["salt"])
        if not hmac.compare_digest(computed_hash, user["password_hash"]):
            self._send_json(
                401,
                {"status": "error", "message": "Invalid username or password"},
            )
            return

        token = secrets.token_urlsafe(24)
        self._send_json(
            200,
            {
                "status": "ok",
                "message": f"Welcome, {username}",
                "token": token,
            },
        )


def check_files(port):
    current_dir = os.getcwd()
    html_files = [f for f in os.listdir(current_dir) if f.endswith(".html")]

    if html_files:
        print(f"📄 Found HTML files: {', '.join(html_files)}")
        print(f"🌐 Main page: http://localhost:{port}/{html_files[0]}")
    else:
        print("📄 No HTML files found in current directory")


def main():
    port = 8000
    check_files(port)

    try:
        with socketserver.TCPServer(("", port), AuthHTTPServer) as httpd:
            print(f"🌐 Server started at http://localhost:{port}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print("🔐 Endpoints: POST /api/register, POST /api/login")
            print("\nPress Ctrl+C to stop the server")
            print("-" * 50)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except OSError as error:
        if error.errno == 48:
            print(f"❌ Port {port} is already in use.")
        else:
            print(f"❌ Error starting server: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
