"""Shared Resend integration for local dev server and Vercel serverless funcs.

Files prefixed with `_` are ignored by Vercel's filesystem router, so this is
a plain importable module — not an endpoint. All secrets are read from the
environment at call time; there are no hardcoded fallbacks.
"""

import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError

FROM_EMAIL = os.environ.get("FROM_EMAIL", "Post AI Company <hello@postaicompany.com>")
CONTACT_TO_EMAIL = os.environ.get("CONTACT_TO_EMAIL", "fefaria@syntheticperson.ai")

EMAIL_RE = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def _resend_key() -> str | None:
    return os.environ.get("RESEND_API_KEY")


def add_to_resend(email: str) -> tuple[bool, str | None]:
    """Add a contact to the Resend audience. Returns (ok, error_message)."""
    api_key = _resend_key()
    if not api_key:
        return False, "RESEND_API_KEY not configured"

    audience_id = os.environ.get("RESEND_AUDIENCE_ID", "")
    if not audience_id:
        # Fallback: log and succeed so the UX doesn't break before the
        # audience is provisioned.
        print(f"[resend] audience_id não configurado — email {email} apenas logado")
        return True, None

    try:
        req = Request(
            f"https://api.resend.com/audiences/{audience_id}/contacts",
            data=json.dumps({"email": email, "unsubscribed": False}).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "PostAILanding/1.0",
            },
            method="POST",
        )
        resp = urlopen(req, timeout=10)
        print(f"[resend] contact added: {resp.read().decode()}")
        return True, None
    except HTTPError as e:
        return False, f"Resend HTTP {e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return False, str(e)


def send_contact_email(name: str, email: str, message: str) -> tuple[bool, str | None]:
    """Forward a contact form submission via Resend. Returns (ok, error_message)."""
    api_key = _resend_key()
    if not api_key:
        return False, "RESEND_API_KEY not configured"

    try:
        req = Request(
            "https://api.resend.com/emails",
            data=json.dumps({
                "from": FROM_EMAIL,
                "to": [CONTACT_TO_EMAIL],
                "subject": f"Post AI Contact: {name}",
                "text": f"Name: {name}\nEmail: {email}\n\n{message}",
            }).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "PostAIContact/1.0",
            },
            method="POST",
        )
        resp = urlopen(req, timeout=10)
        print(f"[contact] email sent: {resp.read().decode()}")
        return True, None
    except HTTPError as e:
        return False, f"Resend HTTP {e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return False, str(e)
