---
name: verifier
description: Lance toutes les vérifications de folder_comparator (formatage, lint, typage, tests) et corrige jusqu'à ce que tout soit vert. À utiliser avant tout commit et avant de déclarer un travail terminé.
---

# Vérifier

Lancer depuis la racine du projet, avec l'environnement virtuel activé :

```bash
ruff format --check .
ruff check .
mypy
pytest
```

Ce sont exactement les commandes de la CI (`.github/workflows/ci.yml`).

## Si c'est rouge

- `ruff format --check` : lancer `ruff format .`.
- `ruff check` : corriger le code. `ruff check --fix .` règle les cas simples.
- `mypy` : corriger les types. Pas de `# type: ignore` sans commentaire qui le justifie.
- `pytest` : corriger le code, **pas le test**, sauf si le test contredit `docs/BESOINS.md`.
  Ne jamais sauter, désactiver ou affaiblir un test.

Relancer les quatre commandes jusqu'à ce que tout passe. Rapporter le résultat tel quel : si une
vérification reste rouge, le dire avec la sortie.

## Si un outil manque

`pip install -r requirements-dev.txt`, avec un environnement virtuel Python 3.13 activé.
