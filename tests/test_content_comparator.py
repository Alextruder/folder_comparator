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


if __name__ == "__main__":
    unittest.main()
