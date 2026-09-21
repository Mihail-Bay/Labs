import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab3" / "task1" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab3_task1", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

import os
import tempfile
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch


class FileTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = os.path.join(self.folder.name, "test.txt")

    def test_create_and_size(self):
        lab.write_file(self.path, "Привет")
        self.assertTrue(os.path.isfile(self.path))
        self.assertEqual(lab.file_info(self.path)["size"],
                         len("Привет".encode("utf-8")))
        self.assertGreater(lab.file_info(self.path)["modified"], 0)

    def test_change_permissions(self):
        lab.write_file(self.path, "text")
        try:
            before, after = lab.change_permissions(self.path)
            self.assertNotEqual(before, after)
            self.assertEqual(after & 0o222, 0)
        finally:
            os.chmod(self.path, 0o600)

    def test_go_to_script(self):
        previous = os.getcwd()
        try:
            os.chdir(self.folder.name)
            with redirect_stdout(StringIO()):
                folder = lab.go_to_script()
            self.assertEqual(os.getcwd(), folder)
            self.assertEqual(folder, os.path.dirname(lab.__file__))
        finally:
            os.chdir(previous)

    def test_user_without_terminal(self):
        with patch.object(lab.os, "getlogin", side_effect=OSError):
            with patch.dict(os.environ, {"USER": "student"}, clear=True):
                self.assertEqual(lab.current_user(), "student")


if __name__ == "__main__":
    unittest.main()
