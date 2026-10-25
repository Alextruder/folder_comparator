# Principes

Ces principes s'appliquent à tout le monde, humains comme IA.

## 1. KISS : faire simple

- On écrit la solution la plus simple qui satisfait les règles de [BESOINS.md](BESOINS.md).
- Pas d'abstraction « pour plus tard », pas d'option que personne n'a demandée.
- On n'ajoute pas de classe quand une fonction suffit, ni de module quand un fichier suffit.

## 2. Les besoins d'abord

- Tout comportement se rattache à une règle `Rn` de BESOINS.md.
- Un besoin nouveau ou modifié s'écrit **d'abord** dans BESOINS.md et doit être validé avant d'être
  codé.
- En cas de doute sur l'interprétation d'une règle, on pose la question plutôt que de deviner.

## 3. Test d'abord

- Chaque règle est couverte par au moins un test, dont le nom ou la docstring cite la règle
  (`test_r8_casse_ignoree`).
- Pour une nouvelle règle, on écrit le test qui échoue, puis le code qui le fait passer.
- Pour un bug, on écrit d'abord le test qui reproduit le bug.
- Les tests créent leurs arborescences dans un dossier temporaire (`tmp_path`) et n'utilisent
  jamais de vrais dossiers de photos.

## 4. Logique pure, entrées/sorties à part

- La comparaison est une fonction pure : des chemins en entrée, des chemins en sortie, sans accès
  au disque.
- La lecture du disque, l'écriture des fichiers et l'affichage sont isolés dans de petites
  fonctions séparées.
- Le résultat est facile à tester et à raisonner.

## 5. Ne jamais toucher aux photos

- Le programme ne fait que **lire** BASE et RETOUCHE (R16).
- Toute écriture se fait dans `.scraping/`.

## 6. Portabilité Windows et macOS

- On manipule les chemins avec `pathlib`, jamais en concaténant des chaînes.
- Les deux systèmes ignorent la casse des noms de fichiers : on ne compte pas sur la casse pour
  distinguer deux fichiers.
- Les fichiers de sortie sont en UTF-8 et utilisent `/` comme séparateur (R12).

## 7. Bibliothèque standard uniquement

- Le programme n'a aucune dépendance (C3).
- Les outils de développement (pytest, ruff, mypy) sont listés dans `requirements-dev.txt` et
  n'entrent jamais dans le code livré.
- Ajouter une dépendance exige une justification écrite et une validation.

## 8. Petits pas

- Une branche ou une PR = une seule fonctionnalité ou une seule correction.
- Chaque commit laisse le projet vert : lint, typage et tests passent.
- Le README et BESOINS.md sont mis à jour dans le même changement que le code.

## 9. Langue

- Documentation, README, messages du programme et messages de commit : **français**.
- Code (noms de variables, fonctions, modules) : **anglais**.
- Commentaires et docstrings : français.
