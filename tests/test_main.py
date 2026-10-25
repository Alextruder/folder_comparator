"""Tests de bout en bout du programme (R4, R11, R15 à R18)."""

from pathlib import Path

import pytest

from folder_comparator.__main__ import PROJECT_ROOT, run
from tests.conftest import MakeFiles

EXAMPLE_BASE = ["IMG_0001.csr", "notes.txt", "Mariage/IMG_0002.csr", "Mariage/IMG_0003.csr"]
EXAMPLE_RETOUCHE = ["img_0001.PSD", "IMG_0001-Edit.psd", "mariage/IMG_0002.psd"]


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def snapshot(folder: Path) -> dict[str, float]:
    return {str(p): p.stat().st_mtime for p in folder.rglob("*")}


def test_r11_exemple_complet(project: Path, make_files: MakeFiles) -> None:
    make_files(project.parent / "BASE", EXAMPLE_BASE)
    make_files(project.parent / "RETOUCHE", EXAMPLE_RETOUCHE)

    run(project)

    scraping = project / ".scraping"
    assert read_lines(scraping / "in.txt") == [
        "IMG_0001.csr",
        "Mariage/IMG_0002.csr",
        "Mariage/IMG_0003.csr",
    ]
    assert read_lines(scraping / "out.txt") == [
        "IMG_0001-Edit.psd",
        "img_0001.PSD",
        "mariage/IMG_0002.psd",
    ]
    assert read_lines(scraping / "diff.txt") == ["Mariage/IMG_0003.csr"]


def test_r15_resume_console(
    project: Path, make_files: MakeFiles, capsys: pytest.CaptureFixture[str]
) -> None:
    make_files(project.parent / "BASE", EXAMPLE_BASE)
    make_files(project.parent / "RETOUCHE", EXAMPLE_RETOUCHE)

    run(project)

    out = capsys.readouterr().out
    assert "BASE     : 3 fichiers .csr" in out
    assert "RETOUCHE : 3 fichiers .psd" in out
    assert "Manquants : 1" in out
    assert str(project / ".scraping" / "diff.txt") in out


def test_r18_code_1_si_manquants(project: Path, make_files: MakeFiles) -> None:
    make_files(project.parent / "BASE", ["a.csr"])

    assert run(project) == 1


def test_r18_code_0_si_tout_est_retouche(project: Path, make_files: MakeFiles) -> None:
    make_files(project.parent / "BASE", ["a.csr"])
    make_files(project.parent / "RETOUCHE", ["A.psd"])

    assert run(project) == 0


def test_r4_r18_erreur_de_config_code_2_et_rien_n_est_ecrit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(tmp_path) == 2

    assert "config.toml" in capsys.readouterr().err
    assert not (tmp_path / ".scraping").exists()


def test_r16_base_et_retouche_inchanges(project: Path, make_files: MakeFiles) -> None:
    base = project.parent / "BASE"
    retouche = project.parent / "RETOUCHE"
    make_files(base, EXAMPLE_BASE)
    make_files(retouche, EXAMPLE_RETOUCHE)
    before = (snapshot(base), snapshot(retouche))

    run(project)

    assert (snapshot(base), snapshot(retouche)) == before


def test_r17_lance_depuis_un_autre_dossier(
    project: Path, make_files: MakeFiles, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    make_files(project.parent / "BASE", ["a.csr"])
    elsewhere = tmp_path / "ailleurs"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    run(project)

    assert read_lines(project / ".scraping" / "diff.txt") == ["a.csr"]
    assert not (elsewhere / ".scraping").exists()


def test_r17_racine_du_projet_contient_le_package() -> None:
    assert (PROJECT_ROOT / "folder_comparator" / "__main__.py").is_file()
    assert (PROJECT_ROOT / "config_template.toml").is_file()
