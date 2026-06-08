"""Vercel serverless function: POST /api/subscribe → Resend audience."""

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _resend import add_to_resend, EMAIL_RE


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(body)
            email = (data.get("email") or "").strip().lower()
        except json.JSONDecodeError:
            return self._json({"ok": False, "error": "invalid json"}, 400)

        if not email or not re.match(EMAIL_RE, email):
            return self._json({"ok": False, "error": "email inválido"}, 400)

        ok, error = add_to_resend(email)
        if ok:
            print(f"[subscribe] {email} → OK")
            return self._json({"ok": True})
        print(f"[subscribe] {email} → FAIL: {error}")
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
