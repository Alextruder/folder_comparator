from typing import TypedDict


class ComparisonResult(TypedDict):
    is_folder_identical: bool
    missing_content: list[str]


def expected_copy_name(
    item: str, extension_in: str | None = None, extension_out: str | None = None
) -> str:
    """
    Renvoie le nom attendu dans la copie pour un élément du dossier d'origine.

    Un fichier qui se termine par .extension_in doit se retrouver avec .extension_out dans la copie
    (ex: "Vacances/IMG_0001.CR2" -> "Vacances/IMG_0001.psd").
    Les dossiers et les fichiers d'une autre extension gardent le même nom.
    """
    if extension_in is None or extension_out is None or item.endswith("/"):
        return item

    suffix_in = f".{extension_in}"
    if item.casefold().endswith(suffix_in.casefold()) and len(item.rsplit("/", 1)[-1]) > len(suffix_in):
        return f"{item[: -len(suffix_in)]}.{extension_out}"
    return item


def comparison_key(item: str) -> str:
    """
    Renvoie la clé de comparaison d'un élément : son chemin en minuscules, sans l'extension pour un fichier.

    Ex: "Vacances/IMG_0001.CR2" -> "vacances/img_0001". Les dossiers gardent leur nom complet.
    """
    name = item.casefold()
    if name.endswith("/"):
        return name

    folder, _, file_name = name.rpartition("/")
    stem, dot, _ = file_name.rpartition(".")
    # Un nom sans point, ou qui commence par un point (".photo"), n'a pas d'extension
    if not dot or not stem:
        return name
    return f"{folder}/{stem}" if folder else stem


def content_comparator(
    folder_content: list[str],
    folder_content_copy: list[str],
    extension_in: str | None = None,
    extension_out: str | None = None,
) -> ComparisonResult:
    """
    Vérifie que chaque élément du dossier d'origine existe dans la copie.

    Les noms sont comparés sans tenir compte de la casse ni de l'extension des fichiers :
    "IMG_0001.CR2" est présent si la copie contient "IMG_0001.psd", "img_0001.jpg"...
    Les éléments manquants sont renvoyés avec le nom attendu dans la copie (donc avec extension_out).

    :param folder_content: Chemins relatifs du dossier d'origine (résultat de folder_mapper)
    :type folder_content: list
    :param folder_content_copy: Chemins relatifs du dossier copie (résultat de folder_mapper)
    :type folder_content_copy: list
    :param extension_in: Extension des fichiers du dossier d'origine à afficher avec extension_out s'ils manquent (sans le point)
    :param extension_out: Extension à afficher pour ces fichiers manquants (sans le point)
    """
    # Normalize the copy once so each lookup is constant-time.
    copy_keys = {comparison_key(item) for item in folder_content_copy}
    missing_content = [
        expected_copy_name(item, extension_in, extension_out)
        for item in folder_content
        if comparison_key(item) not in copy_keys
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

    print()

    # Les .txt de l'original sont des .md dans la copie
    FOLDER_COPY_CONTENT_EXTENSION = [item.replace(".txt", ".md") for item in FOLDER_CONTENT]
    print("Test Extension:")
    print(content_comparator(FOLDER_CONTENT, FOLDER_COPY_CONTENT_EXTENSION, "txt", "md"))
