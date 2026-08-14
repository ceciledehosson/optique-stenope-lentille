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

```bash
manim -pql stenope_lentille_v7.py StenopeVersLentilleV7
