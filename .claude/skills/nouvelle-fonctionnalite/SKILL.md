---
name: nouvelle-fonctionnalite
description: Démarche obligatoire pour ajouter ou modifier une fonctionnalité, une règle métier ou un comportement visible de folder_comparator. Plan d'abord, validation de l'utilisateur, puis test d'abord. À utiliser dès qu'une demande n'est pas une simple correction de bug.
---

# Nouvelle fonctionnalité

Ne jamais écrire de code applicatif avant l'étape 3.

## 1. Comprendre

- Lire `docs/BESOINS.md` et `docs/PRINCIPES.md`.
- Identifier les règles `Rn` concernées, existantes ou à créer.
- Si la demande touche la section « Hors V1 », contredit une règle ou reste ambiguë : poser la
  question et s'arrêter.

## 2. Proposer un plan, puis attendre

Présenter à l'utilisateur, brièvement :

- les règles ajoutées ou modifiées, rédigées comme elles figureront dans BESOINS.md ;
- les exemples concrets d'entrée et de sortie ;
- les fichiers qui vont changer ;
- les tests prévus, avec une ligne par règle.

**S'arrêter et attendre une validation explicite.** Une absence de réponse n'est pas une
validation.

## 3. Écrire les besoins

- Mettre à jour `docs/BESOINS.md` : les règles, plus une ligne datée dans le journal des
  décisions.

## 4. Test d'abord

- Écrire les tests dans `tests/`, en nommant la règle (`test_r7_...`).
- Construire les arborescences avec `tmp_path`, jamais avec de vrais dossiers.
- Lancer `pytest` et constater que les nouveaux tests **échouent** pour la bonne raison.

## 5. Coder

- Implémenter le minimum pour faire passer les tests (KISS).
- Garder la comparaison pure et isoler les accès au disque.
- Bibliothèque standard uniquement.

## 6. Vérifier et documenter

- Suivre le skill `verifier` jusqu'à ce que tout soit vert.
- Mettre à jour `README.md` si l'utilisateur final voit une différence.
- Mettre à jour `config_template.toml` si une clé de configuration change.

## 7. Livrer

- Committer en français sur une branche dédiée, en citant les règles (`R7, R8 : ...`).
- Pousser et ouvrir une PR qui liste les règles couvertes et les tests associés.
