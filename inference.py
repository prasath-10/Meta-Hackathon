import asyncio
import os
from typing import List, Optional

from openai import OpenAI


API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    err = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


def choose_action_with_model(client: OpenAI) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are solving a simple incident response environment. "
                        "Choose exactly one action string. "
                        "Available actions: restart_service, inspect_logs"
                    ),
                },
                {
                    "role": "user",
                    "content": "The service appears down. Return exactly one action string."
                },
            ],
            temperature=0,
            max_tokens=20,
        )
        text = (response.choices[0].message.content or "").strip()
        return text if text in {"restart_service", "inspect_logs"} else "restart_service"
    except Exception:
        return "restart_service"


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

    # Minimal local HTTP fallback style for your current environment
    # since your environment is served as an API endpoint.
    import requests

    base_env_url = "http://127.0.0.1:8000"
    task_name = "easy"
    benchmark = "incident-response-openenv"

    rewards: List[float] = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start(task=task_name, env=benchmark, model=MODEL_NAME)

    try:
        reset_resp = requests.post(f"{base_env_url}/reset", timeout=30)
        reset_resp.raise_for_status()
        result = reset_resp.json()
        done = result.get("done", False)

        for step in range(1, 4):
            if done:
                break

            action = choose_action_with_model(client)

            step_resp = requests.post(
                f"{base_env_url}/step",
                json={"action": action},
                timeout=30,
            )
            step_resp.raise_for_status()
            step_result = step_resp.json()

            reward = float(step_result.get("reward", 0.0))
            done = bool(step_result.get("done", False))
            info = step_result.get("info", {}) or {}
            error = info.get("last_action_error")

            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=action,
                reward=reward,
                done=done,
                error=error,
            )

            if done:
                break

        score = 1.0 if done else 0.0
        success = done

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())