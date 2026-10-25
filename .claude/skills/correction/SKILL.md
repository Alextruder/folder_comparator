---
name: correction
description: Démarche pour corriger un bug de folder_comparator, c'est-à-dire un comportement qui ne respecte pas une règle existante de docs/BESOINS.md. Reproduire par un test, corriger, vérifier. Autonome jusqu'à la PR.
---

# Correction de bug

Un bug est un écart entre le programme et une règle **existante** de `docs/BESOINS.md`. Si
corriger le problème demande de changer une règle, ce n'est pas un bug : utiliser le skill
`nouvelle-fonctionnalite`.

## 1. Identifier la règle

- Trouver dans `docs/BESOINS.md` la règle `Rn` qui n'est pas respectée.
- Si aucune règle ne couvre le cas, s'arrêter et demander.

## 2. Reproduire

- Écrire un test dans `tests/` qui reproduit le bug et cite la règle (`test_r8_...`), avec
  `tmp_path`.
- Lancer `pytest` et constater qu'il **échoue**.

## 3. Corriger

- Faire la correction minimale qui fait passer le test.
- Ne pas en profiter pour refactorer ou ajouter autre chose.

## 4. Vérifier

- Suivre le skill `verifier`.

## 5. Livrer

- Committer en français (`Correction R8 : ...`) sur une branche dédiée.
- Pousser et ouvrir une PR qui décrit le bug, la règle et le test ajouté.
