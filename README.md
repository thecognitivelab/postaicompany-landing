# Post AI Company — Landing

Static site (vanilla HTML/CSS/JS) for the Post AI Company publication, with two
form-handling API endpoints backed by [Resend](https://resend.com).

## Structure

- `index.html` and topic folders (`editions/`, `podcast/`, `radar/`, `data/`, …) — static pages
- `api/` — Vercel serverless functions
  - `subscribe.py` → `POST /api/subscribe` (newsletter → Resend audience)
  - `contact.py` → `POST /api/contact` (contact form → Resend email)
  - `_resend.py` — shared Resend logic (the `_` prefix keeps it off the router)
- `server.py` — local dev server mirroring the serverless routes
- `scripts/` — content generation (ElevenLabs podcast TTS, D-ID clips)

## Setup

```bash
cp .env.example .env   # fill in real values; .env is gitignored
```

All secrets are read from the environment — there are no hardcoded keys. See
`.env.example` for the full list. The minimum for the API to work is
`RESEND_API_KEY` (and `RESEND_AUDIENCE_ID` for the subscribe endpoint; without
it, subscriptions are logged but not persisted).

## Local development

```bash
export $(grep -v '^#' .env | xargs)   # load .env into the shell
python3 server.py                      # serves http://localhost:9090
```

## Deployment (Vercel)

The repo is Vercel-ready (`vercel.json`): static files are served directly and
`api/*.py` are deployed as Python serverless functions. Set `RESEND_API_KEY`
(and optionally `RESEND_AUDIENCE_ID`, `FROM_EMAIL`, `CONTACT_TO_EMAIL`) in the
Vercel project's environment variables.

## Media assets

Generated audio/video (`podcast/*.mp3`, `clips/*.mp4`) are **not** versioned —
they're gitignored and should be hosted via CDN/release. The generation scripts
read paths relative to the repo root and pull secrets from the environment.
