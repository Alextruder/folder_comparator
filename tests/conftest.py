"""Outils communs aux tests : construction d'arborescences dans tmp_path."""

from collections.abc import Callable, Iterable
from pathlib import Path

import pytest

MakeFiles = Callable[[Path, Iterable[str]], None]


def _make_files(root: Path, relative_paths: Iterable[str]) -> None:
    """Crée des fichiers vides ; un chemin terminé par / crée un dossier."""
    for relative in relative_paths:
        path = root / relative
        if relative.endswith("/"):
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()


@pytest.fixture
def make_files() -> MakeFiles:
    return _make_files


def write_config(project_root: Path, values: dict[str, str]) -> None:
    """Écrit un config.toml de test à la racine d'un faux projet."""
    lines = [f"{key} = {_toml_string(value)}" for key, value in values.items()]
    (project_root / "config.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _toml_string(value: str) -> str:
    return '"' + value.replace("\\", "/").replace('"', '\\"') + '"'


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """Faux projet : racine avec config.toml valide, dossiers BASE et RETOUCHE vides."""
    root = tmp_path / "projet"
    base = tmp_path / "BASE"
    retouche = tmp_path / "RETOUCHE"
    for folder in (root, base, retouche):
        folder.mkdir()
    write_config(
        root,
        {
            "BASE_PATH": str(base),
            "RETOUCHE_PATH": str(retouche),
            "BASE_FILE_EXTENSION": "csr",
            "RETOUCHE_FILE_EXTENSION": "psd",
        },
    )
    return root
