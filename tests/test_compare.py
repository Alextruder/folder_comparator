"""Tests de la comparaison pure (R7 à R10)."""

from folder_comparator.compare import find_missing


def test_r7_meme_chemin_meme_nom_autre_extension() -> None:
    assert find_missing(["Mariage/IMG_0001.csr"], ["Mariage/IMG_0001.psd"]) == []


def test_r7_meme_nom_dans_un_autre_dossier_est_manquant() -> None:
    assert find_missing(["Mariage/IMG_0001.csr"], ["Bapteme/IMG_0001.psd"]) == [
        "Mariage/IMG_0001.csr"
    ]


def test_r7_fichier_a_la_racine_contre_sous_dossier() -> None:
    assert find_missing(["IMG_0001.csr"], ["Mariage/IMG_0001.psd"]) == ["IMG_0001.csr"]


def test_r7_point_dans_le_nom_seule_la_derniere_extension_change() -> None:
    assert find_missing(["IMG.0001.csr"], ["IMG.0001.psd"]) == []
    assert find_missing(["IMG.0001.csr"], ["IMG.psd"]) == ["IMG.0001.csr"]


def test_r8_casse_ignoree_dossiers_et_fichiers() -> None:
    assert find_missing(["Mariage/IMG_0001.csr"], ["mariage/img_0001.PSD"]) == []


def test_r9_nom_modifie_n_est_pas_une_correspondance() -> None:
    retouches = ["IMG_0001-Edit.psd", "IMG_0001_v2.psd", "IMG_00011.psd"]
    assert find_missing(["IMG_0001.csr"], retouches) == ["IMG_0001.csr"]


def test_r10_retouche_sans_brut_non_signalee() -> None:
    assert find_missing(["IMG_0001.csr"], ["IMG_0001.psd", "IMG_9999.psd"]) == []


def test_r10_garde_l_ordre_et_le_nom_base() -> None:
    base = ["A.csr", "Mariage/B.csr", "Mariage/C.csr"]
    assert find_missing(base, ["mariage/b.psd"]) == ["A.csr", "Mariage/C.csr"]
