"""Tests de la lecture de config.toml (R1, R2, R4)."""

from pathlib import Path

import pytest

from folder_comparator.config import ConfigError, load_config, normalize_extension
from tests.conftest import write_config

KEYS = ["BASE_PATH", "RETOUCHE_PATH", "BASE_FILE_EXTENSION", "RETOUCHE_FILE_EXTENSION"]


@pytest.fixture
def folders(tmp_path: Path) -> tuple[Path, Path]:
    base = tmp_path / "BASE"
    retouche = tmp_path / "RETOUCHE"
    base.mkdir()
    retouche.mkdir()
    return base, retouche


def valid_values(base: Path, retouche: Path) -> dict[str, str]:
    return {
        "BASE_PATH": str(base),
        "RETOUCHE_PATH": str(retouche),
        "BASE_FILE_EXTENSION": "csr",
        "RETOUCHE_FILE_EXTENSION": "psd",
    }


def test_r1_config_valide_lue(tmp_path: Path, folders: tuple[Path, Path]) -> None:
    base, retouche = folders
    write_config(tmp_path, valid_values(base, retouche))

    config = load_config(tmp_path / "config.toml")

    assert config.base_path == base
    assert config.retouche_path == retouche
    assert config.base_extension == ".csr"
    assert config.retouche_extension == ".psd"


@pytest.mark.parametrize("value", ["csr", ".csr", "CSR", ".CSR", " csr "])
def test_r2_extension_avec_ou_sans_point_et_casse_ignoree(value: str) -> None:
    assert normalize_extension(value) == ".csr"


def test_r4_fichier_absent(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="config.toml"):
        load_config(tmp_path / "config.toml")


def test_r4_toml_invalide(tmp_path: Path) -> None:
    (tmp_path / "config.toml").write_text("BASE_PATH = \n", encoding="utf-8")

    with pytest.raises(ConfigError, match="TOML"):
        load_config(tmp_path / "config.toml")


@pytest.mark.parametrize("missing_key", KEYS)
def test_r4_cle_manquante(tmp_path: Path, folders: tuple[Path, Path], missing_key: str) -> None:
    values = valid_values(*folders)
    del values[missing_key]
    write_config(tmp_path, values)

    with pytest.raises(ConfigError, match=missing_key):
        load_config(tmp_path / "config.toml")


def test_r4_valeur_qui_n_est_pas_du_texte(tmp_path: Path, folders: tuple[Path, Path]) -> None:
    base, retouche = folders
    (tmp_path / "config.toml").write_text(
        f'BASE_PATH = "{base.as_posix()}"\n'
        f'RETOUCHE_PATH = "{retouche.as_posix()}"\n'
        'BASE_FILE_EXTENSION = "csr"\n'
        'RETOUCHE_FILE_EXTENSION = ["psd", "jpg"]\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="RETOUCHE_FILE_EXTENSION"):
        load_config(tmp_path / "config.toml")


@pytest.mark.parametrize("empty", ["", ".", "  "])
def test_r4_extension_vide(tmp_path: Path, folders: tuple[Path, Path], empty: str) -> None:
    values = valid_values(*folders)
    values["BASE_FILE_EXTENSION"] = empty
    write_config(tmp_path, values)

    with pytest.raises(ConfigError, match="BASE_FILE_EXTENSION"):
        load_config(tmp_path / "config.toml")


def test_r4_dossier_inexistant(tmp_path: Path, folders: tuple[Path, Path]) -> None:
    values = valid_values(*folders)
    values["RETOUCHE_PATH"] = str(tmp_path / "absent")
    write_config(tmp_path, values)

    with pytest.raises(ConfigError, match="RETOUCHE_PATH"):
        load_config(tmp_path / "config.toml")


def test_r4_chemin_qui_est_un_fichier(tmp_path: Path, folders: tuple[Path, Path]) -> None:
    a_file = tmp_path / "photo.csr"
    a_file.touch()
    values = valid_values(*folders)
    values["BASE_PATH"] = str(a_file)
    write_config(tmp_path, values)

    with pytest.raises(ConfigError, match="BASE_PATH"):
        load_config(tmp_path / "config.toml")
