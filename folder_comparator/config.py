"""Lecture et validation de config.toml (R1, R2, R4)."""

import tomllib
from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """Configuration invalide : le message est destiné à l'utilisateur, en français."""


@dataclass(frozen=True)
class Config:
    base_path: Path
    retouche_path: Path
    base_extension: str
    retouche_extension: str


def normalize_extension(value: str) -> str:
    """Ramène "csr", ".CSR"... à ".csr" (R2). Renvoie "" si l'extension est vide."""
    extension = value.strip().lstrip(".").lower()
    return f".{extension}" if extension else ""


def load_config(config_file: Path) -> Config:
    if not config_file.is_file():
        raise ConfigError(
            f"Fichier introuvable : {config_file}. "
            "Copier config_template.toml en config.toml, puis le remplir."
        )
    try:
        with config_file.open("rb") as handle:
            data = tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"{config_file} n'est pas un fichier TOML valide : {error}") from error

    return Config(
        base_path=_read_folder(data, "BASE_PATH"),
        retouche_path=_read_folder(data, "RETOUCHE_PATH"),
        base_extension=_read_extension(data, "BASE_FILE_EXTENSION"),
        retouche_extension=_read_extension(data, "RETOUCHE_FILE_EXTENSION"),
    )


def _read_text(data: dict[str, object], key: str) -> str:
    if key not in data:
        raise ConfigError(f"Clé manquante dans config.toml : {key}.")
    value = data[key]
    if not isinstance(value, str):
        raise ConfigError(f'{key} doit être du texte entre guillemets, par exemple {key} = "...".')
    return value


def _read_folder(data: dict[str, object], key: str) -> Path:
    folder = Path(_read_text(data, key))
    if not folder.is_dir():
        raise ConfigError(f"{key} : le dossier {folder} n'existe pas ou n'est pas un dossier.")
    return folder


def _read_extension(data: dict[str, object], key: str) -> str:
    extension = normalize_extension(_read_text(data, key))
    if not extension:
        raise ConfigError(f'{key} est vide : indiquer une extension, par exemple "csr".')
    return extension
