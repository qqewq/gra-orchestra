from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ConnectAgentRequest, StepRequest
from gra_core import GRAOrchestra

app = FastAPI(title="GRA-Orchestra API", description="Управление роем ИИ-агентов с обнулением глобальной пены")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestra = GRAOrchestra()

# Предустановленные агенты с характерами
DEMO_AGENTS = {
    "impressionist": {"chaos": 0.9, "detail": 0.2},
    "paranoid": {"suspicion": 0.8, "accuracy": 0.9},
    "disciplined": {"speed": 0.6, "quality": 0.7},
    "rebel": {"anti_center": 0.9, "creativity": 0.8}
}

for aid, char in DEMO_AGENTS.items():
    orchestra.add_agent(aid, char)

@app.get("/state")
def get_state():
    return orchestra.get_state()

@app.post("/step")
def step(request: StepRequest):
    orchestra.step(request.steps)
    return {"status": "ok", "new_state": orchestra.get_state()}

@app.post("/connect")
def connect_agent(req: ConnectAgentRequest):
    if req.agent_id not in orchestra.agents:
        raise HTTPException(404, "Agent not found")
    orchestra.connect_agent(req.agent_id, req.local_pena_threshold)
    return {"status": "connected"}

@app.post("/disconnect/{agent_id}")
def disconnect_agent(agent_id: str):
    if agent_id not in orchestra.agents:
        raise HTTPException(404, "Agent not found")
    orchestra.remove_agent(agent_id)
    return {"status": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
