import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab3" / "task3" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab3_task3", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)


class SystemTests(unittest.TestCase):
    def test_list_and_process_info(self):
        process = Mock()
        process.info = {"pid": 123, "name": "demo.exe"}
        process.as_dict.return_value = {
            "pid": 123,
            "name": "demo.exe",
            "status": "running"
        }

        with patch.object(lab.psutil, "process_iter", return_value=[process]):
            self.assertEqual(lab.list_processes(), [process.info])

        with patch.object(lab.psutil, "Process", return_value=process):
            self.assertEqual(lab.process_info(123)["pid"], 123)

    def test_terminate_process(self):
        process = Mock()

        with patch.object(lab.psutil, "Process", return_value=process):
            lab.terminate_process(123)

        process.terminate.assert_called_once()

    def test_environment_and_system_info(self):
        with patch.dict(os.environ, {}, clear=True):
            lab.set_environment("LAB_TEST", "hello")
            self.assertEqual(os.environ["LAB_TEST"], "hello")

            with self.assertRaises(ValueError):
                lab.set_environment("BAD=NAME", "x")

        self.assertEqual(lab.system_info()["PID скрипта"], os.getpid())

    def test_windows_priority(self):
        process = Mock()

        # create=True нужен только для запуска теста не на Windows.
        with patch.object(lab.psutil, "IDLE_PRIORITY_CLASS", 64, create=True), \
             patch.object(lab.psutil, "NORMAL_PRIORITY_CLASS", 32, create=True), \
             patch.object(lab.psutil, "HIGH_PRIORITY_CLASS", 128, create=True), \
             patch.object(lab.psutil, "Process", return_value=process):
            lab.change_priority(123, "high")

        process.nice.assert_called_once_with(128)


if __name__ == "__main__":
    unittest.main()
