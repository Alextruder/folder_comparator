from typing import TypedDict


class ComparisonResult(TypedDict):
    is_folder_identical: bool
    missing_content: list[str]


def content_comparator(
    folder_content: list[str], folder_content_copy: list[str]
) -> ComparisonResult:
    """
    Vérifie que chaque élément du dossier d'origine existe dans la copie (comparaison des noms, sans tenir compte de la casse).

    :param folder_content: Chemins relatifs du dossier d'origine (résultat de folder_mapper)
    :type folder_content: list
    :param folder_content_copy: Chemins relatifs du dossier copie (résultat de folder_mapper)
    :type folder_content_copy: list
    """
    # Normalize the copy once so each lookup is constant-time.
    copy_names = {item.casefold() for item in folder_content_copy}
    missing_content = [
        item for item in folder_content if item.casefold() not in copy_names
    ]

    return {
        "is_folder_identical": not missing_content,
        "missing_content": missing_content,
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

    # Même contenu, mais avec une casse différente (doit être considéré identique)
    FOLDER_COPY_CONTENT_CASE = [item.upper() for item in FOLDER_CONTENT]

    print(f"Folder with missing_content: {FOLDER_COPY_CONTENT_MISSING}")

    print()

    print("Test Identical:")
    print(content_comparator(FOLDER_CONTENT, FOLDER_COPY_CONTENT))

    print()

    print("Test Missing:")
    print(content_comparator(FOLDER_CONTENT, FOLDER_COPY_CONTENT_MISSING))

    print()

    print("Test Case:")
    print(content_comparator(FOLDER_CONTENT, FOLDER_COPY_CONTENT_CASE))
