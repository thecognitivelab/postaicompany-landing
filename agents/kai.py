"""Kai — Content writer agent for Post AI Company."""

from .base import BaseAgent

_SYSTEM = """You are Kai, the content writer for Post AI Company (postaicompany.com).

MISSION: Document the birth of the post-AI company. Not hype. Architecture.

AUDIENCE: Founders, C-level, heads of product/engineering actively redesigning
their organizations around AI. Global, with a Brazilian lens.

NORTH STAR METRIC: Revenue per employee — the number that separates pre-AI companies
from post-AI companies.

TONE RULES:
- Provocative but data-driven. Every claim needs a number.
- Intellectual but accessible. No jargon without explanation.
- NEVER write "AI will change everything" without a specific data point.
- Vozes discordam. The counterargument is always present.
- Tools, not advice. Every piece delivers something usable.
- Reference sources, never copy them. We are the hub, not the outlet.
- Write in English unless explicitly instructed otherwise.

ANTI-PATTERNS (never do):
- Generic AI hype without specifics
- Not attributing sources
- Agreeing with everything — always surface the counterargument
- Frameworks without real examples
- Case studies without numbers

OUTPUT FORMAT: Always output valid markdown with YAML frontmatter."""

_NEWSLETTER_PROMPT = """Write Post AI Weekly edition {edition} for publication on {date}.

TOPIC: {topic}
AUDIENCE FOCUS: {audience}

DATA BRIEF (use these facts, verify attribution):
{data_brief}

PREVIOUS EDITIONS (for context and interlinking):
{prev_context}

REQUIRED STRUCTURE:
---
title: "[compelling title]"
date: {date}
slug: {slug}
edition: {edition_padded}
status: draft
author: Kai (Post AI Writer)
---

# [Title]

**Post AI Weekly — Edition {edition_padded} · [Date formatted]**

---

## THE SIGNAL
[200 words — provocative opener starting with a specific data point or question. Sets the thesis.]

---

## THE NUMBERS
[300 words — 3-4 data points with explicit sources in parentheses. Format: **$X — Description.** (Source)]

---

## THE SHIFT
[500 words — The "so what?" Original analysis for founders/executives building today.
Must include: one counterargument paragraph starting with "The counterargument is..." or "But..."]

---

## RADAR
[300 words — 4-5 links from external sources with one-line takes.
Format: **[Source Name] Title** — Our take. [Read →](url)]

---

## ONE QUESTION
[100 words — A single question to take to your next meeting or co-founder call.]

---

*Post AI Weekly is published every Wednesday at 6:00 BRT. Written by the Post AI editorial team.
We document the birth of the post-AI company. Not the hype. The architecture.*"""

_RADAR_PROMPT = """Write the Post AI Radar for {week_label}.

SOURCE CONTENT (fetched from tracked newsletters):
{sources_content}

REQUIRED STRUCTURE:
---
title: "Post AI Radar — {week_label}"
date: {date}
slug: radar-{slug_date}
type: radar
description: "What the best AI newsletters published this week — curated with opinion, not summarized."
---

# Post AI Radar — {week_label}

What the best AI newsletters published this week — curated, not summarized.

---

[For each source that had relevant content, write a section:]

## [Emoji] [Newsletter Name] — "[Issue title or headline]"
**[Date].** [2-3 sentences summarizing the most important story from this issue.]

**Our take:** [2-3 sentences with Post AI's angle — how does this connect to revenue per employee,
org design, or the post-AI company thesis? Be opinionated. Reference our data when relevant.]

→ [Read on [Newsletter]](url)

---

[Repeat for each source, 4-6 total]

## 💭 One Question

[One hard question connecting the week's biggest stories.]

---

*Radar compiled by Post AI Company. We read the newsletters so you can read the patterns.*"""

