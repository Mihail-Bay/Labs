from functools import wraps
from time import perf_counter
from pathlib import Path


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Функция: {func.__name__}")
        print(f"Аргументы: {args}, {kwargs}")
        start = perf_counter()
        try:
            result = func(*args, **kwargs)
            print(f"Результат: {result}")
            return result
        finally:
            elapsed = perf_counter() - start
            print(f"Время: {elapsed:.6f} с")
    return wrapper


@logger
def add(a, b):
    return a + b


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    text = (path / "txt/input.txt").read_text(encoding="utf-8")
    a, b = map(int, text.split())
    add(a, b)
