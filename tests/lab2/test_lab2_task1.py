import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab2" / "task1" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab2_task1", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import AsyncMock, patch


class MessageTests(unittest.IsolatedAsyncioTestCase):
    async def test_message(self):
        output = StringIO()
        with redirect_stdout(output):
            result = await lab.print_message("Привет", 0)
        self.assertEqual(result, "Привет")
        self.assertEqual(output.getvalue(), "Привет\n")

    async def test_delay(self):
        with patch.object(lab.asyncio, "sleep", new_callable=AsyncMock) as sleep:
            with redirect_stdout(StringIO()):
                await lab.print_message("Текст", 2.5)
        sleep.assert_awaited_once_with(2.5)

    async def test_empty_message(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(await lab.print_message("", 0), "")
        self.assertEqual(output.getvalue(), "\n")

    async def test_negative_delay(self):
        with self.assertRaises(ValueError):
            await lab.print_message("Ошибка", -1)


if __name__ == "__main__":
    unittest.main()
