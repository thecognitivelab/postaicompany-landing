"""Podcast pipeline — runs every other Thursday at 09h BRT.

Flow:
  1. Load editorial calendar → find next planned podcast episode
  2. Cris: fetch relevant source material
  3. Kai: write podcast script (Marco + Lena dialogue)
  4. Save script to content/
  5. Run generate_podcast.py (ElevenLabs TTS + ffmpeg concat)
  6. Update podcast/feed.xml with new episode
"""

import json
import os
import subprocess
import sys
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from agents import KaiAgent, CrisAgent


def load_calendar() -> dict:
    path = os.path.join(REPO_ROOT, "config", "editorial-calendar.json")
    with open(path) as f:
        return json.load(f)


def save_calendar(cal: dict) -> None:
    path = os.path.join(REPO_ROOT, "config", "editorial-calendar.json")
    with open(path, "w") as f:
        json.dump(cal, f, indent=2, ensure_ascii=False)
        f.write("\n")


def find_next_episode(cal: dict) -> dict | None:
    today = datetime.utcnow().date().isoformat()
    for ep in cal.get("podcast", []):
        if ep["status"] == "planned" and ep["date"] <= today:
            return ep
    return None


def update_rss_feed(ep_num: int, topic: str, slug: str, pub_date: str, duration_s: int = 1800) -> None:
    """Insert a new <item> into podcast/feed.xml."""
    feed_path = os.path.join(REPO_ROOT, "podcast", "feed.xml")
    if not os.path.exists(feed_path):
        print(f"WARNING: RSS feed not found at {feed_path}")
        return

    dt = datetime.strptime(pub_date, "%Y-%m-%d")
    pub_rfc = dt.strftime("%a, %d %b %Y 09:00:00 -0300")
    duration_fmt = f"{duration_s // 3600:02d}:{(duration_s % 3600) // 60:02d}:{duration_s % 60:02d}"
    mp3_size = 0
    mp3_path = os.path.join(REPO_ROOT, "podcast", f"ep{ep_num}.mp3")
    if os.path.exists(mp3_path):
        mp3_size = os.path.getsize(mp3_path)

    new_item = f"""
  <item>
    <title>ep{ep_num}: {topic}</title>
    <link>https://postaicompany.com/podcast/ep{ep_num}</link>
    <guid isPermaLink="true">https://postaicompany.com/podcast/ep{ep_num}</guid>
    <pubDate>{pub_rfc}</pubDate>
    <description>{topic} — Marco and Lena debate on Post AI Sessions.</description>
    <itunes:summary>{topic} — Marco and Lena debate on Post AI Sessions.</itunes:summary>
    <itunes:duration>{duration_fmt}</itunes:duration>
    <itunes:episode>{ep_num}</itunes:episode>
    <itunes:season>1</itunes:season>
    <enclosure url="https://postaicompany.com/podcast/ep{ep_num}.mp3" length="{mp3_size}" type="audio/mpeg"/>
  </item>
"""

    with open(feed_path) as f:
        content = f.read()

    # Insert before </channel>
    if "</channel>" in content:
        content = content.replace("</channel>", new_item + "\n</channel>")
        with open(feed_path, "w") as f:
            f.write(content)
        print(f"  RSS feed updated with ep{ep_num}")
    else:
        print("  WARNING: </channel> tag not found in feed.xml")


def run() -> None:
    print("=== Podcast Pipeline ===")

    force = os.environ.get("FORCE_RUN", "").lower() in ("1", "true", "yes")

    cal = load_calendar()
    episode_data = find_next_episode(cal)

    if not episode_data:
        if force:
            planned = [e for e in cal.get("podcast", []) if e["status"] == "planned"]
            if not planned:
                print("No planned podcast episodes. Add entries to config/editorial-calendar.json.")
                sys.exit(0)
            episode_data = planned[0]
        else:
            print("No podcast episodes due today. Use FORCE_RUN=true to override.")
            sys.exit(0)

    ep_num = episode_data["episode"]
    topic = episode_data["topic"]
    slug = episode_data["slug"]
    pub_date = episode_data["date"]

    script_path = os.path.join(REPO_ROOT, "content", f"{pub_date}-podcast-ep{ep_num}.md")

    if os.path.exists(script_path) and not force:
        print(f"Script already exists: {script_path}")
    else:
        cris = CrisAgent()
        kai = KaiAgent()

        # Fetch relevant sources
        print(f"\n[Step 1] Cris fetching sources for: {topic}")
        sources = {}
        try:
            sources = cris.fetch_tracked_newsletters()
        except Exception as e:
            print(f"  WARNING: {e}")

        data_brief = ""
        if sources:
            data_brief = cris.compile_data_brief(topic, sources)

        # Write podcast script
        print(f"\n[Step 2] Kai writing podcast script Ep.{ep_num}: {topic}")
        script_md = kai.write_podcast_script(
            topic=topic,
            ep_num=ep_num,
            date=pub_date,
            data_brief=data_brief,
        )
        print(f"  Script: {len(script_md)} chars")

        os.makedirs(os.path.join(REPO_ROOT, "content"), exist_ok=True)
        with open(script_path, "w") as f:
            f.write(script_md)
        print(f"\n[Step 3] Script saved: {script_path}")

    # Update calendar
    for ep in cal.get("podcast", []):
        if ep["episode"] == ep_num:
            ep["status"] = "script_ready"
            ep["content_file"] = f"content/{pub_date}-podcast-ep{ep_num}.md"
    save_calendar(cal)

    # Generate audio if ElevenLabs key is available
    if not os.environ.get("ELEVENLABS_API_KEY"):
        print("\n[Step 4] ELEVENLABS_API_KEY not set — skipping audio generation")
        print(f"  To generate audio manually: PODCAST_SCRIPT_PATH={script_path} python scripts/generate_podcast.py")
        print(f"\n=== Podcast Ep.{ep_num} script complete ===")
        return

    print(f"\n[Step 4] Running ElevenLabs audio generation...")
    gen_script = os.path.join(REPO_ROOT, "scripts", "generate_podcast.py")
    env = os.environ.copy()
    env["PODCAST_SCRIPT_PATH"] = script_path

    result = subprocess.run(
        [sys.executable, gen_script],
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR: Audio generation failed:\n{result.stderr[:500]}")
        sys.exit(1)
    print(f"  Audio generated: {result.stdout[-200:]}")

    # Move final mp3 to podcast/epN.mp3
    ep_dir = os.path.join(REPO_ROOT, "podcast", f"ep{ep_num}")
    final_mp3 = os.path.join(ep_dir, f"ep{ep_num}-final.mp3")
    dest_mp3 = os.path.join(REPO_ROOT, "podcast", f"ep{ep_num}.mp3")

    if os.path.exists(final_mp3):
        import shutil
        shutil.copy2(final_mp3, dest_mp3)
        print(f"  Copied audio to: {dest_mp3}")

    # Update RSS feed
    print(f"\n[Step 5] Updating RSS feed...")
    update_rss_feed(ep_num, topic, slug, pub_date)

    # Mark as published
    for ep in cal.get("podcast", []):
        if ep["episode"] == ep_num:
            ep["status"] = "published"
            ep["audio_file"] = f"podcast/ep{ep_num}.mp3"
    save_calendar(cal)

    print(f"\n=== Podcast Ep.{ep_num} complete ===")


if __name__ == "__main__":
    run()
