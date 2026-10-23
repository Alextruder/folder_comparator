import sys
import tomllib
from pathlib import Path

from src.utils.folder_mapper import folder_mapper
from src.utils.content_comparator import content_comparator


# Racine du projet (le dossier qui contient src/ et config.toml)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.toml"


def compare_folder(main_folder: str, subfolder: str) -> dict:
    main_folder_content = folder_mapper(full_path=main_folder, subdir_to_ignore=subfolder)
    subfolder_content = folder_mapper(f"{main_folder}/{subfolder}")

    return content_comparator(main_folder_content, subfolder_content)


def load_config(config_path: Path = CONFIG_PATH) -> tuple[str, str]:
    """
    Lit le fichier de configuration et renvoie (dossier_principal, sous_dossier).

    Arrête le programme avec un message clair si la configuration est incorrecte.
    """
    if not config_path.is_file():
        sys.exit(f"Erreur : fichier de configuration introuvable ({config_path}).")

    try:
        with open(config_path, "rb") as config_file:
            config = tomllib.load(config_file)
    except tomllib.TOMLDecodeError as error:
        sys.exit(f"Erreur : le fichier {config_path.name} est mal écrit ({error}).")

    # On vérifie que les 2 clés obligatoires sont présentes
    for key in ("dossier_principal", "sous_dossier"):
        if not config.get(key):
            sys.exit(f"Erreur : la clé '{key}' est absente ou vide dans {config_path.name}.")

    # Un chemin relatif est calculé à partir de la racine du projet, pas du dossier courant
    main_folder = Path(config["dossier_principal"])
    if not main_folder.is_absolute():
        main_folder = PROJECT_ROOT / main_folder

    subfolder = config["sous_dossier"]

    if not main_folder.is_dir():
        sys.exit(f"Erreur : le dossier principal n'existe pas ({main_folder}).")
    if not (main_folder / subfolder).is_dir():
        sys.exit(f"Erreur : le sous-dossier '{subfolder}' n'existe pas dans {main_folder}.")

    return main_folder.as_posix(), subfolder


if __name__ == "__main__":
    MAIN_FOLDER, SUBFOLDER = load_config()
    result = compare_folder(main_folder=MAIN_FOLDER, subfolder=SUBFOLDER)

    if result["is_folder_identical"]:
        print(f"OK : le sous-dossier '{SUBFOLDER}' contient tout le contenu de {MAIN_FOLDER}.")
    else:
        print(f"{len(result['missing_content'])} élément(s) de {MAIN_FOLDER} absent(s) de '{SUBFOLDER}' :")
        for item in result["missing_content"]:
            print(f"  - {item}")
        # Code de sortie 1 pour signaler qu'il manque des éléments
        sys.exit(1)
