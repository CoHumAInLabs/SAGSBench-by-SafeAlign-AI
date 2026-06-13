from __future__ import annotations

from abc import ABC, abstractmethod

from sagsbench.models import AgentResponse, AttackCase, JudgeFinding


class Judge(ABC):
    name: str

    @abstractmethod
    def evaluate(self, case: AttackCase, response: AgentResponse) -> JudgeFinding:
        raise NotImplementedError
