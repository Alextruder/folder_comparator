# CLAUDE.md

Guide de travail pour l'IA sur ce dépôt. À lire en entier avant toute action.

## Le projet

`folder_comparator` vérifie que chaque photo brute d'un dossier BASE a sa version retouchée dans
un dossier RETOUCHE. Lancement : `python -m folder_comparator`.

## À lire avant d'agir

1. [`docs/BESOINS.md`](docs/BESOINS.md) : les règles numérotées `Rn`, la seule référence
   fonctionnelle.
2. [`docs/PRINCIPES.md`](docs/PRINCIPES.md) : comment on code ici (KISS, test d'abord, logique
   pure, langue).

Si une demande contredit BESOINS.md ou n'y figure pas, **le signaler et demander** avant de coder.

## Commandes

Environnement : Python 3.13, dans un environnement virtuel activé.

```bash
python -m venv .venv            # une seule fois
# Windows : .venv\Scripts\activate    macOS : source .venv/bin/activate
pip install -r requirements-dev.txt

ruff format .                   # formatage
ruff check .                    # lint
mypy                            # typage (configuré dans pyproject.toml)
pytest                          # tests
python -m folder_comparator     # lancer le programme (nécessite config.toml)
```

## Façon de travailler

| Type de demande | Skill à suivre | Autonomie |
|---|---|---|
| Nouvelle fonctionnalité ou règle modifiée | `nouvelle-fonctionnalite` | **Plan d'abord, puis attendre la validation** avant de coder |
| Correction de bug | `correction` | Autonome jusqu'à la PR |
| Vérifier que tout est vert | `verifier` | Autonome |

## Définition de « terminé »

Un changement est terminé quand :

- [ ] il se rattache à une règle de BESOINS.md, et BESOINS.md est à jour (journal des décisions
      compris) ;
- [ ] chaque règle touchée a un test qui cite son numéro ;
- [ ] `ruff format --check .`, `ruff check .`, `mypy` et `pytest` passent (skill `verifier`) ;
- [ ] `README.md` est à jour si le comportement visible change ;
- [ ] le commit est en français, sur une branche dédiée, jamais sur `main`.

## Interdits

- Modifier ou créer `config.toml` : c'est le fichier personnel de l'utilisateur. On modifie
  `config_template.toml`.
- Versionner le contenu de `.scraping/` (seul `.scraping/.gitkeep` l'est).
- Écrire dans les dossiers BASE ou RETOUCHE, y compris dans les tests (on utilise `tmp_path`).
- Ajouter une dépendance au programme (bibliothèque standard uniquement).
- Committer sur `main`, faire un `git push --force`, réécrire l'historique.
- Désactiver, sauter ou affaiblir un test pour obtenir du vert.
- Coder une fonctionnalité de la section « Hors V1 » sans validation.

## Garde-fous automatiques

Ils sont configurés dans `.claude/settings.json` et exécutés par le harnais, pas par l'IA :

- après chaque modification d'un `.py` : `ruff format` et `ruff check --fix` ;
- avant chaque action : sont bloqués toute écriture dans `config.toml`, tout `git push --force` et
  tout commit ou push sur `main` ;
- en fin de tour, si du code a changé : lint, typage et tests. Si c'est rouge, l'IA doit corriger
  avant de rendre la main ;
- au démarrage d'une session cloud : installation de `requirements-dev.txt`.

La CI GitHub (`.github/workflows/ci.yml`) relance les mêmes vérifications sur Windows et macOS à
chaque PR.

## Structure

```
folder_comparator/   le programme (package lancé par python -m)
tests/               les tests pytest
docs/                BESOINS.md et PRINCIPES.md
.scraping/           sorties du programme (non versionnées, sauf .gitkeep)
.claude/             harnais de l'IA : settings.json, hooks/, skills/
```
