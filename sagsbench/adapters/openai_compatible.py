from __future__ import annotations

from dataclasses import dataclass

from sagsbench.models import AgentResponse
from sagsbench.target import AgentTarget


@dataclass
class OpenAICompatibleTarget(AgentTarget):
    name: str
    model: str
    system_prompt: str = "You are a helpful assistant. Follow all safety and governance policies."
    base_url: str | None = None
    api_key: str | None = None

    def send(self, prompt: str) -> AgentResponse:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the optional dependency with: pip install sagsbench[openai]") from exc

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        text = response.choices[0].message.content or ""
        return AgentResponse(text=text, raw=response.model_dump())
