import os
from pathlib import Path


# Fichiers créés automatiquement par Windows / macOS, à ne jamais comparer (en minuscules)
IGNORED_FILES = {"thumbs.db", "desktop.ini", ".ds_store"}


def folder_mapper(
    full_path: str,
    subfolder: str | None = None,
) -> list[str]:
    """
    Liste les fichiers et dossiers d'un dossier, en chemins relatifs.

    :param full_path: Chemin du dossier à lister
    :param subfolder: Préfixe relatif à ajouter à chaque chemin
    :return: Chemins relatifs des fichiers et dossiers trouvés
    """
    file_list = []
    pending: list[tuple[str, str | None, os.DirEntry[str] | None]] = [
        (full_path, subfolder, None)
    ]

    while pending:
        directory, relative_path, entry = pending.pop()
        if entry is None:
            with os.scandir(directory) as entries:
                pending.extend(
                    (item.path, relative_path, item)
                    for item in reversed(list(entries))
                )
            continue

        if entry.is_file() and entry.name.casefold() in IGNORED_FILES:
            continue

        item_path = entry.name if relative_path is None else f"{relative_path}/{entry.name}"
        if entry.is_dir():
            file_list.append(f"{item_path}/")
            pending.append((entry.path, item_path, None))
        elif entry.is_file():
            file_list.append(item_path)

    return file_list


if __name__ == "__main__":
    # Dossier de test du projet, retrouvé à partir de l'emplacement de ce fichier
    FULL_PATH = (Path(__file__).resolve().parents[2] / "test_folder" / "IDENTICAL" / "original").as_posix()
    folder_map = folder_mapper(full_path=FULL_PATH)
    print(folder_map)
