import threading
import time
from pathlib import Path

counter = 0


def increase(count, barrier=None):
    global counter
    for i in range(count):
        value = counter
        if barrier is not None:
            # Все потоки успевают прочитать старое значение.
            barrier.wait()
        time.sleep(0.001)
        counter = value + 1
        if barrier is not None:
            barrier.wait()


def run_threads(workers, count):
    global counter
    if workers < 1 or count < 0:
        raise ValueError("Неверные параметры")
    counter = 0
    barrier = threading.Barrier(workers)
    threads = []
    for i in range(workers):
        thread = threading.Thread(
            target=increase, args=(count, barrier))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return counter


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    text = (path / "txt/input.txt").read_text()
    workers, count = map(int, text.split())
    result = run_threads(workers, count)
    print("Ожидалось:", workers * count)
    print("Получилось:", result)
