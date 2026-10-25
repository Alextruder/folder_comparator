import tempfile
import unittest
from pathlib import Path

from src.main import PROJECT_ROOT, compare_folder, load_config


TEST_FOLDER = PROJECT_ROOT / "test_folder"


def compare_case(case: str, extension_in: str | None = None, extension_out: str | None = None) -> dict:
    """Compare les dossiers original/ et copy/ d'un cas de test_folder."""
    return compare_folder(
        (TEST_FOLDER / case / "original").as_posix(),
        (TEST_FOLDER / case / "copy").as_posix(),
        extension_in,
        extension_out,
    )


class CompareFolderTests(unittest.TestCase):
    """Tests de bout en bout sur les 3 cas du dossier test_folder."""

    def test_identical_folder(self):
        result = compare_case("IDENTICAL")

        self.assertEqual(result, {"is_folder_identical": True, "missing_content": []})

    def test_different_folder_reports_missing_content(self):
        result = compare_case("DIFFERENCE")

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
        result = compare_case("CASSE")

        self.assertEqual(result, {"is_folder_identical": True, "missing_content": []})

    def test_extension_folder_with_extensions(self):
        result = compare_case("EXTENSION", "CR2", "jpg")

        self.assertEqual(result, {"is_folder_identical": True, "missing_content": []})

    def test_extension_folder_without_extensions_reports_missing_content(self):
        result = compare_case("EXTENSION")

        self.assertCountEqual(
            result["missing_content"], ["IMG_0001.CR2", "Vacances/IMG_0002.cr2"]
        )

    def test_folders_can_be_anywhere(self):
        """Les 2 dossiers n'ont pas besoin d'être l'un dans l'autre."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "disque_1" / "photos").mkdir(parents=True)
            (root / "disque_2" / "sauvegarde").mkdir(parents=True)
            (root / "disque_1" / "photos" / "IMG_0001.JPG").touch()
            (root / "disque_2" / "sauvegarde" / "img_0001.jpg").touch()

            result = compare_folder(
                (root / "disque_1" / "photos").as_posix(),
                (root / "disque_2" / "sauvegarde").as_posix(),
            )

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

    def test_relative_paths_are_resolved_from_project_root(self):
        self.write_config(
            'dossier_principal = "test_folder/IDENTICAL/original"\n'
            'copy_folder = "test_folder/IDENTICAL/copy"\n'
        )

        self.assertEqual(
            load_config(self.config_path),
            (
                (TEST_FOLDER / "IDENTICAL" / "original").as_posix(),
                (TEST_FOLDER / "IDENTICAL" / "copy").as_posix(),
                None,
                None,
            ),
        )

    def test_absolute_paths_are_kept(self):
        (self.root / "photos").mkdir()
        (self.root / "sauvegarde").mkdir()
        self.write_config(
            f'dossier_principal = "{(self.root / "photos").as_posix()}"\n'
            f'copy_folder = "{(self.root / "sauvegarde").as_posix()}"\n'
        )

        self.assertEqual(
            load_config(self.config_path),
            ((self.root / "photos").as_posix(), (self.root / "sauvegarde").as_posix(), None, None),
        )

    def test_extensions_are_read_without_leading_dot(self):
        self.write_config(
            'dossier_principal = "test_folder/EXTENSION/original"\n'
            'extension_in = ".CR2"\n'
            'copy_folder = "test_folder/EXTENSION/copy"\n'
            'extension_out = "jpg"\n'
        )

        self.assertEqual(load_config(self.config_path)[2:], ("CR2", "jpg"))

    def test_empty_extensions_are_ignored(self):
        self.write_config(
            'dossier_principal = "test_folder/EXTENSION/original"\n'
            'extension_in = ""\n'
            'copy_folder = "test_folder/EXTENSION/copy"\n'
            'extension_out = ""\n'
        )

        self.assertEqual(load_config(self.config_path)[2:], (None, None))

    def test_only_one_extension_exits(self):
        self.write_config(
            'dossier_principal = "test_folder/EXTENSION/original"\n'
            'extension_in = "CR2"\n'
            'copy_folder = "test_folder/EXTENSION/copy"\n'
        )

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("à la fois 'extension_in' et 'extension_out'", str(context.exception.code))

    def test_extension_that_is_not_text_exits(self):
        self.write_config(
            'dossier_principal = "test_folder/EXTENSION/original"\n'
            'extension_in = 2\n'
            'copy_folder = "test_folder/EXTENSION/copy"\n'
            'extension_out = "jpg"\n'
        )

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("'extension_in' doit être un texte", str(context.exception.code))

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
        self.write_config('dossier_principal = "test_folder/IDENTICAL/original"\n')

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("copy_folder", str(context.exception.code))

    def test_old_subfolder_key_is_not_accepted(self):
        self.write_config(
            'dossier_principal = "test_folder/IDENTICAL/original"\nsous_dossier = "dont_touch"\n'
        )

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("copy_folder", str(context.exception.code))

    def test_empty_key_exits(self):
        self.write_config('dossier_principal = ""\ncopy_folder = "test_folder/IDENTICAL/copy"\n')

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("dossier_principal", str(context.exception.code))

    def test_missing_main_folder_exits(self):
        self.write_config(
            'dossier_principal = "test_folder/ABSENT"\ncopy_folder = "test_folder/IDENTICAL/copy"\n'
        )

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("dossier principal n'existe pas", str(context.exception.code))

    def test_missing_copy_folder_exits(self):
        self.write_config(
            'dossier_principal = "test_folder/IDENTICAL/original"\ncopy_folder = "test_folder/ABSENT"\n'
        )

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("dossier copie n'existe pas", str(context.exception.code))

    def test_same_folder_twice_exits(self):
        self.write_config(
            'dossier_principal = "test_folder/IDENTICAL/original"\n'
            'copy_folder = "test_folder/IDENTICAL/original"\n'
        )

        with self.assertRaises(SystemExit) as context:
            load_config(self.config_path)

        self.assertIn("même dossier", str(context.exception.code))


if __name__ == "__main__":
    unittest.main()
