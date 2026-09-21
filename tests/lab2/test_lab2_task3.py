import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab2" / "task3" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab2_task3", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import Mock, patch
import asyncio


class RequestTests(unittest.IsolatedAsyncioTestCase):
    async def test_sync_order(self):
        results = [("A", "200", 0.2), ("B", "200", 0.1)]
        with patch.object(lab, "fetch_sync", side_effect=results):
            with redirect_stdout(StringIO()):
                actual, total = lab.run_sync(["A", "B"])
        self.assertEqual(actual, results)
        self.assertGreaterEqual(total, 0)

    async def test_async_completion_order(self):
        async def fake_fetch(session, url):
            await asyncio.sleep(0.04 if url == "slow" else 0)
            return url, "200", 0
        with patch.object(lab, "fetch_async", fake_fetch):
            with redirect_stdout(StringIO()):
                results, total = await lab.run_async(["slow", "fast"])
        self.assertEqual([item[0] for item in results], ["fast", "slow"])

    async def test_request_errors(self):
        with patch.object(lab.requests, "get", side_effect=lab.requests.Timeout):
            self.assertEqual(lab.fetch_sync("url")[1], "Timeout")
        session = Mock()
        session.get.side_effect = lab.aiohttp.ClientConnectionError()
        result = await lab.fetch_async(session, "url")
        self.assertEqual(result[1], "ClientConnectionError")

    async def test_empty_urls(self):
        self.assertEqual(lab.run_sync([])[0], [])
        self.assertEqual((await lab.run_async([]))[0], [])


if __name__ == "__main__":
    unittest.main()
