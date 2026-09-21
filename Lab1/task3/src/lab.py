from functools import wraps
from time import perf_counter
from types import FunctionType
from pathlib import Path


def logger(cls=None, show_magic_methods=True):
    def decorate(target):
        def wrap_method(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Не вызываем __repr__ объектов этого класса.
                def safe(value):
                    if isinstance(value, target) or value is target:
                        return f"<{target.__name__}>"
                    if isinstance(value, (int, float, str, bool)):
                        return repr(value)
                    return f"<{type(value).__name__}>"

                values = [safe(value) for value in args]
                named = {key: safe(value)
                         for key, value in kwargs.items()}
                print(f"Класс: {target.__name__}")
                print(f"Метод: {func.__name__}")
                print(f"Аргументы: {values}, {named}")
                start = perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    elapsed = perf_counter() - start
                    print(f"Время: {elapsed:.6f} с")
            return wrapper

        for name, method in list(vars(target).items()):
            magic = name.startswith("__") and name.endswith("__")
            if magic and not show_magic_methods:
                continue
            if isinstance(method, staticmethod):
                method = staticmethod(wrap_method(method.__func__))
            elif isinstance(method, classmethod):
                method = classmethod(wrap_method(method.__func__))
            elif isinstance(method, FunctionType):
                method = wrap_method(method)
            else:
                continue
            setattr(target, name, method)
        return target

    if cls is None:
        return decorate
    return decorate(cls)


@logger
class Calculator:
    def __init__(self, value):
        self.value = value

    def add(self, number):
        self.value += number
        return self.value

    def __str__(self):
        return str(self.value)


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent
    text = (path / "txt/input.txt").read_text()
    value, number = map(int, text.split())
    calculator = Calculator(value)
    calculator.add(number)
    print(calculator)
