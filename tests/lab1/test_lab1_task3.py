import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab1" / "task3" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab1_task3", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from io import StringIO
from contextlib import redirect_stdout


class ClassLoggerTests(unittest.TestCase):
    def test_regular_method(self):
        output = StringIO()
        with redirect_stdout(output):
            value = lab.Calculator(5).add(2)
        self.assertEqual(value, 7)
        self.assertIn("Класс: Calculator", output.getvalue())
        self.assertIn("Метод: add", output.getvalue())
        self.assertIn("Время:", output.getvalue())

    def test_magic_methods(self):
        output = StringIO()
        with redirect_stdout(output):
            text = str(lab.Calculator(8))
        self.assertEqual(text, "8")
        self.assertIn("Метод: __init__", output.getvalue())
        self.assertIn("Метод: __str__", output.getvalue())

    def test_magic_methods_disabled(self):
        @lab.logger(show_magic_methods=False)
        class Number:
            def __str__(self):
                return "10"
            def get(self):
                return 10
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(str(Number()), "10")
            self.assertEqual(Number().get(), 10)
        self.assertNotIn("__str__", output.getvalue())
        self.assertIn("Метод: get", output.getvalue())

    def test_static_class_and_repr_methods(self):
        @lab.logger
        class Example:
            @staticmethod
            def twice(value):
                return value * 2
            @classmethod
            def name(cls):
                return cls.__name__
            def __repr__(self):
                return "Example()"
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(Example.twice(3), 6)
            self.assertEqual(Example.name(), "Example")
            self.assertEqual(repr(Example()), "Example()")
        self.assertIn("Метод: __repr__", output.getvalue())


if __name__ == "__main__":
    unittest.main()
