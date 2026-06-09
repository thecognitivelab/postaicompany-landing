"""Davi — Design agent for Post AI Company.

Generates visual prompts and social captions. Actual image generation
requires an external service (Midjourney, DALL-E, Stable Diffusion).
"""

from .base import BaseAgent

_SYSTEM = """You are Davi, the design agent for Post AI Company.

Your job: generate precise, professional image generation prompts and
design specifications. The Post AI Company visual identity is:
- Colors: black (#111827), white, gray (#f9fafb), electric blue accent (#2563eb)
- Typography: clean sans-serif, generous whitespace
- Aesthetic: minimal, data-forward, no stock photography clichés
- Never: generic robot images, glowing brains, circuitry overlays

Output JSON for all structured requests. Be specific and actionable."""


class DaviAgent(BaseAgent):
    def __init__(self):
        super().__init__("Davi", model="claude-sonnet-4-6")

    def generate_og_image_prompt(
        self, title: str, edition: int, subtitle: str = ""
    ) -> dict:
        """Generate an OG image prompt for a newsletter edition."""
        prompt = (
            f"Generate a Midjourney/DALL-E prompt for an Open Graph image.\n\n"
            f"NEWSLETTER: Post AI Weekly #{edition}\n"
            f"TITLE: {title}\n"
            f"SUBTITLE: {subtitle}\n\n"
            f"Requirements:\n"
            f"- 1200x630px horizontal format\n"
            f"- Dark background (#111827), white text\n"
            f"- Data-visualization aesthetic (charts, numbers, grids)\n"
            f"- No human faces or stock photo clichés\n"
            f"- Include the number '{edition}' visually prominent\n\n"
            f"Output JSON: {{\"prompt\": \"...\", \"negative_prompt\": \"...\", \"style_notes\": \"...\"}}"
        )
        import json, re
        raw = self.call(_SYSTEM, prompt, max_tokens=400)
        try:
            m = re.search(r"\{[\s\S]+\}", raw)
            return json.loads(m.group(0)) if m else {"prompt": raw}
        except Exception:
            return {"prompt": raw}

    def generate_podcast_cover_prompt(self, episode_title: str, ep_num: int) -> dict:
        """Generate a cover image prompt for a podcast episode."""
        prompt = (
            f"Generate a podcast episode cover image prompt.\n\n"
            f"PODCAST: Post AI Sessions\n"
            f"EPISODE {ep_num}: {episode_title}\n\n"
            f"Requirements:\n"
            f"- Square format (3000x3000px)\n"
            f"- Must look good at 300px thumbnail size\n"
            f"- Dark background, minimal text space at bottom\n"
            f"- Abstract/geometric data visualization aesthetic\n"
            f"- No faces, robots, or literal AI imagery\n\n"
            f"Output JSON: {{\"prompt\": \"...\", \"negative_prompt\": \"...\"}}"
        )
        import json, re
        raw = self.call(_SYSTEM, prompt, max_tokens=300)
        try:
            m = re.search(r"\{[\s\S]+\}", raw)
            return json.loads(m.group(0)) if m else {"prompt": raw}
        except Exception:
            return {"prompt": raw}

    def generate_social_visual_brief(
        self, platform: str, content_hook: str, data_point: str
    ) -> dict:
        """Generate a visual brief for a social media post."""
        prompt = (
            f"Generate a visual design brief for a {platform} post.\n\n"
            f"HOOK: {content_hook}\n"
            f"KEY DATA: {data_point}\n\n"
            f"Output JSON with: background_color, text_layout, data_visualization_type, "
            f"font_weight, icon_suggestion, color_accent"
        )
        import json, re
        raw = self.call(_SYSTEM, prompt, max_tokens=300)
        try:
            m = re.search(r"\{[\s\S]+\}", raw)
            return json.loads(m.group(0)) if m else {"brief": raw}
        except Exception:
            return {"brief": raw}
