from server.models import Observation, Action


class IncidentEnv:
    def __init__(self):
        self.state = None

    def reset(self):
        self.state = {
            "root_cause": "service_down",
            "cpu": 20,
            "memory": 30,
            "logs": "Service crashed",
            "service_status": "down",
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