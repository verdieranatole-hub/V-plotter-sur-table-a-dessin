# montage

Le montage des pièces physique ne pose pas de problême particulier:

## étape 1: montage de la règle
- Montez les poulies sur les moteurs, le décalage des poulies sera à régler une fois le V_plotter monté. ![]()
- Montez le moteur sur les supports moteurs ![]() ![]();
- vissez les deux supports moteurs à chaques extrémité de votre barre ou si votre configuration doit bouger au cours du temps passez directement à la prochaine étapes
- vissez la partie haute du V-plotter sur le rail de la table à dessin

remarque: les points d'ancrage du moteur sur le rail pourrait aussi servir de points d'encrage pour des cordes ou tout autres éléments perméttant de fixer le V-plotter là ou vous le souhaitez.

## étape 2: montage de la nacelle
- Enfoncez à l'aide d'un fer à souder les insert filleté dans les trous en haut du sabot
- collez le servomoteur dans son logement
- faites passer le cable sur le sabot, le collez en place
- Collez la bague bronze au fond de son logement
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
- placez les drivers moteurs dans leur emplacement (X et Y), les placer vis de réglage vers l'extérieur comme sur l'image suivante
![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/images/placement_driver.JPG)

- relier l'alimentation à l'entrée du shield. ![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/images/emplacement_alimentation.JPG)
- de même relier l'alimentation à son câble électrique (l'autre extrémité n'étant pas relier au réseau celà va sans dire)
- relier les deux cartes arduino comme suit le port Z+ du CNC shield vers le port A0 de la deuxième arduino (fil jaune sur les images), le port 5V du CNC shield ves le port Vin de la deuxième arduino (fil orange sur l'image), le port gnd du cnc shield sur le port gnd de la deuxième arduino (fil bleue sur la photo) ![branchement sur le CNC shield](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/images/branchement_cnc_shield.jpg) ![branchement sur l'arduino secondaire](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/images/branchement_arduino_secondaire.jpg)
- Brancher le cables du servo-moteur, l'alimentation (en rouge sur la photo suivante doit être placé sur le 5V (si votre servo à besoin d'une tension plus élevé ou plus basse faire le nécéssaire), la terre (ici en noir) doit être placé sur un gnd de la carte, quand a l'information (ici en bleue) doit être branché sur le port 09 de la carte, ou modifié vers un autre port acceptant le PWM dans le programme ![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/images/branchement_servo.jpg)
- brancher l'autre extrémité du cable au servo, en générale la couleur la plus proche du noir est le neutre, celle la plus proche du rouge l'alimentation et celle d'une autre couleur est l'information, se référer à la documentation de votre servomoteur pour plus d'information.
- brancher les moteurs ne refermez pas le couvercle, vous saurez si vous vous êtes trompé de sens pour ceux-ci une fois les premiers essais effectué.

## étape 4: programmation des deux cartes

### sur la carte disposant du module CNC shield V3
Pour celà on utilise GRBL dont les fichiers sources sont [ici](https://github.com/grbl/grbl) vous y trouverez aussi les instruction d'installation. Cependant il semble qu'il y ait un souci avec les dernières versions de l'éditeur arduino, l'installation a été réussite sans le moindre soucis avec l'IDE arduino 1.8.19.
### sur celle n'en disposant pas
téléversez simplement le programme servomoteur.ino dans la carte

## étape 5: mise en place d'un marquage permettant une remise à zero sur votre support

La solution la plus simple consiste à placer un bout de scotch afin de repérer visuellement le zero, sur lequel vous viendrez mesurer la longeur des courroies à l'aide d'un mètre ruban une fois ceci fait vous pourrez garder les mêmes longueur initial de courroie pour le reste de vos impressions à condition de partir initialement de ce repère. Bien que ce genre de repères soit à peu près suffisant pour configeurer la machine, il reste insuffisament précis pour permettre par exemple d'utiliser plusieurs couleurs au cours d'une même impression.

Une solution un peu plus précise serait de mettre un coin, à un emplacement donné du tableau et de venir calé physiquement le V-plotter dans le coin en désactivant les moteurs. Là aussi mesurer au mètre ruban la longeur des courroies et noté cette valeur.

## étape 6: paramétrage de UGS
Afin d'envoyer les instructions à la machine ont utilise ugs, un logicielle gratuit, open source dont le lien est disponible [ici](https://winder.github.io/ugs_website/download/). Les prochaines étapes concernent le paramétrage de la machine.

### paramétrage du nombre de pas par tour:
Si lors du montage vous avez effectivement pu installer les 3 jumpers sur chaque drivers, et que vous avez une poulie 20 dents sur une courroie GT2 6mm, vous avez avec un moteur ayant 200 pas par tour, 1mm = 5 pas, avec 16 micropas par pas on obtient 1mm = 80 micropas, il faut donc écrire dans la console $100 = 80 et $101 = 80, bien que le microstepping ne permet pas vraiment de positionner le moteur à d'autre position précise que celle offerte par le pas classique, il permet de largement fluidifier le passage entre deux pas et d'éviter l'effet escalier.

### paramétrage de la vitesse maximale des axes:

ce paramètres va influer sur la vitesse maximal à laquelle une courroie peut s'étendre ou se rétracter, ce contrôle ne gère pas la vitesse de la nacelle en elle même, les réglages actuelles de la machine sont une vitesse maximale de 2000 mm / min sur chacun des axes, augmenter ce réglage pourrait augmenter la vitesse d'impression, même si l'accélération maximale qui sera la prochaine catégorie devrait avoir un effet nettement plus important, quoiqu'il en soit ce paramètre correspond à $110 pour le moteur gauche et $111 pour le moteur droit.

### paramétrage de l'accélération maximale des axes:

Ce paramètre sera celui qui influeras le plus sur la durée d'impression, pour l'instant il est réglé tel que $120 et $121 = 100 (mm/s²)
