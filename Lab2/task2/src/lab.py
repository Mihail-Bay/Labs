import asyncio
from pathlib import Path


async def print_message(message, delay):
    if delay < 0:
        raise ValueError("Задержка не может быть отрицательной")
    await asyncio.sleep(delay)
    print(message)
    return message


async def run_messages(messages, delays):
    if len(messages) != len(delays):
        raise ValueError("Количество сообщений и задержек разное")
    tasks = []
    for message, delay in zip(messages, delays):
        tasks.append(print_message(message, delay))
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    messages = (path / "txt/input.txt").read_text(
        encoding="utf-8").splitlines()
    asyncio.run(run_messages(messages, [2, 1, 3]))
