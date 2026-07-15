# montage

Le montage des pièces physique ne pose pas de problême particulier:

## étape 1: montage de la règle

## étape 2: montage de la nacelle

## étape 3: montage du boitier électronique et câblage

## étape 4: programmation des deux cartes

### sur la carte disposant du module CNC shield V3
Pour celà on utilise GRBL dont les fichiers sources sont [ici](https://github.com/grbl/grbl) vous y trouverez aussi les instruction d'installation. Cependant il semble qu'il y ait un souci avec les dernières versions de l'éditeur arduino, l'installation a été réussite sans le moindre soucis avec l'IDE arduino 1.8.19.

## étape 5: mise en place d'un marquage permettant une remise à zero sur votre support

## étape 6: paramétrage de UGS
Afin d'envoyer les instructions à la machine ont utilise ugs, un logicielle gratuit, open source dont le lien est disponible [ici](https://winder.github.io/ugs_website/download/). Les prochaines étapes concernent le paramétrage de la machine.

### paramétrage du nombre de pas par tour:
Si lors du montage vous avez effectivement pu installer les 3 jumpers sur chaque drivers, et que vous avez une poulie 20 dents sur une courroie GT2 6mm, vous avez avec un moteur ayant 200 pas par tour, 1mm = 5 pas, avec 16 micropas par pas on obtient 1mm = 80 micropas, il faut donc écrire dans la console $100 = 80 et $101 = 80, bien que le microstepping ne permet pas vraiment de positionner le moteur à d'autre position précise que celle offerte par le pas classique, il permet de largement fluidifier le passage entre deux pas et d'éviter l'effet escalier.

### paramétrage de la vitesse maximale des axes:

ce paramètres va influer sur la vitesse maximal à laquelle une courroie peut s'étendre ou se rétracter, ce contrôle ne gère pas la vitesse de la nacelle en elle même, les réglages actuelles de la machine sont une vitesse maximale de 2000 mm / min sur chacun des axes, augmenter ce réglage pourrait augmenter la vitesse d'impression, même si l'accélération maximale qui sera la prochaine catégorie devrait avoir un effet nettement plus important, quoiqu'il en soit ce paramètre correspond à $110 pour le moteur gauche et $111 pour le moteur droit.

### paramétrage de l'accélération maximale des axes:

Ce paramètre sera celui qui influeras le plus sur la durée d'impression, pour l'instant il est réglé tel que $120 et $121 = 100 (mm/s²)
