

def content_comparator(folder_content:list, folder_content_copy:list) -> dict:
    """
    Docstring for content_comparator
    
    :param folder_content: Description
    :type folder_content: list
    :param folder_copy_content: Description
    :type folder_copy_content: list
    """
    missing_content = []

    # check for each item in base folder, if there is missing files or folder in the copy
    for item in folder_content:
        # if an item is missing, add it to the missing content list
        if item not in folder_content_copy:
            missing_content.append(item)

    # Return the result as a dict with 2 information
    #   - a boolean to say if the subfolder is identical or not to the main folder
    #   - a list of string representing the missing folder if there is missing ones
    return {
        "is_folder_identical": len(missing_content)==0,  # True if no missing content, else False,
        "missing_content": missing_content
    }


if __name__=="__main__":
    FOLDER_CONTENT = [
        "file1.txt",
        "file2.txt",
        "folder1/",
        "folder1/file1.txt",
        "folder1/file2.txt",
        "folder2/",
        "folder2/file_x.txt",
        "folder2/sub/",
        "folder2/sub/fstring.txt",
        "folder2/sub_diff/",
        "folder2/sub_diff/test1.txt",
        "folder2/sub_diff2/"
    ]

    FOLDER_COPY_CONTENT= FOLDER_CONTENT # copie conforme

    FOLDER_COPY_CONTENT_MISSING = [
        FOLDER_CONTENT[0],          #Entrée 1
        *FOLDER_CONTENT[2:4],       # Entrées 3 à 4
        *FOLDER_CONTENT[5:9],       # Entrées 6 et 7
    ]

    print(f"Folder with misisng_content: {FOLDER_COPY_CONTENT_MISSING}")

    print()

    print("Test Identical:")
    print(content_comparator(FOLDER_CONTENT, FOLDER_COPY_CONTENT))

    print()

    print("Test Missing:")
    print(content_comparator(FOLDER_CONTENT, FOLDER_COPY_CONTENT_MISSING))
