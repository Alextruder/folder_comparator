"""Point d'entrée : python -m folder_comparator."""

import sys
from pathlib import Path

from folder_comparator.compare import find_missing
from folder_comparator.config import ConfigError, load_config
from folder_comparator.files import collect_files, write_reports

# Dossier qui contient le package : on y cherche config.toml et .scraping/ (R17).
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run(project_root: Path) -> int:
    """Lance la vérification et renvoie le code de sortie (R18)."""
    try:
        config = load_config(project_root / "config.toml")
    except ConfigError as error:
        print(f"Erreur de configuration : {error}", file=sys.stderr)
        return 2

    base_files = collect_files(config.base_path, config.base_extension)
    retouche_files = collect_files(config.retouche_path, config.retouche_extension)
    missing = find_missing(base_files, retouche_files)

    output_dir = project_root / ".scraping"
    write_reports(output_dir, base_files, retouche_files, missing)

    print(f"BASE     : {len(base_files)} fichiers {config.base_extension}")
    print(f"RETOUCHE : {len(retouche_files)} fichiers {config.retouche_extension}")
    print(f"Manquants : {len(missing)} -> voir {output_dir / 'diff.txt'}")
    return 1 if missing else 0


def main() -> int:
    return run(PROJECT_ROOT)


if __name__ == "__main__":
    sys.exit(main())
