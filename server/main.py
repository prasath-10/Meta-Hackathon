from fastapi import FastAPI, Body
from server.environment import IncidentEnv
from server.models import Action

app = FastAPI()
env = IncidentEnv()

@app.get("/")
def root():
    return {"message": "Incident Response OpenEnv is running"}

from fastapi import Request

@app.post("/reset")
async def reset(request: Request):
    try:
        payload = await request.json()
    except Exception:
        payload = {}
    
    if not isinstance(payload, dict):
        payload = {}
        
    task_name = payload.get("task_name", "easy")
    obs = env.reset(task_name=task_name)
    return {
        "observation": obs,
        "done": False
    }

@app.post("/step")
def step(action: Action):
    return env.step(action)

@app.get("/state")
def state():
    return env.state