import os
from pathlib import Path


# Fichiers créés automatiquement par Windows / macOS, à ne jamais comparer (en minuscules)
IGNORED_FILES = {"thumbs.db", "desktop.ini", ".ds_store"}


def folder_mapper(full_path: str, subfolder: str=None, subdir_to_ignore: str = None) -> list:
    """
    Liste récursivement les fichiers et dossiers d'un dossier, en chemins relatifs.

    :param full_path: Chemin du dossier à lister
    :type full_path: str
    :param subfolder: Sous-dossier courant, ajouté devant chaque chemin (utilisé par la récursion)
    :type subfolder: str
    :param subdir_to_ignore: Sous-dossier du dossier de départ à ne pas lister (la copie à comparer)
    :type subdir_to_ignore: str
    """
    # Initialiser la liste des fichiers dans une liste
    file_list = []
    # Récupérer chaque fichier et dossier dans le dossier actuel
    # (le "with" referme proprement le dossier une fois la lecture terminée)
    with os.scandir(full_path) as items_list:
        items_list = list(items_list)

    # Pour chaque objet du dossier actuel
    for entry in items_list:
        # Si c'est le fichier à comparer (je pars du principe que ce sous dossier est dans le dossier principal)
        # casefold() met en minuscules pour ignorer la casse ("Dont_Touch" == "dont_touch")
        if (subfolder is None and entry.is_dir() and subdir_to_ignore is not None
                and entry.name.casefold() == subdir_to_ignore.casefold()):
            # On skip, sinon on va avoir des problèmes lors de la comparaison
            pass
        # Si c'est un fichier système (Thumbs.db, desktop.ini...), on l'ignore
        elif entry.is_file() and entry.name.casefold() in IGNORED_FILES:
            pass
        # Si c'est un dossier
        elif entry.is_dir():
            # On relance cette fonction récursivement pour récupérer chaque objet que contient le sous dossier
            # (jusqu'à ce qu'on ne trouve plus de dossier dans le sous-dossier actuel)
            file_list = [
                *file_list,     # le * devant une liste permet de récupérer tous les éléments d'une liste.
                                # On fait ça pour éviter une liste de liste et juste avoir une liste simple
                f"{entry.name}/" if subfolder is None else f"{subfolder}/{entry.name}/" ,   # Si subfolder, on l'ajoute au dossier actuel pour listing
                *folder_mapper(f"{full_path}/{entry.name}",     # on relance la fonction en changeant le subfolder (prochain dossier actuel)
                    subfolder=f"{subfolder}/{entry.name}"       # Si c'était pas vide, on concatène le précédent et le prochain.
                    if subfolder is not None else entry.name)   # Sinon, on ajoute juste le prochain dossier
            ]  
        elif entry.is_file():   # Si c'est un fichier, on ajoute :
            file_list.append(entry.name if subfolder is None   # Juste le nom du fichier si c'est le dossier d'origine
                  else f"{subfolder}/{entry.name}") # On concatène le nom du fichier et son sous dossier si on n'est pas dans le dossier d'origine

    return file_list


if __name__ == "__main__":
    # Dossier de test du projet, retrouvé à partir de l'emplacement de ce fichier
    FULL_PATH = (Path(__file__).resolve().parents[2] / "test_folder" / "IDENTICAL").as_posix()
    SUBDIR_TO_IGNORE = "dont_touch"
    folder_map = folder_mapper(full_path=FULL_PATH, subdir_to_ignore=SUBDIR_TO_IGNORE)
    print(folder_map)