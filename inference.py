import requests

BASE_URL = "http://127.0.0.1:8000"

print("[START] task=easy env=incident model=baseline")

res = requests.post(f"{BASE_URL}/reset")
data = res.json()

rewards = []
steps = 0

for i in range(3):
    action = {"action": "restart_service"}
    r = requests.post(f"{BASE_URL}/step", json=action).json()

    reward = r["reward"]
    done = r["done"]

    rewards.append(reward)
    steps += 1

    print(f"[STEP] step={steps} action=restart_service reward={reward:.2f} done={str(done).lower()} error=null")

    if done:
        break

score = 1.0 if done else 0.0

print(f"[END] success={str(done).lower()} steps={steps} score={score:.2f} rewards={','.join([f'{x:.2f}' for x in rewards])}")