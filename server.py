#!/usr/bin/env python3.13
"""Serve landing page + proxy /api/subscribe → Resend API."""

import json
import os
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import HTTPError

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "re_QibGt1ao_7vqqJC5v7ebnhXc529d1cyfh")
RESEND_AUDIENCE_ID = os.environ.get("RESEND_AUDIENCE_ID", "")  # preenchido após criar
FROM_EMAIL = "Post AI Company <hello@postaicompany.com>"

PORT = 9090


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/subscribe":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(body)
                email = (data.get("email") or "").strip().lower()
            except json.JSONDecodeError:
                self._json({"ok": False, "error": "invalid json"}, 400)
                return

            if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                self._json({"ok": False, "error": "email inválido"}, 400)
                return

            ok, error = add_to_resend(email)
            if ok:
                self._json({"ok": True})
                print(f"[subscribe] {email} → OK")
            else:
                self._json({"ok": False, "error": error}, 500)
                print(f"[subscribe] {email} → FAIL: {error}")
        elif self.path == "/api/contact":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(body)
                name = (data.get("name") or "").strip()
                email = (data.get("email") or "").strip().lower()
                message = (data.get("message") or "").strip()
            except json.JSONDecodeError:
                self._json({"ok": False, "error": "invalid json"}, 400)
                return

            if not name or not email or not message:
                self._json({"ok": False, "error": "name, email, and message are required"}, 400)
                return
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                self._json({"ok": False, "error": "invalid email"}, 400)
                return

            ok, error = send_contact_email(name, email, message)
            if ok:
                self._json({"ok": True})
                print(f"[contact] {name} <{email}> → OK")
            else:
                self._json({"ok": False, "error": error}, 500)
                print(f"[contact] {name} <{email}> → FAIL: {error}")
        else:
            self._json({"ok": False, "error": "not found"}, 404)

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def add_to_resend(email: str) -> tuple[bool, str | None]:
    """Add contact to Resend audience. Returns (ok, error_message)."""
    if not RESEND_AUDIENCE_ID:
        # Fallback: log e retorna ok (pra não quebrar o UX enquanto configura)
        print(f"[resend] audience_id não configurado — email {email} apenas logado")
        return True, None

    try:
        req = Request(
            f"https://api.resend.com/audiences/{RESEND_AUDIENCE_ID}/contacts",
            data=json.dumps({
                "email": email,
                "unsubscribed": False,
            }).encode(),
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "PostAILanding/1.0",
            },
            method="POST",
        )
        resp = urlopen(req, timeout=10)
        print(f"[resend] contact added: {resp.read().decode()}")
        return True, None
    except HTTPError as e:
        body = e.read().decode()
        return False, f"Resend HTTP {e.code}: {body[:200]}"
    except Exception as e:
        return False, str(e)


def send_contact_email(name: str, email: str, message: str) -> tuple[bool, str | None]:
    """Forward contact form submission via Resend to fefaria@syntheticperson.ai."""
    try:
        req = Request(
            "https://api.resend.com/emails",
            data=json.dumps({
                "from": "Post AI Company <hello@postaicompany.com>",
                "to": ["fefaria@syntheticperson.ai"],
                "subject": f"Post AI Contact: {name}",
                "text": f"Name: {name}\nEmail: {email}\n\n{message}",
            }).encode(),
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "PostAIContact/1.0",
            },
            method="POST",
        )
        resp = urlopen(req, timeout=10)
        print(f"[contact] email sent: {resp.read().decode()}")
        return True, None
    except HTTPError as e:
        body = e.read().decode()
        return False, f"Resend HTTP {e.code}: {body[:200]}"
    except Exception as e:
        return False, str(e)


def main():
    import os as _os
    _os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print(f"Serving on http://0.0.0.0:{PORT}")
    print(f"Resend audience_id: {'configurado' if RESEND_AUDIENCE_ID else 'NÃO CONFIGURADO (apenas log)'}")

    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
