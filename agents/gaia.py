"""Gaia — Growth and distribution agent for Post AI Company."""

import json
import os
import re
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional

from .base import BaseAgent

_SYSTEM = """You are Gaia, the growth and distribution agent for Post AI Company.

Your responsibilities:
- Convert newsletter markdown to clean email HTML
- Generate SEO metadata (title, description, og tags)
- Coordinate distribution across channels

Rules:
- Email HTML must be compatible with major email clients (Gmail, Apple Mail, Outlook)
- SEO descriptions: 150-160 characters, include primary keyword
- Be precise with character counts and formatting"""

_SEO_PROMPT = """Generate SEO metadata for this content:

TITLE: {title}
CONTENT (excerpt):
{content_excerpt}

Output as JSON:
{{
  "meta_title": "...",
  "meta_description": "...",
  "og_title": "...",
  "og_description": "...",
  "keywords": ["...", "..."],
  "canonical_path": "..."
}}

Rules:
- meta_description: 150-160 characters
- og_description: 200-250 characters
- Include "Post AI Company" or "Post AI Weekly" in meta_title
- Focus on revenue per employee, AI-native companies, post-AI org design"""


class GaiaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Gaia", model="claude-haiku-4-5-20251001")

    def newsletter_md_to_html(self, md: str, subject: str) -> str:
        """Convert newsletter markdown to email-safe HTML."""
        body = _md_to_html(md)
        return _NEWSLETTER_HTML_TEMPLATE.format(
            subject=subject,
            body=body,
            year=datetime.now().year,
        )

    def send_newsletter(
        self,
        subject: str,
        html: str,
        text: str,
        audience_id: Optional[str] = None,
    ) -> bool:
        """Send newsletter broadcast via Resend API."""
        api_key = os.environ.get("RESEND_API_KEY")
        if not api_key:
            self.log("RESEND_API_KEY not set — skipping send")
            return False

        aud_id = audience_id or os.environ.get("RESEND_AUDIENCE_ID", "")
        if not aud_id:
            self.log("RESEND_AUDIENCE_ID not set — skipping send")
            return False

        from_email = os.environ.get("FROM_EMAIL", "Post AI Company <hello@postaicompany.com>")

        payload = {
            "from": from_email,
            "to": [f"audience:{aud_id}"],
            "subject": subject,
            "html": html,
            "text": text,
        }

        try:
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=json.dumps(payload).encode(),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "PostAIGaia/1.0",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                self.log(f"Email sent: {result.get('id', 'unknown')}")
                return True
        except urllib.error.HTTPError as e:
            self.log(f"Resend error {e.code}: {e.read().decode()[:300]}")
            return False
        except Exception as e:
            self.log(f"send_newsletter failed: {e}")
            return False

    def get_subscriber_count(self, audience_id: Optional[str] = None) -> Optional[int]:
        """Fetch current subscriber count from Resend."""
        api_key = os.environ.get("RESEND_API_KEY")
        aud_id = audience_id or os.environ.get("RESEND_AUDIENCE_ID", "")
        if not api_key or not aud_id:
            return None
        try:
            req = urllib.request.Request(
                f"https://api.resend.com/audiences/{aud_id}/contacts",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "User-Agent": "PostAIGaia/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                contacts = data.get("data", [])
                active = [c for c in contacts if not c.get("unsubscribed", True)]
                return len(active)
        except Exception as e:
            self.log(f"get_subscriber_count failed: {e}")
            return None

    def ping_gsc(self, url: str) -> bool:
        """Ping Google Search Console indexing API for a new URL."""
        api_key = os.environ.get("GSC_API_KEY", "")
        if not api_key:
            self.log(f"GSC_API_KEY not set — skipping GSC ping for {url}")
            return False
        try:
            payload = {"url": url, "type": "URL_UPDATED"}
            req = urllib.request.Request(
                f"https://indexing.googleapis.com/v3/urlNotifications:publish?key={api_key}",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                self.log(f"GSC ping OK for {url}")
                return True
        except Exception as e:
            self.log(f"GSC ping failed for {url}: {e}")
            return False

    def generate_seo_metadata(self, title: str, content: str) -> dict:
        """Generate SEO metadata for a piece of content."""
        prompt = _SEO_PROMPT.format(
            title=title,
            content_excerpt=content[:1500],
        )
        raw = self.call(_SYSTEM, prompt, max_tokens=600)
        try:
            m = re.search(r"\{[\s\S]+\}", raw)
            return json.loads(m.group(0)) if m else {}
        except json.JSONDecodeError:
            return {}

    def post_social_copy(self, platform: str, content: str, hook: str) -> str:
        """Generate platform-optimised social copy. Returns text ready to post."""
        limits = {"linkedin": 700, "twitter": 280, "instagram": 2200}
        limit = limits.get(platform, 500)
        prompt = (
            f"Write a {platform} post (max {limit} chars) for Post AI Company.\n\n"
            f"HOOK: {hook}\n\nCONTENT SUMMARY:\n{content[:800]}\n\n"
            f"Tone: direct, data-driven, no hype. Include 2-3 relevant hashtags at the end."
        )
        return self.call(_SYSTEM, prompt, max_tokens=400)


def _md_to_html(md: str) -> str:
    """Minimal markdown-to-email-HTML converter (no external deps)."""
    lines = md.split("\n")
    html_parts = []
    in_para = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("---") and len(stripped) == 3:
            if in_para:
                html_parts.append("</p>")
                in_para = False
            html_parts.append('<hr style="border:none;border-top:1px solid #e5e7eb;margin:24px 0;">')
            continue

        if stripped.startswith("# ") and not stripped.startswith("## "):
            if in_para:
                html_parts.append("</p>")
                in_para = False
            text = _inline(stripped[2:])
            html_parts.append(f'<h1 style="font-size:24px;font-weight:700;color:#111827;margin:0 0 16px;">{text}</h1>')
            continue

        if stripped.startswith("## "):
            if in_para:
                html_parts.append("</p>")
                in_para = False
            text = _inline(stripped[3:])
            html_parts.append(f'<h2 style="font-size:16px;font-weight:700;color:#111827;letter-spacing:0.08em;text-transform:uppercase;margin:32px 0 12px;">{text}</h2>')
            continue

        if stripped.startswith("### "):
            if in_para:
                html_parts.append("</p>")
                in_para = False
            text = _inline(stripped[4:])
            html_parts.append(f'<h3 style="font-size:15px;font-weight:600;color:#374151;margin:20px 0 8px;">{text}</h3>')
            continue

        if not stripped:
            if in_para:
                html_parts.append("</p>")
                in_para = False
            continue

        if stripped.startswith("- "):
            if in_para:
                html_parts.append("</p>")
                in_para = False
            text = _inline(stripped[2:])
            html_parts.append(f'<li style="margin-bottom:6px;">{text}</li>')
            continue

        # Regular paragraph text
        text = _inline(stripped)
        if not in_para:
            html_parts.append('<p style="margin:0 0 16px;line-height:1.7;color:#374151;">')
            in_para = True
        else:
            html_parts.append(" ")
        html_parts.append(text)

    if in_para:
        html_parts.append("</p>")

    return "\n".join(html_parts)


def _inline(text: str) -> str:
    """Process inline markdown (bold, italic, links)."""
    # Links [text](url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" style="color:#2563eb;">\1</a>', text)
    # Bold **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic *text*
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


_NEWSLETTER_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
</head>
<body style="margin:0;padding:0;background:#f9fafb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f9fafb;">
<tr><td align="center" style="padding:32px 16px;">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;max-width:600px;width:100%;">

<!-- Header -->
<tr><td style="background:#111827;padding:24px 40px;">
<p style="margin:0;font-size:13px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#9ca3af;">Post AI Company</p>
<p style="margin:4px 0 0;font-size:20px;font-weight:700;color:#ffffff;">Post AI Weekly</p>
</td></tr>

<!-- Body -->
<tr><td style="padding:40px 40px 32px;">
{body}
</td></tr>

<!-- Footer -->
<tr><td style="background:#f3f4f6;padding:24px 40px;border-top:1px solid #e5e7eb;">
<p style="margin:0;font-size:12px;color:#6b7280;line-height:1.6;">
You're receiving this because you subscribed to Post AI Weekly.<br>
<a href="{{{{unsubscribe_url}}}}" style="color:#6b7280;">Unsubscribe</a> ·
<a href="https://postaicompany.com" style="color:#6b7280;">postaicompany.com</a>
</p>
<p style="margin:12px 0 0;font-size:11px;color:#9ca3af;">
© {year} Post AI Company. We document the birth of the post-AI company.
</p>
</td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""
