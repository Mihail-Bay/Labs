import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab1" / "task5" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab1_task5", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import AsyncMock, patch, call
import asyncio


class AsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_first(self):
        output = StringIO()
        with patch.object(lab.asyncio, "sleep", new_callable=AsyncMock) as sleep:
            with redirect_stdout(output):
                await lab.first()
        self.assertEqual(sleep.await_args_list, [call(1), call(4)])
        self.assertEqual(output.getvalue().splitlines(),
                         ["Первая: 1", "Первая: 2", "Первая: 3"])

    async def test_second(self):
        output = StringIO()
        with patch.object(lab.asyncio, "sleep", new_callable=AsyncMock) as sleep:
            with redirect_stdout(output):
                await lab.second()
        self.assertEqual(sleep.await_args_list,
                         [call(3), call(1), call(1)])
        self.assertEqual(len(output.getvalue().splitlines()), 4)

    async def test_both_functions_are_awaited(self):
        with patch.object(lab, "first", new_callable=AsyncMock) as first:
            with patch.object(lab, "second", new_callable=AsyncMock) as second:
                await lab.main()
        first.assert_awaited_once()
        second.assert_awaited_once()

    async def test_functions_start_concurrently(self):
        first_started, second_started = asyncio.Event(), asyncio.Event()
        async def first():
            first_started.set()
            await second_started.wait()
        async def second():
            second_started.set()
            await first_started.wait()
        with patch.object(lab, "first", first):
            with patch.object(lab, "second", second):
                await asyncio.wait_for(lab.main(), timeout=1)
        self.assertTrue(first_started.is_set())
        self.assertTrue(second_started.is_set())


if __name__ == "__main__":
    unittest.main()
