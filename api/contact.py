"""Vercel serverless function: POST /api/contact → Resend email."""

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _resend import send_contact_email, EMAIL_RE


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(body)
            name = (data.get("name") or "").strip()
            email = (data.get("email") or "").strip().lower()
            message = (data.get("message") or "").strip()
        except json.JSONDecodeError:
            return self._json({"ok": False, "error": "invalid json"}, 400)

        if not name or not email or not message:
            return self._json({"ok": False, "error": "name, email, and message are required"}, 400)
        if not re.match(EMAIL_RE, email):
            return self._json({"ok": False, "error": "invalid email"}, 400)

        ok, error = send_contact_email(name, email, message)
        if ok:
            print(f"[contact] {name} <{email}> → OK")
            return self._json({"ok": True})
        print(f"[contact] {name} <{email}> → FAIL: {error}")
        return self._json({"ok": False, "error": error}, 500)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
