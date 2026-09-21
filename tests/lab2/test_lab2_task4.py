import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab2" / "task4" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab2_task4", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
import threading


class ThreadTests(unittest.TestCase):
    def test_message_and_delay(self):
        output = StringIO()
        with patch.object(lab.time, "sleep") as sleep:
            with redirect_stdout(output):
                lab.print_message("Привет", 2)
        self.assertEqual(output.getvalue(), "Привет\n")
        sleep.assert_called_once_with(2)

    def test_sequential_order(self):
        output = StringIO()
        with redirect_stdout(output):
            elapsed = lab.run_sequential(["A", "B", "C"], 0)
        self.assertEqual(output.getvalue().splitlines(), ["A", "B", "C"])
        self.assertGreaterEqual(elapsed, 0)

    def test_three_separate_threads(self):
        barrier = threading.Barrier(3, timeout=2)
        identifiers = []
        def message(text, delay):
            identifiers.append(threading.get_ident())
            barrier.wait()
        with patch.object(lab, "print_message", message):
            lab.run_threads(["A", "B", "C"], 0)
        self.assertEqual(len(set(identifiers)), 3)

    def test_empty_and_negative_delay(self):
        self.assertGreaterEqual(lab.run_threads([], 0), 0)
        with self.assertRaises(ValueError):
            lab.run_threads(["A"], -1)


if __name__ == "__main__":
    unittest.main()
