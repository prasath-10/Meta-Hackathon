from fastapi import FastAPI, Query
from server.environment import IncidentEnv
from server.models import Action

app = FastAPI()
env = IncidentEnv()

@app.get("/")
def root():
    return {"message": "Incident Response OpenEnv is running"}

@app.post("/reset")
def reset(task_name: str = Query(default="easy")):
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