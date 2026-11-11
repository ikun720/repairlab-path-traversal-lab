"""Acceptance tests: preserve valid downloads and reject paths outside the root."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.downloads import read_download


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "downloads"
        self.root.mkdir()
        (self.root / "hello.txt").write_text("hello", encoding="utf-8")
        (self.root / "reports").mkdir()
        (self.root / "reports" / "daily.txt").write_text("daily report", encoding="utf-8")
        self.outside = self.base / "outside.txt"
        self.outside.write_text("fake private fixture", encoding="utf-8")
        self.sibling = self.base / "downloads_backup"
        self.sibling.mkdir()
        (self.sibling / "outside.txt").write_text("fake backup fixture", encoding="utf-8")

    def test_existing_download(self):
        self.assertEqual(read_download(self.root, "hello.txt"), "hello")

    def test_nested_download(self):
        self.assertEqual(read_download(self.root, "reports/daily.txt"), "daily report")

    def test_missing_inside_file_keeps_original_error(self):
        with self.assertRaises(FileNotFoundError):
            read_download(self.root, "missing.txt")

    def test_parent_directory_escape_is_rejected(self):
        with self.assertRaises(ValueError):
            read_download(self.root, "../outside.txt")

    def test_absolute_outside_path_is_rejected(self):
        with self.assertRaises(ValueError):
            read_download(self.root, str(self.outside))

    def test_sibling_with_same_prefix_is_rejected(self):
        with self.assertRaises(ValueError):
            read_download(self.root, "../downloads_backup/outside.txt")

    def test_symlink_to_outside_is_rejected(self):
        link = self.root / "shortcut.txt"
        try:
            link.symlink_to(self.outside)
        except (OSError, NotImplementedError):
            self.skipTest("This platform does not permit creating symlinks")
        with self.assertRaises(ValueError):
            read_download(self.root, "shortcut.txt")


if __name__ == "__main__":
    unittest.main()
