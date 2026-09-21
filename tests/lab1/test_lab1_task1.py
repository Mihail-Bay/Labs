import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab1" / "task1" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab1_task1", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch


class LoggerTests(unittest.TestCase):
    def test_result_and_arguments(self):
        output = StringIO()
        with redirect_stdout(output):
            result = lab.add(2, b=3)
        self.assertEqual(result, 5)
        self.assertIn("add", output.getvalue())
        self.assertIn("{'b': 3}", output.getvalue())

    def test_time(self):
        output = StringIO()
        with patch.object(lab, "perf_counter", side_effect=[1, 1.25]):
            with redirect_stdout(output):
                lab.add(1, 1)
        self.assertIn("0.250000", output.getvalue())

    def test_exception_is_not_hidden(self):
        @lab.logger
        def fail():
            raise ValueError("Ошибка")
        output = StringIO()
        with redirect_stdout(output):
            with self.assertRaises(ValueError):
                fail()
        self.assertIn("Время:", output.getvalue())

    def test_function_name_is_preserved(self):
        self.assertEqual(lab.add.__name__, "add")


if __name__ == "__main__":
    unittest.main()
