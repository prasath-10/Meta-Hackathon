from pydantic import BaseModel
from typing import List


class Observation(BaseModel):
    alerts: List[str]
    cpu: int
    memory: int
    logs: str
    service_status: str


class Action(BaseModel):
    action: str