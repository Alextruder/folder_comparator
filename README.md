# Configuration du programme
## Poetry
### Installer Poetry
Pour installer Poetry, suivre ce [lien](https://python-poetry.org/docs/).

### Commandes basiques
1) Initialiser un nouvel environment vide: `poetry init`.
2) Générer le fichier lock à installer: `poetry lock`.
3) **Installer** l'environnement: `poetry install`. Il s'agit de la commande à utiliser pour pouvoir générer l'environnement pour lancer le code (les étapes précédentes ne sont pas nécessaires car les fichiers sont déjà générés).

## Le script
Il n'y a pas d'installation supplémentaire à réalise pour lancer le script. 

Pour lancer la comparaison, il faut:
1) Se placer dans le projet FOLDER_COMPARATOR 
2) Dans un terminal/cmd, lancer la commande suivante: `poetry run python main.py`


# Explication de bases en Python pour maintenir le script
## le f-string (ou string format)
Le f-string permet d'injecter une variable directement dans un string en ajoutant la lettre f devant une déclaration de string. 

Le f-string se présente de cette manière: `f"Le contenu de ma variable: {VARIABLE}"`.

Dans ce cadre, si on a `VARIABLE = "Bonjour"`, le résultat sera le suivant: 
`Le contenu de ma variable: Bonjour`

## La bibliothèque OS
La bibliothèque OS permet d'intéragir avec le système d'opération (Operating System) de la machine. Les cas d'utilisations les plus fréquents sont les suivants: 
- Ouvrir, fermer un fichier pour lire le contenu voire écrire dedans
- Récupérer des informations sur des fichiers ou des dossiers ou les modifier
- Créer, supprimer ou modifier les droits sur des fichiers ou des dossiers

## La concaténation de types
Dans le contexte général, on veut pouvoir concaténer des variables entres elles facilement. Il existe en général des fonctions verbeuses pour le faire, mais aussi des raccourcis.
- Pour les strings: il suffit juste de les "additionner"
```python
a = "Bonjour"
b = "Monde"
print(a+b)
```
Résultat: `BonjourMonde`
- Pour les listes, il est aussi possible de les concaténer. 
```python
a = ["a", "b", "c"]
b = ["c","d"]
c = a + b
print(f"c={c}")
d = [*a, *b]
print(f"c={a+b}")
```
Résultat:
```
c=["a", "b", "c", "c", "d"]
d=["a", "b", "c", "c", "d"]
```
A noter que pour enlever les duplicats, on peut faire un `list(set(c))` &rarr; `["a", "b", "c", "d"]`

L'inconvénient avec la 1ère méthode `list1 + list2` est qu'on ne peut concaténer que des listes entres elles, et non ajouter des strings dedans. 

L'avantage de la seconde méthode, c'est qu'elle permet de mettre à plat toutes les valeurs de la liste. Si on veut rajouter un string dans une concaténation, on peut faire comme ceci: 
```python
a = ["a", "b", "c"]
b = ["c","d"]
c = "Bonjour"
print([*a,*b,c]) # pas de * pour c car c'est un string et non une liste
```
Résultat: `["a", "b", "c", "c", "d", "Bonjour"]`.

## Inline conditions
Il ne s'agit pas forcément des meilleures pratiques car moins lisibles pour les personnes n'ayant pas l'habitude. 

### If [...] else [...]
Les conditions if... else... peuvent s'exprimer de 2 manières différentes: 
```python
# Classique
a = 2
b = 3
if a > b: print("upper")
else: print("lower or equal")

# Inline
print("upper" if a > b else "lower or equal")
```

### `For` loops
On peut faire la même chose avec les boucles `for`:
```python
# on veut doubler la valeur de chaque entier de a
a = [10, 5, 40, 24, 3]

# Classique
b = []
for i in range(a): 
    b.append(i * 2) # on prend chaque valeur et la multiplie par 2

# Inline
b = [i * 2 for i in a]
```

A noter qu'on utiliser un inline `for` avec un inline `If [...] else [...]`

```python
a = [2, 6, 12, 5]

# Si la valeur est inférieure à 6, on la multiplie par 2, sinon on "oublie" cette valeur
b = [i * 2 for i in a if i < 6] 
print(f"b={b}")

# Si la valeur est inférieure à 6, on la double, sinon elle reste telle quelle
c = [i * 2 if i < 6 else i for i in a]
print(f"c={c}")
```
Résultat: 
```
b=[4, 10]
c=[4, 6, 12, 10]
```