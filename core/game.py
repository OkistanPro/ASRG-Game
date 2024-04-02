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
objects = {
"bandeau_haut" : Actif(
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
),
"pers1" : Actif(
    {
        "debout" : [PurePath("images/level/personnage.png")]
    },
    {
        "debout" : [True, 5] #Au hazard
    },
    "debout"
),
"PV" : Text(
    "PV : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255,255,255)
),
"score" : Text(
    "Score",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    30,
    (255,255,255)
),
"cadreProgression" : Actif(
    {"anim1" : [PurePath("images/interface/cadreProgression.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"cadrePV" : Actif(
    {"anim1" : [PurePath("images/interface/cadrePV.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jaugeProgression" : Actif(
    {"anim1" : [PurePath("images/interface/jaugeProgression.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jaugeVertPV" : Actif(
    {"anim1" : [PurePath("images/interface/jaugeVertPV.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jaugeRougePV" : Actif(
    {"anim1" : [PurePath("images/interface/jaugeRougePV.png")]},
    {"anim1" : [False, 5]},
    "anim1"
)}


# Setup les objets (changement des propriétés de chaque objet)
objects["pers1"].taillex = 0.5
objects["pers1"].tailley = 0.5

objects["bandeau_bas"].posy = 470
objects["pers1"].posx = 50
objects["pers1"].posy = 280
objects["PV"].posx = 454
objects["PV"].posy = 10
objects["score"].posx = 10
objects["score"].posy = 40
objects["cadreProgression"].posx = 124
objects["cadreProgression"].posy = 492
objects["cadrePV"].posx = 287
objects["cadrePV"].posy = 7
objects["jaugeProgression"].posx = 129
objects["jaugeProgression"].posy = 497
objects["jaugeVertPV"].posx = 292
objects["jaugeVertPV"].posy = 11
objects["jaugeRougePV"].posx = 292
objects["jaugeRougePV"].posy = 11

objects["PV"].shadow = True
objects["score"].shadow = True

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
    "scene1" : Scene({
        0:[], 
        1:["pers1"], 
        2:[
            "bandeau_haut", 
            "bandeau_bas", 
            "cadreProgression" ,
            "cadrePV" , 
            "jaugeProgression", 
            "jaugeRougePV", 
            "jaugeVertPV", 
            "PV", 
            "score"
        ]}, 
        (0, 0, 0))
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
                    if objects[objet].shadow:
                        displaylist[objet+ "_SHADOW"] = ecran.blit(objects[objet].renderShadow(), (objects[objet].posx+objects[objet].sx-scenes[scenecourante].camera[0], objects[objet].posy+objects[objet].sy-scenes[scenecourante].camera[1]))
                    displaylist[objet] = ecran.blit(objects[objet].renderText(), (objects[objet].posx-scenes[scenecourante].camera[0], objects[objet].posy-scenes[scenecourante].camera[1]))
                else:
                    if objects[objet].shadow:
                        displaylist[objet+ "_SHADOW"] = ecran.blit(objects[objet].renderShadow(), (objects[objet].posx+objects[objet].sx, objects[objet].posy+objects[objet].sy))
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