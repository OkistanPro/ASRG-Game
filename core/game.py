import pygame
from pygame.locals import *
from pathlib import Path, PurePath

from classes import *

pygame.init()

# Définition globale
titreJeu = "Un jeu."
iconeJeu = ""
tailleEcran = largeurEcran, hauteurEcran = (960, 540)
ecran = pygame.display.set_mode(tailleEcran)

# Définition de l'horloge
horloge = pygame.time.Clock()
FPS = 60

# Définition des Objects
# Exemple : objects = {"nomObjet" : Objet}
# Les types d'objets en questions :
"""
Actif   (   
            { 
                "nomAnim" : [PurePath("cheminImage1..."), PurePath("cheminImage2...")...], 
                "nomAnim2" : ...
            },
 
            {
                "nomAnim" : [enBoucle, vitesseAnim],
                "nomAnim2" : ...
            },

            "nomAnimParDéfaut"
        )

Text(
    "blablabla", 
    PurePath("cheminVersPolice"), 
    taillePolice, 
    (R, V, B) --> couleur du Texte
)

Bouton(
        [
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...],
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...],
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...],
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...],
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...]
        ],
        [
            [enBoucle, imageDébutBoucle, vitesseAnim],
            [enBoucle, imageDébutBoucle, vitesseAnim],
            [enBoucle, imageDébutBoucle, vitesseAnim],
            [enBoucle, imageDébutBoucle, vitesseAnim],
            [enBoucle, imageDébutBoucle, vitesseAnim]
        ]

)
"""
objects = {"bandeau_haut" : Actif(
    {
        "bandeau_haut" : [PurePath("images/interface/bandeau.png")]
    },
    {
        "bandeau_haut" : [True, 1] #Ne change rien car image fixe
    },
    "bandeau_haut"
),
"bandeau_bas" : Actif(
    {
        "bandeau_bas" : [PurePath("images/interface/bandeau.png")]
    },
    {
        "bandeau_bas" : [True, 1] #Ne change rien car image fixe
    },
    "bandeau_bas"
)}


# Setup les objets (changement des propriétés de chaque objet)
objects["bandeau_bas"].posy = 470

# Définition des scènes
"""
scenes = {
    "nomScène" : Scene(
        {
            numCalque : ["nomObjet1", "nomObjet2", ...],
            numCalque2 : ...
        },
        (R, V, B) --> couleur du fond de la scène
    ),

    "nomScène2" : ...
}
"""
scenes = {
    "scene1" : Scene({0:["bandeau_haut", "bandeau_bas"]}, (0, 0, 0))
}

# Scène qui sera affiché
scenecourante = "scene1"

# Liste des objets qui seront affichés après le update
displaylist = {}

# Boucle de jeu
active = True

def update():
    displaylist["BACKGROUND"] = ecran.fill(scenes[scenecourante].fond)
    # Pour chaque calque de la scène courante
    for calque in scenes[scenecourante].calques:
        # Pour chaque objet du calque
        for objet in scenes[scenecourante].calques[calque]:
            # Si l'objet est un Actif
            if isinstance(objects[objet], Actif) and objects[objet].visible:
                # On augmente son compteur d'animation
                objects[objet].cptframe += 1

                if not objects[objet].suivreScene:
                    displaylist[objet] = ecran.blit(
                        pygame.transform.scale_by(objects[objet].renderActif(),
                        (objects[objet].taillex, objects[objet].tailley)),
                        (objects[objet].posx-scenes[scenecourante].camera[0],objects[objet].posy-scenes[scenecourante].camera[1])
                    )
                else:
                    displaylist[objet] = ecran.blit(
                        pygame.transform.scale_by(objects[objet].renderActif(),
                        (objects[objet].taillex, objects[objet].tailley)),
                        (objects[objet].posx,objects[objet].posy)
                    )
            # Si l'objet est un Text
            if isinstance(objects[objet], Text) and objects[objet].visible:

                if not objects[objet].suivreScene:
                    displaylist[objet] = ecran.blit(objects[objet].renderText(), (objects[objet].posx-scenes[scenecourante].camera[0], objects[objet].posy-scenes[scenecourante].camera[1]))
                else:
                    displaylist[objet] = ecran.blit(objects[objet].renderText(), (objects[objet].posx, objects[objet].posy))

            # Si l'objet est un Bouton
            if isinstance(objects[objet], Bouton) and objects[objet].visible:
                # On augmente son compteur d'animation
                objects[objet].cptframe += 1

                if not objects[objet].suivreScene:
                    displaylist[objet] = ecran.blit(
                        pygame.transform.scale_by(objects[objet].renderButton(),
                        (objects[objet].taillex, objects[objet].tailley)),
                        (objects[objet].posx-scenes[scenecourante].camera[0],objects[objet].posy-scenes[scenecourante].camera[1])
                    )
                else:
                    displaylist[objet] = ecran.blit(
                        pygame.transform.scale_by(objects[objet].renderButton(),
                        (objects[objet].taillex, objects[objet].tailley)),
                        (objects[objet].posx,objects[objet].posy)
                    )
    # On réactualise l'écran
    pygame.display.flip()