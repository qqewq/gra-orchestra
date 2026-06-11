from pydantic import BaseModel
from typing import List, Dict, Optional

class AgentState(BaseModel):
    id: str
    local_pena: float          # Φ_i^local
    align_error: float         # Φ_i^align
    is_connected: bool
    character: Dict[str, float]  # s_i параметры (тараканы)

class OrchestraState(BaseModel):
    global_pena: float         # Φ_global
    delta_global: float        # ΔΦ_global
    delta2_global: float       # Δ²Φ_global
    is_stable: bool
    agents: List[AgentState]

class ConnectAgentRequest(BaseModel):
    agent_id: str
    local_pena_threshold: float = 1.0

class StepRequest(BaseModel):
    steps: int = 1
