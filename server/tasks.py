def get_easy_task():
    return {
        "root_cause": "service_down",
        "initial_state": {
            "alerts": ["service_down"],
            "cpu": 20,
            "memory": 30,
            "logs": "Service crashed unexpectedly",
            "service_status": "down"
        }
    }