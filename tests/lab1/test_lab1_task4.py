import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab1" / "task4" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab1_task4", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

class LimiterTests(unittest.TestCase):
    def test_limit(self):
        @lab.call_limiter(2)
        class Example:
            def get(self):
                return 5
        obj = Example()
        self.assertEqual(obj.get(), 5)
        self.assertEqual(obj.get(), 5)
        with self.assertRaises(RuntimeError):
            obj.get()

    def test_methods_have_separate_counters(self):
        @lab.call_limiter(1)
        class Example:
            def first(self):
                return 1
            def second(self):
                return 2
        obj = Example()
        self.assertEqual(obj.first(), 1)
        self.assertEqual(obj.second(), 2)
        with self.assertRaises(RuntimeError):
            obj.first()

    def test_counter_is_shared_by_instances(self):
        @lab.call_limiter(1)
        class Example:
            def get(self):
                return 1
        first, second = Example(), Example()
        first.get()
        with self.assertRaises(RuntimeError):
            second.get()

    def test_zero_and_negative_limit(self):
        @lab.call_limiter(0)
        class Example:
            def get(self):
                return 1
        with self.assertRaises(RuntimeError):
            Example().get()
        with self.assertRaises(ValueError):
            lab.call_limiter(-1)


if __name__ == "__main__":
    unittest.main()
