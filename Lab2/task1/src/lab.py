import asyncio
from pathlib import Path


async def print_message(message, delay):
    if delay < 0:
        raise ValueError("Задержка не может быть отрицательной")
    await asyncio.sleep(delay)
    print(message)
    return message


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    lines = (path / "txt/input.txt").read_text(
        encoding="utf-8").splitlines()
    asyncio.run(print_message(lines[1], float(lines[0])))
