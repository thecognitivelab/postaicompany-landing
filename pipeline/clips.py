"""Clips pipeline — runs every Wednesday at 09h BRT.

Flow:
  1. Run D-ID pipeline to create 8 avatar clips
  2. Poll until all clips are done
  3. Download finished clips to clips/
  4. Generate social copy for each clip (Gaia)
  5. Log Buffer-ready posts
"""

import json
import os
import sys
import time
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from agents import GaiaAgent

# Import clip definitions from the existing pipeline script
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
from did_pipeline import CLIPS, get_token, create_talk, check_talk


def wait_for_clip(talk_id: str, clip_id: str, max_wait: int = 300) -> str | None:
    """Poll D-ID until clip is done. Returns result_url or None."""
    start = time.time()
    interval = 10
    while time.time() - start < max_wait:
        result = check_talk(talk_id)
        status = result.get("status")
        if status == "done":
            return result.get("result_url")
        if status in ("error", "rejected"):
            print(f"  [{clip_id}] D-ID status: {status}")
            return None
        print(f"  [{clip_id}] status: {status} — waiting {interval}s...")
        time.sleep(interval)
    print(f"  [{clip_id}] Timed out after {max_wait}s")
    return None


def download_clip(url: str, dest: str) -> bool:
    """Download a clip from D-ID to the local filesystem."""
    try:
        token = get_token()
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Basic {token}"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(dest, "wb") as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"  Download failed for {url}: {e}")
        return False


def run() -> None:
    print("=== Clips Pipeline ===")

    did_config = os.environ.get("D_ID_AUTH_FILE", os.path.expanduser("~/.d-id-auth"))
    if not os.path.exists(did_config):
        # Try env var fallback
        d_id_auth = os.environ.get("D_ID_AUTH", "")
        if d_id_auth:
            os.makedirs(os.path.dirname(did_config), exist_ok=True)
            with open(did_config, "w") as f:
                f.write(d_id_auth)
        else:
            print("D-ID auth not configured. Set D_ID_AUTH_FILE or D_ID_AUTH env var.")
            sys.exit(1)

    gaia = GaiaAgent()
    clip_dir = os.path.join(REPO_ROOT, "clips")
    os.makedirs(clip_dir, exist_ok=True)

    pending = []

    # Step 1: Create all clips that don't exist yet
    print(f"\n[Step 1] Creating {len(CLIPS)} clips via D-ID...")
    for i, clip in enumerate(CLIPS):
        dest = os.path.join(clip_dir, f"{clip['id']}.mp4")
        if os.path.exists(dest):
            print(f"  [{i+1}/{len(CLIPS)}] {clip['id']}: already exists")
            continue
        try:
            print(f"  [{i+1}/{len(CLIPS)}] Creating {clip['id']}: {clip['hook'][:60]}")
            result = create_talk(clip["text"], clip["voice"])
            pending.append({
                "talk_id": result["id"],
                "clip": clip,
                "dest": dest,
            })
            print(f"    D-ID talk_id: {result['id']}")
            time.sleep(1)  # Rate limit
        except Exception as e:
            print(f"  ERROR creating {clip['id']}: {e}")

    if not pending:
        print("\nAll clips already exist.")
    else:
        # Step 2: Wait for all clips to finish
        print(f"\n[Step 2] Waiting for {len(pending)} clips to render...")
        for item in pending:
            clip = item["clip"]
            talk_id = item["talk_id"]
            dest = item["dest"]

            result_url = wait_for_clip(talk_id, clip["id"])
            if result_url:
                print(f"  Downloading {clip['id']}...")
                ok = download_clip(result_url, dest)
                if ok:
                    size_mb = os.path.getsize(dest) / 1_000_000
                    print(f"  {clip['id']} downloaded ({size_mb:.1f} MB)")
                else:
                    print(f"  Failed to download {clip['id']}")

    # Step 3: Generate social copy for each clip
    print(f"\n[Step 3] Gaia generating social copy...")
    social_posts = []
    for clip in CLIPS:
        dest = os.path.join(clip_dir, f"{clip['id']}.mp4")
        if not os.path.exists(dest):
            continue
        for platform in ["linkedin", "twitter"]:
            copy = gaia.post_social_copy(
                platform=platform,
                content=clip["text"],
                hook=clip["hook"],
            )
            social_posts.append({
                "clip_id": clip["id"],
                "platform": platform,
                "hook": clip["hook"],
                "copy": copy,
                "file": f"clips/{clip['id']}.mp4",
            })

    # Save social posts to a staging file
    staging_path = os.path.join(REPO_ROOT, "clips", "social-staging.json")
    existing = []
    if os.path.exists(staging_path):
        with open(staging_path) as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []

    # Merge new posts
    existing_ids = {(p["clip_id"], p["platform"]) for p in existing}
    new_posts = [p for p in social_posts if (p["clip_id"], p["platform"]) not in existing_ids]
    all_posts = existing + new_posts

    with open(staging_path, "w") as f:
        json.dump(all_posts, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\n[Step 4] Social staging file: {staging_path}")
    print(f"  {len(new_posts)} new posts staged for {len(CLIPS)} clips")
    print(f"\n  Ready to post:")
    for post in new_posts[:4]:
        print(f"  [{post['platform'].upper()}] {post['clip_id']}: {post['hook']}")

    print(f"\n=== Clips pipeline complete ===")
    print(f"  Download all clips from: clips/")
    print(f"  Review social copy in: clips/social-staging.json")
    print(f"  To post: add Buffer API token as BUFFER_ACCESS_TOKEN")


if __name__ == "__main__":
    run()
