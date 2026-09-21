import time
from functools import wraps
from pathlib import Path


def retry(attempts, delay, exceptions=None):
    if attempts < 1 or delay < 0:
        raise ValueError("Неверное число попыток или задержка")
    errors = (Exception,) if exceptions is None else tuple(exceptions)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for number in range(attempts):
                try:
                    return func(*args, **kwargs)
                except errors:
                    if number == attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


def demo(attempts, delay):
    calls = 0

    @retry(attempts, delay, [ValueError])
    def unstable():
        nonlocal calls
        calls += 1
        print("Попытка", calls)
        if calls < 3:
            raise ValueError("Временная ошибка")
        return "Успех"

    return unstable()


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    values = (path / "txt/input.txt").read_text().split()
    print(demo(int(values[0]), float(values[1])))
