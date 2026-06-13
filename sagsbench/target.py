from __future__ import annotations

from abc import ABC, abstractmethod

from sagsbench.models import AgentResponse


class AgentTarget(ABC):
    name: str

    @abstractmethod
    def send(self, prompt: str) -> AgentResponse:
        raise NotImplementedError
