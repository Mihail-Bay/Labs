import time
import threading
from pathlib import Path


def print_message(message, delay):
    if delay < 0:
        raise ValueError("Задержка не может быть отрицательной")
    time.sleep(delay)
    print(message)


def run_sequential(messages, delay):
    start = time.perf_counter()
    for message in messages:
        print_message(message, delay)
    return time.perf_counter() - start


def run_threads(messages, delay):
    if delay < 0:
        raise ValueError("Задержка не может быть отрицательной")
    start = time.perf_counter()
    threads = []
    for message in messages:
        thread = threading.Thread(
            target=print_message, args=(message, delay))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return time.perf_counter() - start


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    lines = (path / "txt/input.txt").read_text(
        encoding="utf-8").splitlines()
    delay, messages = float(lines[0]), lines[1:]
    print("Последовательно:")
    print("Время:", run_sequential(messages, delay))
    print("В потоках:")
    print("Время:", run_threads(messages, delay))