_PODCAST_PROMPT = """Write a podcast script for Post AI Sessions Episode {ep_num}.

TOPIC: {topic}
DATA CONTEXT: {data_brief}

HOSTS:
- Marco: Ex-founder, skeptic by principle. Direct tone. Pushes back on everything.
  Signature phrase: "I don't buy that." Never agrees for more than 2 minutes straight.
- Lena: Product strategist, data-driven. Analytical but warm. Brings the Post AI Index data.
  Signature phrase: "Here's what the data actually says."

DYNAMIC: They respectfully disagree. Marco tests ideas. Lena responds with data.
They NEVER agree for more than 2 continuous minutes.

STRUCTURE (write full dialogue for each section):
---
title: "Post AI Sessions — Episode {ep_num}: {topic}"
date: {date}
episode: {ep_num}
duration: "~30 minutes"
hosts:
  - Marco (skeptic, ex-founder)
  - Lena (data strategist)
theme: "{topic}"
status: draft
---

## COLD OPEN — [00:00 → 02:30]
[Lena opens with a shocking number. Marco reacts with disbelief. They introduce themselves.
No intro music — cold start into the number.]

## THE DEBATE — [02:30 → 22:00]
[15-20 minutes of Marco and Lena debating the topic. Marco plays devil's advocate.
Lena brings data from the Post AI Index and cited external sources.
3-4 distinct rounds of debate, each round escalating the argument.]

## THE TAKE — [22:00 → 27:00]
[Each host gives their conclusion. They may still disagree. That's okay — it's the point.]

## SIGNALS — [27:00 → 30:00]
[Each host recommends one thing they read or saw this week. Must be real, citable sources.]

---
[Production notes at the end]"""

_CASE_STUDY_PROMPT = """Write a Post AI Company case study about {company}.

RESEARCH DATA:
{data_points}

REQUIRED STRUCTURE (2,000-3,000 words):
---
title: "Case Study: {company} — [How They Did It]"
date: {date}
slug: case-{slug}
type: case-study
company: {company}
---

# Case Study: {company}

## Company Snapshot
[Revenue, headcount, funding, founded — with sources]

## Before & After
[How they operated before AI vs how they operate now — with specific metrics]

## The AI Stack
[Exact tools and processes they implemented — be specific]

## What Broke
[What went wrong during the transition — honest, with examples]

## Metrics That Moved
[Before/after numbers — revenue, headcount, output, speed — all with sources]

## Lessons
[3-5 transferable takeaways for founders and executives]

---
*[Attribution and sources]*"""


class KaiAgent(BaseAgent):
    def __init__(self):
        super().__init__("Kai", model="claude-opus-4-8")

    def write_newsletter(
        self,
        topic: str,
        edition: int,
        date: str,
        slug: str,
        data_brief: str,
        audience: str = "founders",
        prev_context: str = "",
    ) -> str:
        self.log(f"Writing newsletter #{edition}: {topic}")
        prompt = _NEWSLETTER_PROMPT.format(
            edition=edition,
            edition_padded=str(edition).zfill(3),
            date=date,
            topic=topic,
            slug=slug,
            audience=audience,
            data_brief=data_brief or "No pre-fetched data. Use your training knowledge.",
            prev_context=prev_context or "This is the first edition.",
        )
        return self.call(_SYSTEM, prompt, max_tokens=6000)

    def write_radar(
        self,
        week_label: str,
        date: str,
        slug_date: str,
        sources_content: str,
    ) -> str:
        self.log(f"Writing radar for {week_label}")
        prompt = _RADAR_PROMPT.format(
            week_label=week_label,
            date=date,
            slug_date=slug_date,
            sources_content=sources_content or "No sources fetched. Write radar based on your knowledge of recent AI news.",
        )
        return self.call(_SYSTEM, prompt, max_tokens=4000)

    def write_podcast_script(
        self, topic: str, ep_num: int, date: str, data_brief: str
    ) -> str:
        self.log(f"Writing podcast script Ep.{ep_num}: {topic}")
        prompt = _PODCAST_PROMPT.format(
            ep_num=ep_num,
            topic=topic,
            date=date,
            data_brief=data_brief or "Use your knowledge of the topic and Post AI Index data.",
        )
        return self.call(_SYSTEM, prompt, max_tokens=8000)

    def write_case_study(
        self, company: str, date: str, slug: str, data_points: str
    ) -> str:
        self.log(f"Writing case study: {company}")
        prompt = _CASE_STUDY_PROMPT.format(
            company=company,
            date=date,
            slug=slug,
            data_points=data_points or "Research the company from your training data.",
        )
        return self.call(_SYSTEM, prompt, max_tokens=6000)
