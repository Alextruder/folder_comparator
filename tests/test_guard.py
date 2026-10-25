"""Tests du garde-fou .claude/hooks/guard.py (voir CLAUDE.md, section Interdits)."""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

GUARD_FILE = Path(__file__).resolve().parent.parent / ".claude" / "hooks" / "guard.py"


def _load_guard() -> ModuleType:
    spec = importlib.util.spec_from_file_location("guard", GUARD_FILE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = _load_guard()


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "projet"
    root.mkdir()
    return root.resolve()


def blocked(command: str, project: Path, cwd: Path | None = None, branch: str = "dev") -> bool:
    protected = project / "config.toml"
    return guard.check_command(command, cwd or project, protected, branch) is not None


# --- config.toml du projet : outils Edit / Write ---


def test_ecrire_config_du_projet_est_bloque(project: Path) -> None:
    protected = project / "config.toml"
    assert guard.check_file(str(protected), project, protected) is not None
    assert guard.check_file(str(project / "CONFIG.TOML"), project, protected) is not None


def test_ecrire_un_autre_config_toml_est_autorise(project: Path, tmp_path: Path) -> None:
    protected = project / "config.toml"
    assert guard.check_file(str(tmp_path / "copie" / "config.toml"), project, protected) is None
    assert guard.check_file(str(project / "config_template.toml"), project, protected) is None


# --- config.toml du projet : commandes shell ---


@pytest.mark.parametrize(
    "command",
    [
        "echo x > config.toml",
        "echo x >> config.toml",
        "echo x >config.toml",
        'echo x > "config.toml"',
        "cp config_template.toml config.toml",
        "mv autre.toml config.toml",
        "echo x | tee config.toml",
        "sed -i 's/a/b/' config.toml",
        "rm config.toml",
        "touch config.toml",
        "python -c \"open('config.toml', 'w').write('x')\"",
        "echo x > ./config.toml",
    ],
)
def test_commande_qui_ecrit_config_du_projet_est_bloquee(command: str, project: Path) -> None:
    assert blocked(command, project)


def test_chemin_absolu_vers_config_du_projet_est_bloque(project: Path, tmp_path: Path) -> None:
    assert blocked(f"cp a.toml {project / 'config.toml'}", project, cwd=tmp_path)


def test_cd_vers_le_projet_est_suivi(project: Path, tmp_path: Path) -> None:
    assert blocked(f"cd {project} && cp a.toml config.toml", project, cwd=tmp_path)


@pytest.mark.parametrize(
    "command",
    [
        "cat config.toml",
        "cp config_template.toml copie.toml",
        "sed -i 's/a/b/' config_template.toml",
        "git status",
    ],
)
def test_commande_sans_ecriture_de_config_est_autorisee(command: str, project: Path) -> None:
    assert not blocked(command, project)


def test_config_toml_hors_du_projet_est_autorise(project: Path, tmp_path: Path) -> None:
    assert not blocked("cp config_template.toml copie/config.toml", project)
    assert not blocked(f"cd {tmp_path} && echo x > config.toml", project)


# --- git ---


def test_push_force_est_bloque(project: Path) -> None:
    assert blocked("git push --force origin dev", project)
    assert blocked("git push -f origin dev", project)


def test_push_ou_commit_sur_main_est_bloque(project: Path) -> None:
    assert blocked("git push -u origin main", project)
    assert blocked("git push -u origin dev", project, branch="main")
    assert blocked("git commit -m 'x'", project, branch="main")


def test_push_et_commit_sur_branche_dediee_autorises(project: Path) -> None:
    assert not blocked("git push -u origin dev", project)
    assert not blocked("git commit -m 'x'", project)


def test_texte_du_message_de_commit_ignore(project: Path) -> None:
    assert not blocked("git commit -m 'garde-fou : push --force et main interdits'", project)
    assert not blocked("git commit -m 'ne plus écrire > config.toml'", project)


def test_limite_connue_ligne_du_message_commencant_par_git_push(project: Path) -> None:
    # Faux positif accepté (côté prudent) : le découpage par lignes ignore les guillemets.
    assert blocked("git commit -m 'titre\ngit push --force interdit'", project)
