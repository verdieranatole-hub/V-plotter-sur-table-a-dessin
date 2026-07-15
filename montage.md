# montage

Le montage des pièces physique ne pose pas de problême particulier:

## étape 1: montage de la règle
- Montez les poulies sur les moteurs, le décalage des poulies sera à régler une fois le V_plotter monté. ![]()
- Montez le moteur sur les supports moteurs ![]() ![]();
- vissez les deux supports moteurs à chaques extrémité de votre barre ou si votre configuration doit bouger au cours du temps passez directement à la prochaine étapes
- vissez la partie haute du V-plotter sur le rail de la table à dessin

remarque: les points d'ancrage du moteur sur le rail pourrait aussi servir de points d'encrage pour des cordes ou tout autres éléments perméttant de fixer le V-plotter là ou vous le souhaitez.

## étape 2: montage de la nacelle
- Collez la bague bronze au fond de son logement, rajouter un point de colle
- Enfoncez à l'aide d'un fer à souder les insert filleté dans les trous en haut du sabot
- collez le servomoteur dans son logement
- faites passer le cable sur le sabot, le collez en place
- Montez le servo-moteur en place
- insérez les courroies dans les supports de courroies
- placez les supports de courroies sur la bagues en bronze.
- inserez à l'aide d'un fer à souder les insert filleté dans le porte crayon
- placez le porte crayon dans la bague
- placez le ressort
- mettre le support de ressort et le vissez en place
- placez le crayon de tel manière que la mine dépasse de 1 mm

## étape 3: montage du boitier électronique et câblage
- vissez en place les composant dans le boitier, tous les composants ne peuvent se monter que dans un seul sens, le placement des arduino ne revet que peu d'importance.
- placez un jumper entre la pin enable et ground du cnc shield ![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/images/jumper_enable.jpg), en placez aussi 3 en dessous de chaque driver ![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/images/jumper_sous_driver.jpg)


## étape 4: programmation des deux cartes

### sur la carte disposant du module CNC shield V3
Pour celà on utilise GRBL dont les fichiers sources sont [ici](https://github.com/grbl/grbl) vous y trouverez aussi les instruction d'installation. Cependant il semble qu'il y ait un souci avec les dernières versions de l'éditeur arduino, l'installation a été réussite sans le moindre soucis avec l'IDE arduino 1.8.19.
### sur celle n'en disposant pas
téléversez simplement le programme dans la carte

## étape 5: mise en place d'un marquage permettant une remise à zero sur votre support

## étape 6: paramétrage de UGS
Afin d'envoyer les instructions à la machine ont utilise ugs, un logicielle gratuit, open source dont le lien est disponible [ici](https://winder.github.io/ugs_website/download/). Les prochaines étapes concernent le paramétrage de la machine.

### paramétrage du nombre de pas par tour:
Si lors du montage vous avez effectivement pu installer les 3 jumpers sur chaque drivers, et que vous avez une poulie 20 dents sur une courroie GT2 6mm, vous avez avec un moteur ayant 200 pas par tour, 1mm = 5 pas, avec 16 micropas par pas on obtient 1mm = 80 micropas, il faut donc écrire dans la console $100 = 80 et $101 = 80, bien que le microstepping ne permet pas vraiment de positionner le moteur à d'autre position précise que celle offerte par le pas classique, il permet de largement fluidifier le passage entre deux pas et d'éviter l'effet escalier.

### paramétrage de la vitesse maximale des axes:

ce paramètres va influer sur la vitesse maximal à laquelle une courroie peut s'étendre ou se rétracter, ce contrôle ne gère pas la vitesse de la nacelle en elle même, les réglages actuelles de la machine sont une vitesse maximale de 2000 mm / min sur chacun des axes, augmenter ce réglage pourrait augmenter la vitesse d'impression, même si l'accélération maximale qui sera la prochaine catégorie devrait avoir un effet nettement plus important, quoiqu'il en soit ce paramètre correspond à $110 pour le moteur gauche et $111 pour le moteur droit.

### paramétrage de l'accélération maximale des axes:

Ce paramètre sera celui qui influeras le plus sur la durée d'impression, pour l'instant il est réglé tel que $120 et $121 = 100 (mm/s²)
