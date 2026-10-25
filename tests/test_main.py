"""Test provisoire du squelette, à remplacer par les tests de la V1."""

from folder_comparator.__main__ import main


def test_squelette_main_signale_v1_en_cours() -> None:
    assert main() == 1
