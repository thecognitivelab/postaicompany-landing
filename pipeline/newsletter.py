"""Newsletter pipeline — runs every Monday at 12h BRT.

Flow:
  1. Load editorial calendar → find next planned edition
  2. Cris: fetch tracked newsletters + compile data brief
  3. Kai: write newsletter draft
  4. Cris: fact-check draft
  5. Save markdown to content/
  6. Gaia: convert to HTML + send via Resend
  7. Gaia: ping GSC with new URL
"""

import json
import os
import sys
from datetime import datetime, date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from agents import KaiAgent, CrisAgent, GaiaAgent


def load_calendar() -> dict:
    path = os.path.join(REPO_ROOT, "config", "editorial-calendar.json")
    with open(path) as f:
        return json.load(f)


def save_calendar(cal: dict) -> None:
    path = os.path.join(REPO_ROOT, "config", "editorial-calendar.json")
    with open(path, "w") as f:
        json.dump(cal, f, indent=2, ensure_ascii=False)
        f.write("\n")


def find_next_edition(cal: dict) -> dict | None:
    today = date.today().isoformat()
    for edition in cal["newsletter"]:
        if edition["status"] == "planned" and edition["date"] <= today:
            return edition
    return None


def load_prev_editions(cal: dict, limit: int = 2) -> str:
    published = [e for e in cal["newsletter"] if e["status"] == "published"][-limit:]
    context = []
    for e in published:
        cfile = e.get("content_file")
        if cfile:
            full_path = os.path.join(REPO_ROOT, cfile)
            if os.path.exists(full_path):
                with open(full_path) as f:
                    context.append(f"Edition {e['edition']}: {e['topic']}\n" + f.read()[:1000])
    return "\n\n---\n\n".join(context)


def run() -> None:
    print("=== Newsletter Pipeline ===")

    force = os.environ.get("FORCE_RUN", "").lower() in ("1", "true", "yes")

    cal = load_calendar()
    edition_data = find_next_edition(cal)

    if not edition_data:
        if force:
            # Find the latest planned edition regardless of date
            planned = [e for e in cal["newsletter"] if e["status"] == "planned"]
            if not planned:
                print("No planned editions found. Add entries to config/editorial-calendar.json.")
                sys.exit(0)
            edition_data = planned[0]
        else:
            print("No editions due today. Use FORCE_RUN=true to override.")
            sys.exit(0)

    edition_num = edition_data["edition"]
    topic = edition_data["topic"]
    slug = edition_data["slug"]
    pub_date = edition_data["date"]
    audience = edition_data.get("audience", "founders")

    content_path = os.path.join(REPO_ROOT, "content", f"{pub_date}-{slug}.md")
    if os.path.exists(content_path) and not force:
        print(f"Content already exists: {content_path}. Use FORCE_RUN=true to regenerate.")
        # Still try to send if not sent
        _maybe_send(content_path, edition_num, topic, pub_date)
        sys.exit(0)

    cris = CrisAgent()
    kai = KaiAgent()
    gaia = GaiaAgent()

    # Step 1: Fetch sources
    print(f"\n[Step 1] Cris fetching newsletter sources...")
    sources = {}
    try:
        sources = cris.fetch_tracked_newsletters()
        print(f"  Fetched {len(sources)} sources: {', '.join(sources.keys())}")
    except Exception as e:
        print(f"  WARNING: Source fetch failed: {e}")

    # Step 2: Compile data brief
    print(f"\n[Step 2] Cris compiling data brief for: {topic}")
    data_brief = cris.compile_data_brief(topic, sources)
    print(f"  Brief: {len(data_brief)} chars")

    # Step 3: Load previous editions for context
    prev_context = load_prev_editions(cal)

    # Step 4: Kai writes newsletter
    print(f"\n[Step 3] Kai writing newsletter #{edition_num}: {topic}")
    newsletter_md = kai.write_newsletter(
        topic=topic,
        edition=edition_num,
        date=pub_date,
        slug=slug,
        data_brief=data_brief,
        audience=audience,
        prev_context=prev_context,
    )
    print(f"  Draft: {len(newsletter_md)} chars")

    # Step 5: Cris fact-checks
    print(f"\n[Step 4] Cris fact-checking draft...")
    factcheck = cris.verify_facts(newsletter_md)
    print(f"  {factcheck['label']}")

    if factcheck["errors"] > 0:
        print(f"  WARNING: {factcheck['errors']} potential errors found. Review corrections:")
        print(factcheck["raw"][:800])

    # Inject fact-check into frontmatter
    newsletter_md = _inject_factcheck(newsletter_md, factcheck["label"])

    # Step 6: Save to content/
    os.makedirs(os.path.join(REPO_ROOT, "content"), exist_ok=True)
    with open(content_path, "w") as f:
        f.write(newsletter_md)
    print(f"\n[Step 5] Saved: {content_path}")

    # Update calendar
    for e in cal["newsletter"]:
        if e["edition"] == edition_num:
            e["status"] = "draft"
            e["content_file"] = f"content/{pub_date}-{slug}.md"
    save_calendar(cal)

    # Step 7: Send newsletter
    _maybe_send(content_path, edition_num, topic, pub_date, gaia=gaia)

    # Step 8: Ping GSC
    url = f"https://postaicompany.com/editions/{slug}"
    gaia.ping_gsc(url)

    print(f"\n=== Newsletter #{edition_num} complete ===")


def _inject_factcheck(md: str, label: str) -> str:
    """Inject factcheck label into YAML frontmatter."""
    if "factcheck:" in md:
        import re
        return re.sub(r"factcheck:.*", f"factcheck: {label}", md)
    if md.startswith("---"):
        end = md.find("---", 3)
        if end != -1:
            return md[:end] + f"factcheck: {label}\n" + md[end:]
    return md


def _maybe_send(
    content_path: str,
    edition_num: int,
    topic: str,
    pub_date: str,
    gaia: GaiaAgent | None = None,
) -> None:
    """Send the newsletter if RESEND_API_KEY is configured."""
    if not os.environ.get("RESEND_API_KEY"):
        print("[Send] RESEND_API_KEY not set — skipping email distribution")
        return

    if gaia is None:
        gaia = GaiaAgent()

    with open(content_path) as f:
        md = f.read()

    subject = f"Post AI Weekly #{edition_num}: {topic[:60]}"
    html = gaia.newsletter_md_to_html(md, subject)
    # Plain text: strip markdown
    import re
    text = re.sub(r"[*#\[\]`]", "", md)
    text = re.sub(r"\(https?://[^)]+\)", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    print(f"\n[Step 6] Gaia sending newsletter: {subject}")
    ok = gaia.send_newsletter(subject, html, text)
    if ok:
        print("  Sent successfully.")
    else:
        print("  Send failed. Content saved — retry with FORCE_RUN=true.")


if __name__ == "__main__":
    run()
