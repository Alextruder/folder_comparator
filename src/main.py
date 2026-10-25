import sys
import tomllib
from pathlib import Path

if __package__:
    from .utils.content_comparator import content_comparator
    from .utils.folder_mapper import folder_mapper
else:
    from utils.content_comparator import content_comparator
    from utils.folder_mapper import folder_mapper


# Racine du projet (le dossier qui contient src/ et config.toml)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.toml"


def compare_folder(main_folder: str, copy_folder: str) -> dict:
    """Compare a folder with its copy and return the comparison result."""
    main_folder_content = folder_mapper(full_path=main_folder)
    copy_folder_content = folder_mapper(full_path=copy_folder)

    return content_comparator(main_folder_content, copy_folder_content)


def resolve_path(path: str) -> Path:
    """Un chemin relatif est calculé à partir de la racine du projet, pas du dossier courant."""
    folder = Path(path)
    return folder if folder.is_absolute() else PROJECT_ROOT / folder


def load_config(config_path: Path = CONFIG_PATH) -> tuple[str, str]:
    """
    Lit le fichier de configuration et renvoie (dossier_principal, copy_folder).

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
    for key in ("dossier_principal", "copy_folder"):
        if not config.get(key):
            sys.exit(f"Erreur : la clé '{key}' est absente ou vide dans {config_path.name}.")

    main_folder = resolve_path(config["dossier_principal"])
    copy_folder = resolve_path(config["copy_folder"])

    if not main_folder.is_dir():
        sys.exit(f"Erreur : le dossier principal n'existe pas ({main_folder}).")
    if not copy_folder.is_dir():
        sys.exit(f"Erreur : le dossier copie n'existe pas ({copy_folder}).")
    if main_folder.resolve() == copy_folder.resolve():
        sys.exit(f"Erreur : le dossier principal et le dossier copie sont le même dossier ({main_folder}).")

    return main_folder.as_posix(), copy_folder.as_posix()


if __name__ == "__main__":
    MAIN_FOLDER, COPY_FOLDER = load_config()
    result = compare_folder(main_folder=MAIN_FOLDER, copy_folder=COPY_FOLDER)

    if result["is_folder_identical"]:
        print(f"OK : {COPY_FOLDER} contient tout le contenu de {MAIN_FOLDER}.")
    else:
        print(f"{len(result['missing_content'])} élément(s) de {MAIN_FOLDER} absent(s) de {COPY_FOLDER} :")
        for item in result["missing_content"]:
            print(f"  - {item}")
        # Code de sortie 1 pour signaler qu'il manque des éléments
        sys.exit(1)
