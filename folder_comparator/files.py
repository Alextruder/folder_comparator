"""Accès au disque : collecte des fichiers (R5, R6) et écriture des rapports (R11 à R13)."""

from pathlib import Path


def collect_files(root: Path, extension: str) -> list[str]:
    """Chemins relatifs à root, avec /, des fichiers ayant l'extension donnée, triés (R12)."""
    found = [
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.suffix.lower() == extension and path.is_file()
    ]
    return sorted(found, key=str.casefold)


def write_reports(
    output_dir: Path, base_files: list[str], retouche_files: list[str], missing: list[str]
) -> None:
    """Écrit in.txt, out.txt et diff.txt, en écrasant les versions précédentes (R13)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, lines in (("in.txt", base_files), ("out.txt", retouche_files), ("diff.txt", missing)):
        content = "".join(f"{line}\n" for line in lines)
        (output_dir / name).write_text(content, encoding="utf-8", newline="\n")
