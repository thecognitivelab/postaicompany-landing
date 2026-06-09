"""Weekly report pipeline — runs every Friday at 10h BRT.

Compiles:
  - Newsletter subscriber count (Resend)
  - Published content count (filesystem)
  - Clips generated (filesystem)
  - D-ID credits remaining
  - A one-paragraph summary from Cris
"""

import json
import os
import sys
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from agents import CrisAgent, GaiaAgent


def count_content_files() -> dict:
    content_dir = os.path.join(REPO_ROOT, "content")
    if not os.path.exists(content_dir):
        return {"newsletters": 0, "radars": 0, "podcasts": 0, "total": 0}
    files = os.listdir(content_dir)
    newsletters = [f for f in files if "radar" not in f and "podcast" not in f and f.endswith(".md")]
    radars = [f for f in files if "radar" in f and f.endswith(".md")]
    podcasts = [f for f in files if "podcast" in f and f.endswith(".md")]
    return {
        "newsletters": len(newsletters),
        "radars": len(radars),
        "podcasts": len(podcasts),
        "total": len(files),
    }


def count_clips() -> int:
    clips_dir = os.path.join(REPO_ROOT, "clips")
    if not os.path.exists(clips_dir):
        return 0
    return len([f for f in os.listdir(clips_dir) if f.endswith(".mp4")])


def get_did_credits() -> str:
    """Try to fetch D-ID credits remaining."""
    did_config = os.environ.get("D_ID_AUTH_FILE", os.path.expanduser("~/.d-id-auth"))
    d_id_auth = os.environ.get("D_ID_AUTH", "")

    if not os.path.exists(did_config) and not d_id_auth:
        return "N/A (D-ID not configured)"

    try:
        import urllib.request
        token = ""
        if os.path.exists(did_config):
            with open(did_config) as f:
                token = f.read().strip()
        else:
            token = d_id_auth

        req = urllib.request.Request(
            "https://api.d-id.com/credits",
            headers={"Authorization": f"Basic {token}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            remaining = data.get("remaining", "?")
            total = data.get("total", "?")
            return f"{remaining}/{total}"
    except Exception as e:
        return f"Error: {e}"


def run() -> None:
    print("=== Weekly Report Pipeline ===")

    now = datetime.utcnow()
    week_num = now.isocalendar()[1]
    report_date = now.strftime("%Y-%m-%d")
    report_week = f"Week {week_num}, {now.strftime('%B %Y')}"

    gaia = GaiaAgent()
    cris = CrisAgent()

    # Gather metrics
    print(f"\n[Step 1] Gathering metrics for {report_week}...")

    subscriber_count = gaia.get_subscriber_count()
    content_counts = count_content_files()
    clip_count = count_clips()
    did_credits = get_did_credits()

    cal_path = os.path.join(REPO_ROOT, "config", "editorial-calendar.json")
    with open(cal_path) as f:
        cal = json.load(f)
    published_editions = len([e for e in cal.get("newsletter", []) if e["status"] == "published"])
    published_podcasts = len([e for e in cal.get("podcast", []) if e["status"] == "published"])

    metrics = {
        "date": report_date,
        "week": report_week,
        "subscribers": subscriber_count or "N/A",
        "newsletter_editions_published": published_editions,
        "podcast_episodes_published": published_podcasts,
        "radar_posts": len(cal.get("radar", [])),
        "clips_generated": clip_count,
        "d_id_credits": did_credits,
        "content_files_total": content_counts["total"],
    }

    print(f"  Subscribers: {metrics['subscribers']}")
    print(f"  Newsletter editions: {metrics['newsletter_editions_published']}")
    print(f"  Podcast episodes: {metrics['podcast_episodes_published']}")
    print(f"  Radar posts: {metrics['radar_posts']}")
    print(f"  Clips generated: {metrics['clips_generated']}")
    print(f"  D-ID credits: {metrics['d_id_credits']}")

    # Step 2: Cris writes summary
    print(f"\n[Step 2] Cris compiling weekly summary...")
    summary_prompt = f"""Write a terse weekly operations report for Post AI Company.

METRICS THIS WEEK:
{json.dumps(metrics, indent=2)}

Format as a short markdown report with:
- One paragraph summary (what's going well, what needs attention)
- A bulleted metrics table
- One priority action for next week

Be direct. No filler. Under 300 words."""

    summary = cris.call(
        "You are Cris, the data analyst for Post AI Company. Write a concise weekly report.",
        summary_prompt,
        max_tokens=600,
    )

    # Step 3: Save report
    reports_dir = os.path.join(REPO_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, f"{report_date}-weekly-report.md")

    report_content = f"""---
date: {report_date}
week: "{report_week}"
type: weekly-report
---

# Weekly Report — {report_week}

{summary}

---

## Raw Metrics

```json
{json.dumps(metrics, indent=2)}
```

*Generated automatically by Cris on {now.strftime('%Y-%m-%d %H:%M UTC')}*
"""

    with open(report_path, "w") as f:
        f.write(report_content)

    print(f"\n[Step 3] Report saved: {report_path}")
    print(f"\n=== Weekly report complete ===")
    print(f"\n--- REPORT SUMMARY ---")
    print(summary)


if __name__ == "__main__":
    run()
