import tempfile
import unittest
from pathlib import Path

from src.utils.folder_mapper import folder_mapper


class FolderMapperTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_lists_files_and_directories_as_relative_paths(self):
        (self.root / "photo.jpg").touch()
        (self.root / "holiday" / "beach").mkdir(parents=True)
        (self.root / "holiday" / "beach" / "photo.jpg").touch()

        self.assertEqual(
            set(folder_mapper(str(self.root))),
            {"photo.jpg", "holiday/", "holiday/beach/", "holiday/beach/photo.jpg"},
        )

    def test_ignores_system_files_case_insensitively(self):
        for name in ("Thumbs.db", "DESKTOP.INI", ".DS_Store", "keep.txt"):
            (self.root / name).touch()

        self.assertEqual(folder_mapper(str(self.root)), ["keep.txt"])

    def test_ignores_named_directory_only_at_root(self):
        (self.root / "dont_touch").mkdir()
        (self.root / "dont_touch" / "backup.txt").touch()
        nested = self.root / "other" / "dont_touch"
        nested.mkdir(parents=True)
        (nested / "keep.txt").touch()

        self.assertEqual(
            set(folder_mapper(str(self.root), subdir_to_ignore="DONT_TOUCH")),
            {"other/", "other/dont_touch/", "other/dont_touch/keep.txt"},
        )

    def test_adds_subfolder_prefix(self):
        (self.root / "photo.jpg").touch()

        self.assertEqual(
            folder_mapper(str(self.root), subfolder="album"),
            ["album/photo.jpg"],
        )


if __name__ == "__main__":
    unittest.main()
