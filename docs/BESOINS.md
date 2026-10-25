# Besoins

Ce document est la **référence fonctionnelle** du projet. Tout comportement du programme doit
s'y rattacher à une règle numérotée. Une règle ne change qu'après validation du propriétaire du
projet, et le changement est consigné dans le [journal des décisions](#journal-des-décisions).

## Contexte

Un photographe travaille avec deux dossiers :

- **BASE** : les photos brutes, avec une extension donnée (par exemple `.csr`). Ce dossier contient
  aussi des sous-dossiers et des fichiers d'autres extensions, sans intérêt pour la vérification.
- **RETOUCHE** : les photos retouchées, avec une autre extension (par exemple `.psd`).

## Besoin

> En tant que photographe, je veux vérifier que chaque fichier `BASE_FILE_EXTENSION` du dossier
> `BASE_PATH` a sa version retouchée, avec l'extension `RETOUCHE_FILE_EXTENSION`, dans le dossier
> `RETOUCHE_PATH`.

## Règles (V1)

### Configuration

- **R1** : la configuration est lue dans le fichier `config.toml`, à la racine du projet. Il
  contient quatre clés obligatoires :
  - `BASE_PATH` : chemin du dossier BASE ;
  - `RETOUCHE_PATH` : chemin du dossier RETOUCHE ;
  - `BASE_FILE_EXTENSION` : une seule extension, par exemple `"csr"` ;
  - `RETOUCHE_FILE_EXTENSION` : une seule extension, par exemple `"psd"`.
- **R2** : une extension s'écrit avec ou sans point (`"csr"` ou `".csr"`), et sa casse est
  ignorée.
- **R3** : le fichier `config_template.toml` est versionné et documente chaque clé. `config.toml`
  n'est jamais versionné : il est listé dans le `.gitignore`.
- **R4** : si `config.toml` est absent, si une clé manque ou si un des dossiers n'existe pas, le
  programme s'arrête avec un message clair en français, sans rien écrire.

### Collecte

- **R5** : le programme parcourt BASE et RETOUCHE récursivement, sous-dossiers compris.
- **R6** : seuls les fichiers dont l'extension correspond à celle configurée pour leur dossier sont
  retenus. Tout le reste est ignoré : autres extensions, fichiers sans extension, dossiers.

### Comparaison

- **R7** : un fichier de BASE est **présent** si RETOUCHE contient un fichier au **même chemin
  relatif**, avec le **même nom**, où seule l'extension change.
  `BASE/Mariage/IMG_0001.csr` est présent si `RETOUCHE/Mariage/IMG_0001.psd` existe.
- **R8** : la casse est ignorée dans les noms de dossiers comme dans les noms de fichiers.
  `BASE/Mariage/IMG_0001.csr` est présent si `RETOUCHE/mariage/img_0001.PSD` existe.
- **R9** : un nom modifié n'est pas une correspondance. `IMG_0001-Edit.psd` ou `IMG_0001_v2.psd`
  ne valident pas `IMG_0001.csr`.
- **R10** : la comparaison se fait dans un seul sens, de BASE vers RETOUCHE. Un fichier présent
  uniquement dans RETOUCHE n'est pas signalé.

### Sorties

- **R11** : le programme écrit trois fichiers dans le dossier `.scraping/`, à la racine du
  projet :
  - `in.txt` : les fichiers retenus dans BASE (R6) ;
  - `out.txt` : les fichiers retenus dans RETOUCHE (R6) ;
  - `diff.txt` : les fichiers de BASE absents de RETOUCHE (R7 à R10), avec leur nom BASE.
- **R12** : chaque fichier contient une ligne par fichier, en chemin relatif au dossier racine
  concerné, avec `/` comme séparateur quel que soit le système, en UTF-8 et triée par ordre
  alphabétique.
- **R13** : les trois fichiers sont écrasés à chaque lancement, sans historique.
- **R14** : le dossier `.scraping/` existe dès le clonage du dépôt, grâce à `.scraping/.gitkeep`.
  Son contenu n'est jamais versionné.
- **R15** : en fin d'exécution, le programme affiche un résumé dans la console : nombre de fichiers
  dans BASE, nombre dans RETOUCHE, nombre de manquants, et chemin de `diff.txt`.

### Sécurité

- **R16** : le programme ne crée, ne modifie, ne déplace et ne supprime **jamais** rien dans BASE
  ni dans RETOUCHE. Il n'écrit que dans `.scraping/`.

## Contraintes

- **C1** : il se lance avec `python -m folder_comparator`, depuis la racine du projet.
- **C2** : il fonctionne avec Python 3.13, sur Windows et macOS.
- **C3** : le programme n'a aucune dépendance en dehors de la bibliothèque standard.

## Hors V1 (pistes pour plus tard)

- Exclure des sous-dossiers de la vérification (V2 envisagée).
- Accepter plusieurs extensions RETOUCHE.
- Tolérer des suffixes de retouche (`-Edit`, `_v2`…).

## Journal des décisions

| Date | Décision |
|---|---|
| 2026-10-25 | Le dépôt est repris de zéro. |
| 2026-10-25 | La comparaison se fait par chemin relatif identique (R7), sans tenir compte de la casse (R8). |
| 2026-10-25 | Le nom doit être strictement identique, seule l'extension change : un suffixe de retouche ne compte pas (R9). |
| 2026-10-25 | En V1, une seule extension pour BASE et une seule pour RETOUCHE (R1). |
| 2026-10-25 | La configuration est en TOML : `config.toml` est ignoré par git, `config_template.toml` est versionné (R1, R3). |
| 2026-10-25 | Les sorties vont dans `.scraping/` (`in.txt`, `out.txt`, `diff.txt`), qui est écrasé à chaque lancement (R11 à R14). |
| 2026-10-25 | Interface : `python -m`, principe KISS. Plateformes : Windows et macOS, Python 3.13 (C1, C2). |
