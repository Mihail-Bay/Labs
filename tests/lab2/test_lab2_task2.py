import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab2" / "task2" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab2_task2", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
import asyncio


class GatherTests(unittest.IsolatedAsyncioTestCase):
    async def test_completion_and_result_order(self):
        output = StringIO()
        with redirect_stdout(output):
            result = await lab.run_messages(["A", "B", "C"], [0.04, 0, 0.08])
        self.assertEqual(output.getvalue().splitlines(), ["B", "A", "C"])
        self.assertEqual(result, ["A", "B", "C"])

    async def test_empty_list(self):
        self.assertEqual(await lab.run_messages([], []), [])

    async def test_different_lengths(self):
        with self.assertRaises(ValueError):
            await lab.run_messages(["A"], [])

    async def test_tasks_start_together(self):
        started = []
        all_started = asyncio.Event()
        async def message(text, delay):
            started.append(text)
            if len(started) == 3:
                all_started.set()
            await all_started.wait()
            return text
        with patch.object(lab, "print_message", message):
            result = await asyncio.wait_for(
                lab.run_messages(["A", "B", "C"], [2, 1, 3]), 1)
        self.assertEqual(result, ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
