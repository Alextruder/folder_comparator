"""Comparaison pure entre BASE et RETOUCHE, sans accès au disque (R7 à R10)."""

from pathlib import PurePosixPath


def _match_key(relative_path: str) -> str:
    """Chemin sans sa dernière extension, sans tenir compte de la casse (R7, R8)."""
    return str(PurePosixPath(relative_path).with_suffix("")).casefold()


def find_missing(base_files: list[str], retouche_files: list[str]) -> list[str]:
    """Fichiers de BASE sans retouche, dans l'ordre de base_files et avec leur nom BASE."""
    retouched = {_match_key(path) for path in retouche_files}
    return [path for path in base_files if _match_key(path) not in retouched]
