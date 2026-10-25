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

    def test_file_keeping_extension_in_is_reported_missing(self):
        self.assertEqual(
            content_comparator(
                ["IMG_0001.CR2"], ["IMG_0001.CR2"], extension_in="cr2", extension_out="jpg"
            ),
            {"is_folder_identical": False, "missing_content": ["IMG_0001.CR2"]},
        )

    def test_missing_converted_file_keeps_original_name(self):
        self.assertEqual(
            content_comparator(
                ["IMG_0001.CR2", "IMG_0002.CR2"],
                ["IMG_0001.jpg"],
                extension_in="cr2",
                extension_out="jpg",
            ),
            {"is_folder_identical": False, "missing_content": ["IMG_0002.CR2"]},
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
