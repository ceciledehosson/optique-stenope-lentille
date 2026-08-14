# Optique : du sténopé à l'image stigmatique

Animation réalisée avec [Manim Community](https://www.manim.community/) pour illustrer la formation d'une figure par un sténopé et d'une image par une lentille idéale.

## Objectif

L'animation met en relation trois éléments souvent dissociés dans les représentations usuelles de l'optique géométrique :

- un objet est visible lorsque l'œil reçoit un **pinceau de lumière** issu de chacun de ses points ;
- avec un **sténopé de diamètre fini**, un point-objet produit une **tache** sur l'écran ; la figure observée résulte de l'ensemble de ces taches ;
- avec une **lentille idéale stigmatique**, un point-objet correspond à un unique point-image : l'image est reconstruite point par point.

L'écran est considéré comme diffusant. Une fois l'image ou la figure formée sur l'écran, chacun de ses points devient à son tour un point-objet pour l'œil et lui envoie un pinceau de lumière.

## Animation

Le script principal est :

`stenope_lentille_v7.py`

Rendu rapide :

`manim -pql stenope_lentille_v7.py StenopeVersLentilleV7`

Rendu haute définition :

`manim -pqh stenope_lentille_v7.py StenopeVersLentilleV7`

## Installation

L'animation nécessite Python et Manim Community.

Dans un environnement virtuel :

``` bash
python3 -m venv manim-env
source manim-env/bin/activate
pip install manim
```

Sous Linux, certaines dépendances système de Cairo et Pango peuvent également être nécessaires.

## Principe de construction

Le script ne repose pas sur une animation pré-dessinée. Les rayons et pinceaux lumineux sont construits géométriquement à partir de la position de l'objet, de l'ouverture, de la lentille et de l'écran. Dans le modèle de lentille utilisé ici, la lentille est supposée idéale et stigmatique : tous les rayons issus d'un même point-objet et traversant la lentille convergent vers le même point-image.

## Autrice

Cécile de Hosson
Université Paris Cité — Laboratoire de Didactique André Revuz

## Licence

Le code source est distribué sous licence MIT.

Les vidéos, schémas et contenus pédagogiques associés sont mis à disposition sous licence Creative Commons Attribution 4.0 International (CC BY 4.0).

© Cécile de Hosson
