import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab1" / "task2" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab1_task2", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from unittest.mock import Mock, patch


class RetryTests(unittest.TestCase):
    def test_success_at_once(self):
        function = Mock(return_value=7)
        with patch.object(lab.time, "sleep") as sleep:
            self.assertEqual(lab.retry(3, 1)(function)(), 7)
        self.assertEqual(function.call_count, 1)
        sleep.assert_not_called()

    def test_success_after_errors(self):
        function = Mock(side_effect=[ValueError(), ValueError(), 9])
        with patch.object(lab.time, "sleep") as sleep:
            result = lab.retry(3, 0.2, [ValueError])(function)()
        self.assertEqual(result, 9)
        self.assertEqual(function.call_count, 3)
        self.assertEqual(sleep.call_count, 2)
        sleep.assert_called_with(0.2)

    def test_attempts_are_exhausted(self):
        function = Mock(side_effect=ValueError("Ошибка"))
        with patch.object(lab.time, "sleep") as sleep:
            with self.assertRaises(ValueError):
                lab.retry(2, 0)(function)()
        self.assertEqual(function.call_count, 2)
        self.assertEqual(sleep.call_count, 1)

    def test_unlisted_error_and_invalid_parameters(self):
        function = Mock(side_effect=TypeError())
        with self.assertRaises(TypeError):
            lab.retry(3, 0, [ValueError])(function)()
        self.assertEqual(function.call_count, 1)
        for attempts, delay in [(0, 1), (1, -1)]:
            with self.subTest(attempts=attempts, delay=delay):
                with self.assertRaises(ValueError):
                    lab.retry(attempts, delay)


if __name__ == "__main__":
    unittest.main()
