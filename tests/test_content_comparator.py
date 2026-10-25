import unittest

from src.utils.content_comparator import content_comparator


class ContentComparatorTests(unittest.TestCase):
    def test_identical_contents_are_reported_as_identical(self):
        contents = ["photo.jpg", "holiday/", "holiday/photo.jpg"]

        self.assertEqual(
            content_comparator(contents, contents),
            {"is_folder_identical": True, "missing_content": []},
        )

    def test_comparison_ignores_case(self):
        self.assertEqual(
            content_comparator(["Photo.JPG", "Holiday/"], ["photo.jpg", "holiday/"]),
            {"is_folder_identical": True, "missing_content": []},
        )

    def test_missing_items_are_returned_in_original_order(self):
        self.assertEqual(
            content_comparator(["one.txt", "two.txt", "folder/"], ["two.txt"]),
            {
                "is_folder_identical": False,
                "missing_content": ["one.txt", "folder/"],
            },
        )

    def test_extra_copy_items_do_not_make_comparison_fail(self):
        self.assertEqual(
            content_comparator(["one.txt"], ["one.txt", "extra.txt"]),
            {"is_folder_identical": True, "missing_content": []},
        )

    def test_empty_original_is_identical_to_any_copy(self):
        self.assertEqual(
            content_comparator([], ["extra.txt"]),
            {"is_folder_identical": True, "missing_content": []},
        )

    def test_extension_in_is_replaced_by_extension_out(self):
        self.assertEqual(
            content_comparator(
                ["IMG_0001.CR2", "holiday/", "holiday/IMG_0002.cr2", "notes.txt"],
                ["img_0001.jpg", "holiday/", "holiday/IMG_0002.JPG", "notes.txt"],
                extension_in="cr2",
                extension_out="JPG",
            ),
            {"is_folder_identical": True, "missing_content": []},
        )

    def test_extension_is_not_checked(self):
        self.assertEqual(
            content_comparator(
                ["IMG_0001.CR2", "IMG_0002.cr2", "notes.txt", "photo.xmp"],
                ["img_0001.psd", "IMG_0002.CR2", "notes.md", "photo"],
            ),
            {"is_folder_identical": True, "missing_content": []},
        )

    def test_missing_file_keeps_its_name_without_extensions(self):
        self.assertEqual(
            content_comparator(["IMG_0001.CR2", "IMG_0002.CR2"], ["IMG_0001.psd"]),
            {"is_folder_identical": False, "missing_content": ["IMG_0002.CR2"]},
        )

    def test_only_the_last_extension_is_skipped(self):
        self.assertEqual(
            content_comparator(["archive.tar.gz"], ["archive.zip"]),
            {"is_folder_identical": False, "missing_content": ["archive.tar.gz"]},
        )

    def test_file_without_dot_or_starting_with_dot_is_compared_whole(self):
        self.assertEqual(
            content_comparator(["README", ".hidden"], ["README.md", ".hidden"]),
            {"is_folder_identical": True, "missing_content": []},
        )
        self.assertEqual(
            content_comparator([".hidden"], [".other"]),
            {"is_folder_identical": False, "missing_content": [".hidden"]},
        )

    def test_folder_with_same_stem_does_not_count_as_file(self):
        self.assertEqual(
            content_comparator(["IMG_0001.CR2"], ["IMG_0001/"]),
            {"is_folder_identical": False, "missing_content": ["IMG_0001.CR2"]},
        )

    def test_missing_converted_file_is_named_with_extension_out(self):
        self.assertEqual(
            content_comparator(
                ["IMG_0001.CR2", "Vacances/", "Vacances/IMG_0002.cr2"],
                ["IMG_0001.psd", "vacances/"],
                extension_in="cr2",
                extension_out="psd",
            ),
            {"is_folder_identical": False, "missing_content": ["Vacances/IMG_0002.psd"]},
        )

    def test_missing_file_of_another_extension_keeps_its_name(self):
        self.assertEqual(
            content_comparator(
                ["IMG_0001.CR2", "notes.txt"],
                ["IMG_0001.psd"],
                extension_in="cr2",
                extension_out="psd",
            ),
            {"is_folder_identical": False, "missing_content": ["notes.txt"]},
        )

    def test_extension_does_not_apply_to_folders(self):
        self.assertEqual(
            content_comparator(
                ["album.cr2/"], ["album.jpg/"], extension_in="cr2", extension_out="jpg"
            ),
            {"is_folder_identical": False, "missing_content": ["album.cr2/"]},
        )

    def test_extension_is_matched_on_the_whole_suffix(self):
        """'photo.xcr2' ne se termine pas par '.cr2' et garde son nom."""
        self.assertEqual(
            content_comparator(
                ["photo.xcr2"], ["photo.xcr2"], extension_in="cr2", extension_out="jpg"
            ),
            {"is_folder_identical": True, "missing_content": []},
        )


if __name__ == "__main__":
    unittest.main()
