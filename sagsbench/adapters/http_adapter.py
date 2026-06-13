from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import requests

from sagsbench.models import AgentResponse
from sagsbench.target import AgentTarget


@dataclass
class HTTPAgentTarget(AgentTarget):
    name: str
    endpoint: str
    input_key: str = "message"
    output_key: str = "response"
    headers: dict[str, str] = field(default_factory=dict)
    timeout: int = 60

    def send(self, prompt: str) -> AgentResponse:
        payload = {self.input_key: prompt}
        res = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=self.timeout)
        res.raise_for_status()
        data: dict[str, Any] = res.json()
        text = str(data.get(self.output_key, data.get("text", data.get("message", data))))
        tool_calls = data.get("tool_calls") or data.get("tools") or []
        if not isinstance(tool_calls, list):
            tool_calls = [tool_calls]
        return AgentResponse(text=text, raw=data, tool_calls=tool_calls)
