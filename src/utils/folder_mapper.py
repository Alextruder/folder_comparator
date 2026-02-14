import os


def folder_mapper(full_path: str, subfolder: str=None, subdir_to_ignore: str = None) -> list:
    """
    Docstring for folder_mapper
    
    :param full_path: Path of the directory to map
    :type full_path: str
    :param subfolder: Subfolder to add to the final file path
    :type subfolder: str
    :param file_to_ignore: Subdirectory to ignore
    :type file_to_ignore: str
    """
    # Initialiser la liste des fichiers dans une liste
    file_list = []
    # Récupérer chaque fichier et dossier dans le dossier actuel
    items_list = os.scandir(full_path)

    # Pour chaque objet du dossier actuel
    for entry in items_list:
        # Si c'est le fichier à comparer (je pars du principe que ce sous dossier est dans le dossier principal)
        if subfolder is None and entry.is_dir() and entry.name==subdir_to_ignore:
            # On skip, sinon on va avoir des problèmes lors de la comparaison
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
    FULL_PATH = "C:/Users/alexa/OneDrive/Documents/Code/folder_comparator/test_folder"
    SUBDIR_TO_IGNORE = "dont_touch"
    folder_map = folder_mapper(full_path=FULL_PATH, subdir_to_ignore=SUBDIR_TO_IGNORE)
    print(folder_map)