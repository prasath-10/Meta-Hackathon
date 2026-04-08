from server.models import Observation, Action
from server.tasks import get_easy_task


class IncidentEnv:
    def __init__(self):
        self.state = None

    def reset(self, task_name="easy"):
        if task_name == "easy":
            task_data = get_easy_task()
            self.state = {
                "root_cause": task_data["root_cause"],
                "cpu": task_data["initial_state"]["cpu"],
                "memory": task_data["initial_state"]["memory"],
                "logs": task_data["initial_state"]["logs"],
                "service_status": task_data["initial_state"]["service_status"],
                "resolved": False
            }
        else:
            self.state = {
                "root_cause": "unknown",
                "cpu": 50,
                "memory": 50,
                "logs": "Unknown issue",
                "service_status": "unknown",
                "resolved": False
            }

        return Observation(
            alerts=["service_down"],
            cpu=self.state["cpu"],
            memory=self.state["memory"],
            logs=self.state["logs"],
            service_status=self.state["service_status"]
        )

    def step(self, action: Action):
        reward = 0.0
        done = False

        if action.action == "restart_service":
            self.state["resolved"] = True
            self.state["service_status"] = "running"
            reward = 1.0
            done = True
        else:
            reward = -0.1

        observation = Observation(
            alerts=[] if self.state["resolved"] else ["service_down"],
            cpu=self.state["cpu"],
            memory=self.state["memory"],
            logs=self.state["logs"],
            service_status=self.state["service_status"]
        )

        return {
            "observation": observation,
            "reward": reward,
            "done": done,
            "info": {}
        }