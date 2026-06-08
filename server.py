#!/usr/bin/env python3
"""Local dev server: serve the landing page + /api/subscribe and /api/contact.

Mirrors the Vercel serverless functions in api/ for local development.
Secrets are read from the environment (see .env.example) — there are no
hardcoded keys. In production the api/ functions handle these routes.
"""

import json
import os
import re
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "api"))
from _resend import add_to_resend, send_contact_email, EMAIL_RE

PORT = int(os.environ.get("PORT", "9090"))

# Long-cache immutable-ish static assets; short-cache HTML so content updates ship fast.
CACHEABLE_EXT = (".css", ".js", ".woff2", ".woff", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".ico", ".mp3", ".mp4")


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/subscribe":
            data = self._read_json()
            if data is None:
                return
            email = (data.get("email") or "").strip().lower()
            if not email or not re.match(EMAIL_RE, email):
                return self._json({"ok": False, "error": "email inválido"}, 400)
            ok, error = add_to_resend(email)
            if ok:
                print(f"[subscribe] {email} → OK")
                return self._json({"ok": True})
            print(f"[subscribe] {email} → FAIL: {error}")
            return self._json({"ok": False, "error": error}, 500)

        if self.path == "/api/contact":
            data = self._read_json()
            if data is None:
                return
            name = (data.get("name") or "").strip()
            email = (data.get("email") or "").strip().lower()
            message = (data.get("message") or "").strip()
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

        self._json({"ok": False, "error": "not found"}, 404)

    def end_headers(self):
        # Add caching headers for static assets (HTML stays short-lived).
        path = self.path.split("?", 1)[0]
        if path.endswith(CACHEABLE_EXT):
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        elif path.endswith(".html") or path.endswith("/"):
            self.send_header("Cache-Control", "public, max-age=300")
        super().end_headers()

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            self._json({"ok": False, "error": "invalid json"}, 400)
            return None

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        super().end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.environ.get("RESEND_API_KEY"):
        print("WARNING: RESEND_API_KEY not set — /api/subscribe and /api/contact will return errors.")
    print(f"Serving on http://0.0.0.0:{PORT}")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
