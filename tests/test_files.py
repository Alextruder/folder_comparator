"""Tests de la collecte (R5, R6) et de l'écriture des rapports (R11 à R13)."""

from pathlib import Path

from folder_comparator.files import collect_files, write_reports
from tests.conftest import MakeFiles


def test_r5_parcours_recursif(tmp_path: Path, make_files: MakeFiles) -> None:
    make_files(tmp_path, ["a.csr", "Mariage/b.csr", "Mariage/Eglise/Entree/c.csr"])

    assert collect_files(tmp_path, ".csr") == [
        "a.csr",
        "Mariage/b.csr",
        "Mariage/Eglise/Entree/c.csr",
    ]


def test_r6_seule_l_extension_configuree_est_retenue(tmp_path: Path, make_files: MakeFiles) -> None:
    make_files(
        tmp_path,
        [
            "IMG_0001.csr",
            "IMG_0002.CSR",
            "notes.txt",
            "sans_extension",
            "IMG_0003.csr.bak",
            ".csr",
            "dossier.csr/",
            "Vide/",
        ],
    )

    assert collect_files(tmp_path, ".csr") == ["IMG_0001.csr", "IMG_0002.CSR"]


def test_r12_tri_sans_casse_et_separateur_slash(tmp_path: Path, make_files: MakeFiles) -> None:
    make_files(tmp_path, ["c.csr", "B.csr", "a.csr", "Z/x.csr", "y/x.csr"])

    assert collect_files(tmp_path, ".csr") == ["a.csr", "B.csr", "c.csr", "y/x.csr", "Z/x.csr"]


def test_r11_r12_trois_fichiers_une_ligne_par_fichier(tmp_path: Path) -> None:
    output = tmp_path / ".scraping"

    write_reports(output, ["Mariage/é.csr", "a.csr"], ["a.psd"], ["Mariage/é.csr"])

    assert (output / "in.txt").read_text(encoding="utf-8") == "Mariage/é.csr\na.csr\n"
    assert (output / "out.txt").read_text(encoding="utf-8") == "a.psd\n"
    assert (output / "diff.txt").read_text(encoding="utf-8") == "Mariage/é.csr\n"


def test_r11_liste_vide_donne_un_fichier_vide(tmp_path: Path) -> None:
    write_reports(tmp_path, ["a.csr"], ["a.psd"], [])

    assert (tmp_path / "diff.txt").read_text(encoding="utf-8") == ""


def test_r13_fichiers_ecrases_a_chaque_lancement(tmp_path: Path) -> None:
    write_reports(tmp_path, ["a.csr", "b.csr"], [], ["a.csr", "b.csr"])
    write_reports(tmp_path, ["c.csr"], ["c.psd"], [])

    assert (tmp_path / "in.txt").read_text(encoding="utf-8") == "c.csr\n"
    assert (tmp_path / "out.txt").read_text(encoding="utf-8") == "c.psd\n"
    assert (tmp_path / "diff.txt").read_text(encoding="utf-8") == ""
