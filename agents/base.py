import os
import anthropic


class BaseAgent:
    def __init__(self, name: str, model: str = "claude-opus-4-8"):
        self.name = name
        self.model = model
        self._client = None

    @property
    def client(self) -> anthropic.Anthropic:
        if self._client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY not set")
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def call(self, system: str, user: str, max_tokens: int = 8192) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return msg.content[0].text

    def log(self, message: str) -> None:
        print(f"[{self.name}] {message}")
