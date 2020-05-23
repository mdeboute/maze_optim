# maze

Ceci est un projet de programmation sur la génération et visite de labyrinthe. Il y a 3 fichiers principaux:
+ `solution_generate.py` pour générer un labyrinthe,
+ `solution_shortest.py` pour calculer un plus court chemin,
+ `solution_visit.py` pour faire des *visites* (sans visibilité du labyrinthe complet).

Chacun de ces fichiers peut être exécuté en ligne de commande, et
l'option `-h` ou `--help` donne les options utilisables. Par exemple,

`python3 solution_generate.py --help`

affiche

```
usage: Generate a labyrinth of given size [-h] [-o FILE] [--slow] [-s]
                                          [-d DRAW] [-r X]
                                          n m

positional arguments:
  n                     Number of columns of the labyrinth
  m                     Number of rows of the labyrinth

optional arguments:
  -h, --help            show this help message and exit
  -o FILE               File to save the result
  --slow                Use the slow algorithm for checking connected
                        components
  -s, --show            Show the result in compact form
  -d DRAW, --draw DRAW  Draw the result in an image with this filename
  -r X                  Remove X random walls from the labyrinth
```

L'option de dessiner dans un fichier nécessite `wand` (basé sur
ImageMagick, plus d'informations
[sur leur page](https://docs.wand-py.org/)). L'affichage des visites
dans le terminal n'est pas garanti de marcher sous Windows.
