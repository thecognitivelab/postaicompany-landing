"""Cris — Research and data agent for Post AI Company."""

import json
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from typing import Optional

from .base import BaseAgent

_SYSTEM = """You are Cris, the research and data agent for Post AI Company.

Your job:
1. Verify facts and claims in newsletter drafts
2. Compile data briefs from fetched sources
3. Extract key stories from AI newsletters
4. Maintain accuracy — every number needs a source

When fact-checking, be precise:
- VERIFIED: claim is accurate with a known source
- APPROXIMATE: claim is directionally correct but exact number uncertain
- ERROR: claim appears incorrect, provide correction
- UNVERIFIED: cannot confirm, flag for editor

Output structured responses. Be terse. No filler."""

_FACTCHECK_PROMPT = """Fact-check the following newsletter draft.

For each factual claim (numbers, company stats, quotes, events):
1. Mark as VERIFIED, APPROXIMATE, or ERROR
2. Note the source if you know it
3. Correct any errors

NEWSLETTER DRAFT:
{draft}

Output format:
- Total claims identified: N
- Verified: N
- Approximate: N
- Errors: N

Then list any corrections or flags:
CLAIM: [original text]
STATUS: [VERIFIED/APPROXIMATE/ERROR]
NOTE: [source or correction]"""

_DATA_BRIEF_PROMPT = """Compile a data brief for a newsletter about: {topic}

Using this fetched source content:
{sources_content}

Extract and compile:
1. The most relevant data points (numbers, company stats, research findings)
2. Key events or announcements from the past week
3. Quotes from founders or executives
4. Links to original sources

Format as a structured brief that a writer can use directly.
Include source attribution for every fact."""

_EXTRACT_STORIES_PROMPT = """Extract the 2-3 most important AI business stories from this newsletter content.

NEWSLETTER: {name}
CONTENT:
{content}

For each story extract:
- Headline
- Key data point or quote
- Why it matters for the post-AI company thesis
- Source URL if mentioned

Be concise. Focus on stories about: company efficiency, headcount decisions,
revenue per employee, AI tool adoption, org design changes, funding."""


class CrisAgent(BaseAgent):
    def __init__(self):
        super().__init__("Cris", model="claude-sonnet-4-6")

    def fetch_url(self, url: str, timeout: int = 15) -> Optional[str]:
        """Fetch URL content. Returns text or None on failure."""
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "PostAIBot/1.0 (research@postaicompany.com)",
                    "Accept": "text/html,application/xhtml+xml,application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                charset = "utf-8"
                ct = resp.headers.get("Content-Type", "")
                if "charset=" in ct:
                    charset = ct.split("charset=")[-1].split(";")[0].strip()
                return resp.read().decode(charset, errors="replace")
        except Exception as e:
            self.log(f"fetch_url failed for {url}: {e}")
            return None

    def fetch_rss(self, url: str) -> list[dict]:
        """Fetch RSS feed. Returns list of {title, link, description, pubDate}."""
        raw = self.fetch_url(url)
        if not raw:
            return []
        try:
            root = ET.fromstring(raw)
            ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
            items = []
            for item in root.findall(".//item")[:5]:
                entry = {
                    "title": (item.findtext("title") or "").strip(),
                    "link": (item.findtext("link") or "").strip(),
                    "description": _strip_tags(item.findtext("description") or "")[:500],
                    "pubDate": (item.findtext("pubDate") or "").strip(),
                }
                content = item.find("content:encoded", ns)
                if content is not None and content.text:
                    entry["description"] = _strip_tags(content.text)[:800]
                items.append(entry)
            return items
        except ET.ParseError as e:
            self.log(f"RSS parse error for {url}: {e}")
            return []

    def fetch_tracked_newsletters(self) -> dict[str, str]:
        """Fetch content from all tracked newsletters. Returns {name: summarized_content}."""
        import os, json as _json

        sources_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config", "sources.json"
        )
        with open(sources_path) as f:
            sources = _json.load(f)["newsletters"]

        results = {}
        for source in sources:
            name = source["name"]
            self.log(f"Fetching {name} via RSS...")
            items = self.fetch_rss(source["rss"])
            if not items:
                self.log(f"RSS failed for {name}, trying homepage...")
                html = self.fetch_url(source["url"])
                if html:
                    items = [{"title": name, "description": _strip_tags(html)[:1500], "link": source["url"], "pubDate": ""}]

            if items:
                raw = f"=== {name} ===\n"
                for item in items[:3]:
                    raw += f"\nTitle: {item['title']}\nURL: {item['link']}\n{item['description'][:600]}\n"
                results[name] = raw

        return results

    def extract_stories(self, name: str, content: str) -> str:
        """Use Claude to extract key stories from a newsletter's content."""
        prompt = _EXTRACT_STORIES_PROMPT.format(name=name, content=content[:3000])
        return self.call(_SYSTEM, prompt, max_tokens=600)

    def compile_data_brief(self, topic: str, fetched_sources: dict[str, str]) -> str:
        """Compile a structured data brief for a given topic from fetched sources."""
        self.log(f"Compiling data brief for: {topic}")
        combined = "\n\n".join(fetched_sources.values()) if fetched_sources else ""
        prompt = _DATA_BRIEF_PROMPT.format(
            topic=topic,
            sources_content=combined[:6000] or "No external sources fetched.",
        )
        return self.call(_SYSTEM, prompt, max_tokens=2000)

    def verify_facts(self, draft: str) -> dict:
        """Fact-check a newsletter draft. Returns structured result dict."""
        self.log("Running fact-check...")
        prompt = _FACTCHECK_PROMPT.format(draft=draft[:6000])
        result_text = self.call(_SYSTEM, prompt, max_tokens=2000)

        verified = _extract_int(result_text, "Verified")
        approximate = _extract_int(result_text, "Approximate")
        errors = _extract_int(result_text, "Errors")

        return {
            "verified": verified,
            "approximate": approximate,
            "errors": errors,
            "raw": result_text,
            "label": f"VERIFIED — {verified} claims verified, {approximate} approximate, {errors} errors",
        }


def _strip_tags(html: str) -> str:
    """Remove HTML tags from a string."""
    clean = re.sub(r"<[^>]+>", " ", html)
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()


def _extract_int(text: str, label: str) -> int:
    """Extract an integer from text like 'Verified: 8'."""
    m = re.search(rf"{label}:\s*(\d+)", text, re.IGNORECASE)
    return int(m.group(1)) if m else 0
