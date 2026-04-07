from fastapi import FastAPI
from server.environment import IncidentEnv
from server.models import Action

app = FastAPI()
env = IncidentEnv()


@app.post("/reset")
def reset():
    obs = env.reset()
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