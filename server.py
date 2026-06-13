#!/usr/bin/env python3.13
"""Serve landing page + analytics + subscriber storage + /api/subscribe → Resend API."""

import csv
import json
import os
import re
import time
from datetime import date, datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import StringIO
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_AUDIENCE_ID = os.environ.get("RESEND_AUDIENCE_ID", "")
FROM_EMAIL = "Post AI Company <hello@postaicompany.com>"

PORT = 9090
ANALYTICS_FILE = Path(__file__).parent / ".analytics.json"
SUBSCRIBERS_CSV = Path(__file__).parent / ".subscribers.csv"


# ─── Rate Limiting ───
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = 5      # max requests per window per IP
_rate_limit_store: dict[str, list[float]] = {}

def check_rate_limit(ip: str) -> bool:
    now = time.time()
    if ip not in _rate_limit_store:
        _rate_limit_store[ip] = []
    _rate_limit_store[ip] = [t for t in _rate_limit_store[ip] if now - t < RATE_LIMIT_WINDOW]
    if len(_rate_limit_store[ip]) >= RATE_LIMIT_MAX:
        return False
    _rate_limit_store[ip].append(now)
    return True

# ─── Analytics ───

def load_analytics() -> dict:
    if ANALYTICS_FILE.exists():
        try:
            return json.loads(ANALYTICS_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "total_subscribers": 0,
        "subscribers_by_role": {"founder": 0, "transformer": 0, "curious": 0},
        "daily_subscribers": {},
        "total_pageviews": 0,
        "daily_pageviews": {},
        "pageviews_by_path": {},
        "first_subscriber": None,
        "last_activity": None,
    }


def save_analytics(data: dict):
    ANALYTICS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def track_subscriber(role: str, email: str, whatsapp: str = ""):
    data = load_analytics()
    today = date.today().isoformat()

    data["total_subscribers"] += 1
    data["daily_subscribers"][today] = data["daily_subscribers"].get(today, 0) + 1

    role_key = role if role in ("founder", "transformer") else "curious"
    data["subscribers_by_role"][role_key] = data["subscribers_by_role"].get(role_key, 0) + 1

    if data["first_subscriber"] is None:
        data["first_subscriber"] = today

    data["last_activity"] = datetime.now(timezone.utc).isoformat()
    save_analytics(data)

    # Salvar no CSV local
    save_subscriber_csv(email, role_key, whatsapp)

    print(f"[subscriber] #{data['total_subscribers']} — {email} — role: {role_key} — whatsapp: {whatsapp or 'não'}")


def save_subscriber_csv(email: str, role: str, whatsapp: str = ""):
    """Append subscriber to local CSV for backup/export."""
    file_exists = SUBSCRIBERS_CSV.exists()
    with open(SUBSCRIBERS_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "role", "whatsapp", "subscribed_at"])
        writer.writerow([email, role, whatsapp, datetime.now(timezone.utc).isoformat()])


def track_pageview(path: str):
    data = load_analytics()
    today = date.today().isoformat()

    data["total_pageviews"] += 1
    data["daily_pageviews"][today] = data["daily_pageviews"].get(today, 0) + 1
    data["pageviews_by_path"][path] = data["pageviews_by_path"].get(path, 0) + 1
    data["last_activity"] = datetime.now(timezone.utc).isoformat()
    save_analytics(data)


def get_stats() -> dict:
    data = load_analytics()
    today = date.today().isoformat()

    top_pages = sorted(data["pageviews_by_path"].items(), key=lambda x: x[1], reverse=True)[:10]

    from datetime import timedelta
    last_7 = [(date.today() - timedelta(days=i)).isoformat() for i in range(7)]
    last_7.reverse()

    # Count subscribers from CSV
    total_from_csv = 0
    if SUBSCRIBERS_CSV.exists():
        with open(SUBSCRIBERS_CSV) as f:
            total_from_csv = max(0, sum(1 for _ in f) - 1)  # minus header

    return {
        "total_subscribers": data["total_subscribers"],
        "subscribers_in_csv": total_from_csv,
        "subscribers_today": data["daily_subscribers"].get(today, 0),
        "subscribers_by_role": data["subscribers_by_role"],
        "total_pageviews": data["total_pageviews"],
        "pageviews_today": data["daily_pageviews"].get(today, 0),
        "top_pages": [{"path": p, "views": v} for p, v in top_pages],
        "last_7_days": {
            "subscribers": {d: data["daily_subscribers"].get(d, 0) for d in last_7},
            "pageviews": {d: data["daily_pageviews"].get(d, 0) for d in last_7},
        },
        "first_subscriber": data["first_subscriber"],
        "last_activity": data["last_activity"],
    }


def send_welcome_email(email: str, role: str) -> bool:
    """Send welcome email via Resend."""
    welcome_text = f"""Welcome to Post AI Company.

You're receiving this because you subscribed to Post AI Weekly — the newsletter documenting the birth of the post-AI company.

Every Wednesday, we send data, analysis, and provocations on how companies are being rebuilt around AI. Revenue per employee. Org design. Case studies. No hype. Just signal.

Your first edition arrives this Wednesday at 6am BRT.

In the meantime:
→ Read past editions: https://postaicompany.com/editions
→ Listen to the podcast: https://postaicompany.com/podcast
→ Check the Radar: https://postaicompany.com/radar

If you ever want to unsubscribe, just reply to this email.

— Fernanda Faria
Founder, Post AI Company"""

    try:
        req = Request(
            "https://api.resend.com/emails",
            data=json.dumps({
                "from": FROM_EMAIL,
                "to": [email],
                "subject": "Welcome to Post AI Company — your first edition arrives Wednesday",
                "text": welcome_text,
            }).encode(),
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "PostAIWelcome/1.0",
            },
            method="POST",
        )
        resp = urlopen(req, timeout=10)
        print(f"[welcome] email sent to {email}: {resp.read().decode()}")
        return True
    except Exception as e:
        print(f"[welcome] FAILED for {email}: {e}")
        return False


