from functools import wraps
from types import FunctionType
from pathlib import Path


def call_limiter(limit):
    if limit < 0:
        raise ValueError("Лимит не может быть отрицательным")

    def decorate(cls):
        def wrap_method(func):
            # У каждого метода свой счетчик на весь класс.
            calls = 0

            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal calls
                if calls >= limit:
                    raise RuntimeError("Лимит метода исчерпан")
                calls += 1
                return func(*args, **kwargs)
            return wrapper

        for name, method in list(vars(cls).items()):
            if isinstance(method, staticmethod):
                method = staticmethod(wrap_method(method.__func__))
            elif isinstance(method, classmethod):
                method = classmethod(wrap_method(method.__func__))
            elif isinstance(method, FunctionType):
                method = wrap_method(method)
            else:
                continue
            setattr(cls, name, method)
        return cls
    return decorate


def demo(limit):
    @call_limiter(limit)
    class Greeter:
        def hello(self, name):
            return f"Привет, {name}!"

    greeter = Greeter()
    for number in range(limit + 1):
        try:
            print(greeter.hello("Михаил"))
        except RuntimeError as error:
            print(error)


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    text = (path / "txt/input.txt").read_text()
    demo(int(text))
