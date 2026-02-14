from src.utils.folder_mapper import folder_mapper
from src.utils.content_comparator import content_comparator


def compare_folder(main_folder: str, subfolder: str) -> dict:
    main_folder_content = folder_mapper(full_path=main_folder, subdir_to_ignore=subfolder)
    subfolder_content = folder_mapper(f"{main_folder}/{subfolder}")

    return content_comparator(main_folder_content, subfolder_content)


if __name__ == "__main__":
    PROJECT_PATH = "C:/Users/alexa/OneDrive/Documents/Code/folder_comparator/test_folder"
    SUBDIR_TO_COMPARE = "dont_touch"

    IDENTICAL_PATH = f"{PROJECT_PATH}/IDENTICAL"
    correct_comparator = compare_folder(main_folder=IDENTICAL_PATH, subfolder=SUBDIR_TO_COMPARE)
    print(correct_comparator)

    DIFFERENT_PATH = f"{PROJECT_PATH}/DIFFERENCE"
    different_comparator = compare_folder(main_folder=DIFFERENT_PATH, subfolder=SUBDIR_TO_COMPARE)
    print(different_comparator)
