import asyncio
from env.environment import TriageEnv


def simple_policy(patient):
    if patient["symptoms"] == "chest pain":
        return "Cardiology"
    elif patient["symptoms"] == "fever":
        return "General Medicine"
    elif patient["symptoms"] == "injury":
        return "Orthopedics"
    else:
        return "General Medicine"


async def main():
    env = TriageEnv()

    total_reward = 0
    steps = 5

    print("[START]")

    for step in range(steps):
        patient = await env.reset()
        action = simple_policy(patient)

        result, reward, done, _ = await env.step(action)

        total_reward += reward

        print("[STEP]")
        print(f"patient={patient}")
        print(f"action={action}")
        print(f"reward={reward}")
        print(f"redirected={result['redirected']}")
        print("")

    await env.close()

    # normalization
    max_reward_per_step = 4
    max_total = steps * max_reward_per_step
    final_score = total_reward / max_total

    print("[END]")
    print(f"total_reward={total_reward}")
    print(f"final_score={round(final_score, 3)}")


if __name__ == "__main__":
    asyncio.run(main())