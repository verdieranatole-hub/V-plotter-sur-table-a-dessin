# preprocesseur

La partie logiciel demande encore à l'utilisateur de manipuler le programme, donc voici un guide sur les paramètres à modifier et ceux à quoi ils correspondent.

## choisir le fichier à transformer

Entrez ici le nom du fichier gcode que vous souhaitez transformé en coordonnée moteur, attention il doit être enregistré dans le même dossier que le programme, ou eventuellement dans un sous dossier de celui-ci dont le chemin sera à préciser.
![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/preprocesseur/images/INPUT_FILE.png)

## choisir où le nouveau fichier gcode ira et son nom

Entrez ici le nom du fichier gcode transformé en coordonnée moteur, attention il sera enregistré dans le même dossier que le programme, ou eventuellement dans un sous dossier de celui-ci dont le chemin sera à préciser.
![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/preprocesseur/images/OUTPUT_FILE.png)

## distance entre les accroches des câbles

Renseignez ici la distance entre les sorties de courroies. __Ce paramètre pose des problèmes de précisions majeurs en cas de mauvais renseignement.__

![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/preprocesseur/images/distance_entre_les_sorties_de_courroies.png)

## préciser la longueur des divisions

Ce paramètre a une influence direct sur la précision de la machine et correspond a la fréquence à laquelle les coordonnées cartésiennes sont transformé en coordonnées moteurs

![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/preprocesseur/images/taille_des_segments.png)

## délai de lever et de baisser du crayon

renseignez ici la durée de lever et de baisser du crayon en ms. __Si le temps est trop court, les trajectoires de liaisons seront partiellement visibles, si ce temps est trop long la vitesse de travail sera diminué.__

![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/preprocesseur/images/delai_lever_et_baisser_de_stylo.png)

## longueurs initiales des courroies

renseignez ici la longueur initiale des courroies. __Ce paramètre pose des problèmes de précisions majeurs en cas de mauvais renseignement.__

![](https://github.com/verdieranatole-hub/V-plotter-sur-table-a-dessin/blob/main/preprocesseur/images/longueur_origine_des_courroies.png)
