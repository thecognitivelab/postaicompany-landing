"""Radar pipeline — runs every Sunday at 18h BRT.

Flow:
  1. Cris fetches all tracked newsletters via RSS
  2. Cris extracts key stories per source
  3. Kai writes the Radar post with analysis
  4. Save to content/YYYY-MM-DD-radar-week-NN.md
"""

import json
import os
import sys
from datetime import datetime, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from agents import KaiAgent, CrisAgent


def current_week_label() -> tuple[str, str, str]:
    """Returns (week_label, date_iso, slug_date) for this Sunday."""
    today = datetime.utcnow()
    week_num = today.isocalendar()[1]
    month = today.strftime("%B %Y")
    week_label = f"Week {week_num}, {month}"
    date_iso = today.strftime("%Y-%m-%d")
    slug_date = today.strftime("%Y-%m-%d")
    return week_label, date_iso, slug_date


def run() -> None:
    print("=== Radar Pipeline ===")

    force = os.environ.get("FORCE_RUN", "").lower() in ("1", "true", "yes")

    week_label, date_iso, slug_date = current_week_label()
    output_path = os.path.join(REPO_ROOT, "content", f"{date_iso}-radar.md")

    if os.path.exists(output_path) and not force:
        print(f"Radar already exists for today: {output_path}")
        print("Use FORCE_RUN=true to regenerate.")
        sys.exit(0)

    cris = CrisAgent()
    kai = KaiAgent()

    # Step 1: Fetch all newsletters
    print(f"\n[Step 1] Cris fetching newsletters for {week_label}...")
    raw_sources = {}
    try:
        raw_sources = cris.fetch_tracked_newsletters()
        print(f"  Fetched {len(raw_sources)} sources: {', '.join(raw_sources.keys())}")
    except Exception as e:
        print(f"  WARNING: Fetch failed: {e}")

    # Step 2: Extract stories per source
    print(f"\n[Step 2] Cris extracting stories per source...")
    summaries = {}
    for name, content in raw_sources.items():
        try:
            summary = cris.extract_stories(name, content)
            summaries[name] = summary
            print(f"  {name}: {len(summary)} chars extracted")
        except Exception as e:
            print(f"  WARNING: Story extraction failed for {name}: {e}")
            summaries[name] = content[:600]

    # Combine summaries for Kai
    combined = ""
    for name, summary in summaries.items():
        combined += f"\n\n=== {name} ===\n{summary}"

    # Step 3: Kai writes the Radar
    print(f"\n[Step 3] Kai writing Radar for {week_label}...")
    radar_md = kai.write_radar(
        week_label=week_label,
        date=date_iso,
        slug_date=slug_date,
        sources_content=combined,
    )
    print(f"  Draft: {len(radar_md)} chars")

    # Step 4: Save
    os.makedirs(os.path.join(REPO_ROOT, "content"), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(radar_md)
    print(f"\n[Step 4] Saved: {output_path}")

    # Update calendar
    cal_path = os.path.join(REPO_ROOT, "config", "editorial-calendar.json")
    with open(cal_path) as f:
        cal = json.load(f)
    cal.setdefault("radar", []).append({
        "date": date_iso,
        "week_label": week_label,
        "status": "published",
        "content_file": f"content/{date_iso}-radar.md",
    })
    with open(cal_path, "w") as f:
        json.dump(cal, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\n=== Radar {week_label} complete ===")


if __name__ == "__main__":
    run()
