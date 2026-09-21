import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab2" / "task6" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab2_task6", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

class CounterTests(unittest.TestCase):
    def test_one_thread(self):
        self.assertEqual(lab.run_threads(1, 8), 8)

    def test_three_threads(self):
        self.assertEqual(lab.run_threads(3, 10), 30)

    def test_zero_increments(self):
        self.assertEqual(lab.run_threads(3, 0), 0)

    def test_invalid_parameters(self):
        for workers, count in [(0, 1), (2, -1)]:
            with self.subTest(workers=workers, count=count):
                with self.assertRaises(ValueError):
                    lab.run_threads(workers, count)


if __name__ == "__main__":
    unittest.main()