# ─── Bot Scan Blocklist ───
# Paths that are never real traffic — scanners hitting common vuln/config paths.
# Blocked early: 404, no pageview, no filesystem access.
_BOT_SCAN_PREFIXES = (
    "/wp-", "/wp-admin", "/wp-content", "/wp-includes", "/wp-login",
    "/.env", "/.git/", "/.aws/", "/.ssh/", "/.docker/",
    "/admin/", "/administrator/", "/backup/", "/bak/",
    "/phpmyadmin/", "/phpMyAdmin/", "/pma/", "/mysql/",
    "/.well-known/acme-challenge/",  # Let's Encrypt — some are bots probing
    "/actuator/",  # Spring Boot
    "/api/v1/", "/api/v2/",  # generic API probes
    "/config/", "/configuration/", "/debug/",
    "/vendor/", "/node_modules/",
    "/console/", "/cron/",
    "/favicon.ico",  # most are real, but don't count as pageviews
)

def _is_bot_scan(path: str) -> bool:
    path_lower = path.lower()
    for prefix in _BOT_SCAN_PREFIXES:
        if path_lower.startswith(prefix):
            return True
    # Also catch paths with suspicious extensions
    if any(path_lower.endswith(ext) for ext in ('.php', '.asp', '.aspx', '.jsp', '.cgi', '.sql', '.bak', '.swp', '.save', '.tar', '.gz', '.zip', '.rar', '.7z', '.env', '.ini', '.conf', '.config', '.log')):
        return True
    return False


# ─── Handler ───

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if hasattr(self, 'command') and self.command == 'GET':
            path = self.path.split('?')[0]
            if not any(path.endswith(ext) for ext in ('.css','.js','.png','.jpg','.svg','.ico','.woff2','.xml','.json','.txt')) \
               and not _is_bot_scan(path):
                track_pageview(path)

    def do_GET(self):
        if self.path == "/api/stats":
            self._json(get_stats())
            return

        # Block bot scans early — no pageview, no filesystem hit
        path = self.path.split('?')[0]
        if _is_bot_scan(path):
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        super().do_GET()

    def do_POST(self):
        if self.path == "/api/subscribe":
            # Rate limit check
            client_ip = self.client_address[0]
            if not check_rate_limit(client_ip):
                self._json({"ok": False, "error": "rate limit exceeded, try again in 1 minute"}, 429)
                return

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(body)
                email = (data.get("email") or "").strip().lower()
                role = (data.get("role") or "").strip().lower()
                whatsapp = (data.get("whatsapp") or "").strip()
            except json.JSONDecodeError:
                self._json({"ok": False, "error": "invalid json"}, 400)
                return

            if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                self._json({"ok": False, "error": "email inválido"}, 400)
                return

            # Salvar localmente (sempre, independente do Resend)
            track_subscriber(role, email, whatsapp)

            # Enviar welcome email (assíncrono mental — é síncrono mas não bloqueia resposta)
            welcome_ok = send_welcome_email(email, role)

            # Adicionar ao Resend (se configurado)
            ok, error = add_to_resend(email)

            self._json({
                "ok": True,
                "welcome_sent": welcome_ok,
            })

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
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# ─── Resend integration ───

def add_to_resend(email: str) -> tuple[bool, str | None]:
    if not RESEND_AUDIENCE_ID:
        print(f"[resend] audience_id não configurado — email {email} não enviado ao Resend")
        return True, None

    try:
        req = Request(
            f"https://api.resend.com/audiences/{RESEND_AUDIENCE_ID}/contacts",
            data=json.dumps({"email": email, "unsubscribed": False}).encode(),
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
    try:
        req = Request(
            "https://api.resend.com/emails",
            data=json.dumps({
                "from": FROM_EMAIL,
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


# ─── Main ───

def main():
    import os as _os
    _os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if not ANALYTICS_FILE.exists():
        save_analytics(load_analytics())
        print("[analytics] Initialized")

    if not SUBSCRIBERS_CSV.exists():
        with open(SUBSCRIBERS_CSV, "w", newline="") as f:
            csv.writer(f).writerow(["email", "role", "whatsapp", "subscribed_at"])
        print("[subscribers] CSV initialized")

    print(f"Serving on http://0.0.0.0:{PORT}")
    print(f"Subscribers CSV: {SUBSCRIBERS_CSV}")
    print(f"Analytics JSON: {ANALYTICS_FILE}")
    print(f"Resend audience_id: {'configurado' if RESEND_AUDIENCE_ID else 'NÃO CONFIGURADO (apenas log)'}")
    if not RESEND_AUDIENCE_ID:
        print("[warn] Emails salvos APENAS no CSV local. Configure RESEND_AUDIENCE_ID para enviar newsletters.")

    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
