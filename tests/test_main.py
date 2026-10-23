import tempfile
import unittest
from pathlib import Path

from src.main import PROJECT_ROOT, compare_folder, load_config


TEST_FOLDER = PROJECT_ROOT / "test_folder"
SUBFOLDER = "dont_touch"


class CompareFolderTests(unittest.TestCase):
    """Tests de bout en bout sur les 3 cas du dossier test_folder."""

    def test_identical_folder(self):
        result = compare_folder((TEST_FOLDER / "IDENTICAL").as_posix(), SUBFOLDER)

        self.assertEqual(result, {"is_folder_identical": True, "missing_content": []})

    def test_different_folder_reports_missing_content(self):
        result = compare_folder((TEST_FOLDER / "DIFFERENCE").as_posix(), SUBFOLDER)

        self.assertFalse(result["is_folder_identical"])
        self.assertCountEqual(
            result["missing_content"],
            [
                "merging_file/sub/",
                "merging_file/sub/test.txt",
                "watching/",
                "watching/document1.json",
                "watching/document1.txt",
                "watching/document2.png",
                "watching/sub/",
                "watching/sub/test.txt",
                "watching/unkonwn.jpg",
            ],
        )

    def test_case_folder_ignores_case_and_system_files(self):
        result = compare_folder((TEST_FOLDER / "CASSE").as_posix(), SUBFOLDER)

        self.assertEqual(result, {"is_folder_identical": True, "missing_content": []})

    def test_subfolder_name_is_case_insensitive(self):
        result = compare_folder((TEST_FOLDER / "CASSE").as_posix(), SUBFOLDER.upper())

        self.assertEqual(result, {"is_folder_identical": True, "missing_content": []})


class LoadConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.config_path = self.root / "config.toml"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_config(self, content: str):
        self.config_path.write_text(content, encoding="utf-8")

    def test_relative_path_is_resolved_from_project_root(self):
        self.write_config('dossier_principal = "test_folder/IDENTICAL"\nsous_dossier = "dont_touch"\n')

        self.assertEqual(
            load_config(self.config_path),
            ((TEST_FOLDER / "IDENTICAL").as_posix(), "dont_touch"),
        )

    def test_absolute_path_is_kept(self):
        (self.root / "photos" / "dont_touch").mkdir(parents=True)
        self.write_config(
            f'dossier_principal = "{(self.root / "photos").as_posix()}"\nsous_dossier = "dont_touch"\n'
        )

        self.assertEqual(
            load_config(self.config_path),
            ((self.root / "photos").as_posix(), "dont_touch"),
        )

    def test_missing_config_file_exits(self):
        with self.assertRaises(SystemExit) as context:
            load_config(self.root / "absent.toml")

        self.assertIn("introuvable", str(context.exception.code))

    def test_invalid_toml_exits(self):
        self.write_config("dossier_principal = \n")

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("mal écrit", str(context.exception.code))

    def test_missing_key_exits(self):
        self.write_config('dossier_principal = "test_folder/IDENTICAL"\n')

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("sous_dossier", str(context.exception.code))

    def test_empty_key_exits(self):
        self.write_config('dossier_principal = ""\nsous_dossier = "dont_touch"\n')

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("dossier_principal", str(context.exception.code))

    def test_missing_main_folder_exits(self):
        self.write_config('dossier_principal = "test_folder/ABSENT"\nsous_dossier = "dont_touch"\n')

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("dossier principal n'existe pas", str(context.exception.code))

    def test_missing_subfolder_exits(self):
        self.write_config('dossier_principal = "test_folder/IDENTICAL"\nsous_dossier = "absent"\n')

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("'absent' n'existe pas", str(context.exception.code))


if __name__ == "__main__":
    unittest.main()
