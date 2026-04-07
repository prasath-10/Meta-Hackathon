def grade(env_state):
    if env_state.get("resolved"):
        return 1.0
    return 0.0