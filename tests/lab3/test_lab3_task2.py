import sys
import unittest
from pathlib import Path

import importlib.util

source = Path(__file__).resolve().parents[2] / "Lab3" / "task2" / "src" / "lab.py"
spec = importlib.util.spec_from_file_location("lab3_task2", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

import os
import tempfile
from io import StringIO
from contextlib import redirect_stdout


class DirectoryTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.source = os.path.join(self.folder.name, "source.txt")
        self.work = os.path.join(self.folder.name, "work")
        os.mkdir(self.work)
        lab.write_file(self.source, "Оригинал")
        previous = os.getcwd()
        self.addCleanup(os.chdir, previous)

    def test_copy(self):
        target = os.path.join(self.work, "copy.txt")
        lab.copy_file(self.source, target)
        self.assertEqual(Path(target).read_text(encoding="utf-8"), "Оригинал")

    def test_move_and_rename(self):
        with redirect_stdout(StringIO()):
            moved, new = lab.run(self.source, self.work, "Новый")
        self.assertEqual(Path(moved).read_text(encoding="utf-8"), "Оригинал")
        self.assertEqual(Path(new).read_text(encoding="utf-8"), "Новый")
        self.assertFalse(os.path.exists(os.path.join(self.work, "new.txt")))

    def test_tree_and_current_directory(self):
        output = StringIO()
        with redirect_stdout(output):
            lab.run(self.source, self.work, "text")
        self.assertFalse(os.path.exists(os.path.join(self.work, "empty")))
        self.assertTrue(os.path.isfile(os.path.join(
            self.work, "extra", "inside", "note.txt")))
        self.assertIn("note.txt", output.getvalue())
        self.assertEqual(os.getcwd(), self.work)

    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            lab.copy_file(os.path.join(self.work, "missing.txt"),
                          os.path.join(self.work, "copy.txt"))


if __name__ == "__main__":
    unittest.main()
