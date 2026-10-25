# Folder comparator

Vérifie que **chaque photo brute** d'un dossier a bien **sa version retouchée** dans un autre
dossier, et liste celles qui manquent.

```
D:/Photos/Bruts/              (BASE_PATH, extension "csr")
├── IMG_0001.csr
├── notes.txt                 <- ignoré : ce n'est pas un .csr
└── Mariage/
    ├── IMG_0002.csr
    └── IMG_0003.csr

E:/Photos/Retouches/          (RETOUCHE_PATH, extension "psd")
├── img_0001.psd
└── mariage/
    └── IMG_0002.psd

Résultat : Mariage/IMG_0003.csr est manquant.
```

## Règles de vérification

- Une photo brute est retrouvée si la retouche a le **même nom**, au **même endroit** (même
  sous-dossier), avec l'extension de retouche.
- Les **majuscules et minuscules** sont ignorées : `IMG_0001.csr` et `img_0001.PSD` correspondent.
- Le nom doit être **exactement le même** : `IMG_0001-Edit.psd` ne compte pas pour
  `IMG_0001.csr`.
- Les fichiers d'une autre extension sont ignorés.
- La vérification se fait dans **un seul sens** : une retouche sans brut n'est pas signalée.
- Le programme **ne modifie jamais** vos dossiers de photos : il ne fait que les lire.

## Installation

Il faut **Python 3.13** ([python.org](https://www.python.org/downloads/)). Aucune autre
installation n'est nécessaire.

```bash
git clone https://github.com/Alextruder/folder_comparator.git
cd folder_comparator
```

## Configuration

Copier `config_template.toml` en `config.toml`, puis remplir les quatre valeurs :

```toml
BASE_PATH = "D:/Photos/Bruts"
RETOUCHE_PATH = "E:/Photos/Retouches"
BASE_FILE_EXTENSION = "csr"
RETOUCHE_FILE_EXTENSION = "psd"
```

`config.toml` reste sur votre ordinateur : il n'est jamais envoyé sur GitHub.

## Utilisation

Depuis le dossier du projet :

```bash
python -m folder_comparator
```

Sur macOS, la commande peut s'appeler `python3`.

Un résumé s'affiche à la fin :

```
BASE     : 3 fichiers .csr
RETOUCHE : 3 fichiers .psd
Manquants : 1 -> voir D:/.../folder_comparator/.scraping/diff.txt
```

Trois fichiers sont écrits dans le dossier `.scraping/` :

| Fichier | Contenu |
|---|---|
| `in.txt` | Toutes les photos brutes trouvées |
| `out.txt` | Toutes les photos retouchées trouvées |
| `diff.txt` | Les photos brutes **sans retouche** : c'est la liste à traiter |

Ces fichiers sont remplacés à chaque lancement. Un chemin s'écrit toujours avec des `/`, relatif
au dossier BASE ou RETOUCHE.

En cas de problème de configuration (fichier absent, clé manquante, dossier introuvable…), un
message explique quoi corriger et rien n'est écrit.

Pour une utilisation dans un script, le code de sortie vaut `0` si tout est retouché, `1` s'il
manque des retouches et `2` en cas d'erreur de configuration.

## Développement

Les règles détaillées sont dans [`docs/BESOINS.md`](docs/BESOINS.md), les principes de code dans
[`docs/PRINCIPES.md`](docs/PRINCIPES.md), et le guide de travail de l'IA dans
[`CLAUDE.md`](CLAUDE.md).
