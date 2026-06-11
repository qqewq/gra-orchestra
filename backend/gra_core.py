import numpy as np
from typing import List, Dict
from models import AgentState

class GRAOrchestra:
    """
    GRA-Core: иерархическая стабилизация роя.
    Принцип: оркестр обнуляет глобальную пену, но поощряет локальную пену агентов.
    """
    def __init__(self):
        self.agents: Dict[str, AgentState] = {}
        self.global_pena = 0.0
        self.delta_global = 0.0
        self.delta2_global = 0.0

    def add_agent(self, agent_id: str, character: Dict[str, float]):
        self.agents[agent_id] = AgentState(
            id=agent_id,
            local_pena=0.5,  # начальная локальная пена (характер)
            align_error=0.0,
            is_connected=True,
            character=character
        )
        self._recompute_global_pena()

    def remove_agent(self, agent_id: str):
        if agent_id in self.agents:
            self.agents[agent_id].is_connected = False
            self._recompute_global_pena()

    def connect_agent(self, agent_id: str, threshold: float = 1.0):
        if agent_id in self.agents:
            self.agents[agent_id].is_connected = True
            # при подключении возможно изменение локальной пены в пределах порога
            self.agents[agent_id].local_pena = min(self.agents[agent_id].local_pena, threshold)
            self._recompute_global_pena()

    def _recompute_global_pena(self):
        """Глобальная пена = сумма квадратов align_error + конфликт характеров"""
        connected = [a for a in self.agents.values() if a.is_connected]
        if not connected:
            self.global_pena = 0.0
            self.delta_global = 0.0
            self.delta2_global = 1.0
            return

        # 1. Ошибки выравнивания
        align_sum = sum(a.align_error ** 2 for a in connected)

        # 2. Конфликт характеров (простейшая мера: дисперсия первых двух компонент)
        chars = np.array([list(a.character.values())[:2] for a in connected if a.character])
        if len(chars) > 1:
            conflict = np.var(chars, axis=0).sum()
        else:
            conflict = 0.0

        self.global_pena = align_sum + 0.5 * conflict

        # Для демонстрации: вычисляем конечные разности (имитация истории)
        # В реальном GRA-Core тут был бы итерационный шаг
        self.delta_global = self.global_pena - getattr(self, '_prev_pena', 0.0)
        self.delta2_global = self.delta_global - getattr(self, '_prev_delta', 0.0)
        self._prev_pena = self.global_pena
        self._prev_delta = self.delta_global

    def step(self, steps: int = 1):
        """Выполняет GRA-шаги: уменьшает глобальную пену, сохраняя локальную > 0."""
        for _ in range(steps):
            for agent in self.agents.values():
                if not agent.is_connected:
                    continue
                # Уменьшаем ошибку выравнивания, но не трогаем локальную пену
                agent.align_error = max(0.0, agent.align_error - 0.1 * agent.align_error)
                # Локальная пена сохраняется (даже случайно колеблется, но >0)
                agent.local_pena = max(0.1, min(agent.local_pena + np.random.normal(0, 0.02), 2.0))
            self._recompute_global_pena()

    def get_state(self):
        return {
            "global_pena": self.global_pena,
            "delta_global": self.delta_global,
            "delta2_global": self.delta2_global,
            "is_stable": abs(self.global_pena) < 0.01 and abs(self.delta_global) < 0.01 and self.delta2_global > 0,
            "agents": [a.dict() for a in self.agents.values()]
        }
