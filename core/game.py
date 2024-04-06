import pygame
from pygame.locals import *
from pathlib import Path, PurePath

from classes import *

pygame.init()

# Définition globale
titreJeu = "Un jeu."
iconeJeu = ""
tailleEcran = largeurEcran, hauteurEcran = (960, 540)
ecran = pygame.display.set_mode(tailleEcran, SCALED, vsync=1)

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

Bouton( 0 : Normal, 1 : Enfoncé, 2 : Grisé, 3 : Sélectionné, 4 : Survolé
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
    {"bandeau_haut" : [PurePath("images/interface/bandeau.png")]},
    {"bandeau_haut" : [True, 1]}, #Ne change rien car image fixe
    "bandeau_haut"
),
"bandeau_bas" : Actif(
    {"bandeau_bas" : [PurePath("images/interface/bandeau.png")]},
    {"bandeau_bas" : [True, 1]},
    "bandeau_bas"
),
"pers1" : Actif(
    {"debout" : [PurePath("images/level/personnage.png")]},
    {"debout" : [True, 5]}, #Au hazard
    "debout"
),
"coeur1" : Actif(
    {"anim1" : [PurePath("images/level/coeurRouge.png")]},
    {"anim1" : [True, 5]},
    "anim1",
    ["item", "coeur"]
),
"coeur2" : Actif(
    {"anim1" : [PurePath("images/level/coeurRouge.png")]},
    {"anim1" : [True, 5]},
    "anim1",
    ["item", "coeur"]
),
"PV" : Text(
    "PV",
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
"numscore" : Text(
    "01458",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    32,
    (255,255,0)
),
"combo" : Text(
    "combo",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255,255,0)
),
"pause" : Bouton(
    { "pause" : [
        [PurePath("images/interface/rainbowpause.png")],
        [PurePath("images/interface/rainbowpause.png")],
        [PurePath("images/interface/rainbowpause.png")],
        [PurePath("images/interface/rainbowpause.png")],
        [PurePath("images/interface/rainbowpause.png")]
    ], "play" : [
        [PurePath("images/interface/youtubebronze.png")],
        [PurePath("images/interface/youtubebronze.png")],
        [PurePath("images/interface/youtubebronze.png")],
        [PurePath("images/interface/youtubebronze.png")],
        [PurePath("images/interface/youtubebronze.png")]
    ]},
    {"pause" : [
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5]
    ], "play" : [
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5]
    ]},
    "pause"
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
),
"premierFond" : Actif(
    {
        "anim1" : [PurePath("images/fonds/premierPlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"premierFondbis" : Actif(
    {
        "anim1" : [PurePath("images/fonds/premierPlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"deuxiemeFond" : Actif(
    {
        "anim1" : [PurePath("images/fonds/deuxiemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"deuxiemeFondbis" : Actif(
    {
        "anim1" : [PurePath("images/fonds/deuxiemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"troisiemeFond" : Actif(
    {
        "anim1" : [PurePath("images/fonds/troisiemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"troisiemeFondbis" : Actif(
    {
        "anim1" : [PurePath("images/fonds/troisiemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"quatriemeFond" : Actif(
    {
        "anim1" : [PurePath("images/fonds/quatriemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"quatriemeFondbis" : Actif(
    {
        "anim1" : [PurePath("images/fonds/quatriemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"sol" : Actif(
    {"anim1" : [PurePath("images/fonds/sol.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"solbis" : Actif(
    {"anim1" : [PurePath("images/fonds/sol.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"fondpause" : Actif(
    {"anim1" : [PurePath("images/fonds/fondpause.png")]},
    {"anim1" : [False, 5]},
    "anim1"
)}
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
        0:[
            "quatriemeFond", 
            "quatriemeFondbis", 
            "troisiemeFond", 
            "troisiemeFondbis", 
            "deuxiemeFond", 
            "deuxiemeFondbis", 
            "premierFond", 
            "premierFondbis", 
            "sol", 
            "solbis"
        ], 
        1:[
            "pers1"
        ], 
        2:[
            "coeur1", 
            "coeur2"
        ],
        3:[
            "fondpause",
            "bandeau_haut", 
            "bandeau_bas", 
            "cadreProgression" ,
            "cadrePV" , 
            "jaugeProgression", 
            "jaugeRougePV", 
            "jaugeVertPV", 
            "PV", 
            "score",
            "numscore",
            "combo",
            "pause"
        ]}, 
        (0, 0, 0))
}


# Setup les objets (changement des propriétés de chaque objet)
#Tailles objets
objects["pers1"].taillex = 0.5
objects["pers1"].tailley = 0.5

#Positions objets
objects["premierFond"].posy = objects["premierFondbis"].posy = 181
objects["deuxiemeFond"].posy = objects["deuxiemeFondbis"].posy = 181
objects["troisiemeFond"].posy = objects["troisiemeFondbis"].posy = 150
objects["sol"].posy = objects["solbis"].posy = 410

objects["premierFondbis"].posx = 960
objects["deuxiemeFondbis"].posx = 960
objects["troisiemeFondbis"].posx = 960
objects["quatriemeFondbis"].posx = 960
objects["solbis"].posx = 960

objects["pers1"].posx = 50
objects["pers1"].posy = 280
## Ennemis haut posy = 185
## Ennemis bas posy = 365
objects["coeur1"].posx = 800
objects["coeur1"].posy = 185 - (objects["coeur1"].sprites["anim1"][0].get_rect().height / 2)
objects["coeur2"].posx = 800
objects["coeur2"].posy = 365 - (objects["coeur1"].sprites["anim1"][0].get_rect().height / 2)

# (pendant les calculs de position, utiliser les tailles de l'image non redimensionnées) width / 4

objects["bandeau_bas"].posy = 470
objects["PV"].posx = 480 - (objects["PV"].renderText().get_rect().width / 2)
objects["PV"].posy = 10
objects["score"].posx = 10
objects["score"].posy = 40
objects["numscore"].posx = 10
objects["numscore"].posy = 10
objects["combo"].posx = 480 - (objects["combo"].renderText().get_rect().width / 2)
objects["combo"].posy = 40
objects["pause"].posx = 890
objects["pause"].posy = 0
objects["cadreProgression"].posx = 480 - (objects["cadreProgression"].sprites["anim1"][0].get_rect().width / 2)
objects["cadreProgression"].posy = 492
objects["cadrePV"].posx = 480 - (objects["cadrePV"].sprites["anim1"][0].get_rect().width / 2)
objects["cadrePV"].posy = 7
objects["jaugeProgression"].posx = 480 - (objects["jaugeProgression"].sprites["anim1"][0].get_rect().width / 2)
objects["jaugeProgression"].posy = 497
objects["jaugeVertPV"].posx =  480 - (objects["jaugeVertPV"].sprites["anim1"][0].get_rect().width / 2)
objects["jaugeVertPV"].posy = 11
objects["jaugeRougePV"].posx =  480 - (objects["jaugeRougePV"].sprites["anim1"][0].get_rect().width / 2)
objects["jaugeRougePV"].posy = 11

#Ombres objets
objects["PV"].shadow = True
objects["score"].shadow = True
objects["numscore"].shadow = True
objects["combo"].shadow = True

#Parallax
objects["premierFond"].parallax = objects["premierFondbis"].parallax = [0.8, 1.0]
objects["deuxiemeFond"].parallax = objects["deuxiemeFondbis"].parallax = [0.6, 1.0]
objects["troisiemeFond"].parallax = objects["troisiemeFondbis"].parallax = [0.4, 1.0]
objects["quatriemeFond"].parallax = objects["quatriemeFondbis"].parallax = [0.2, 1.0]

for object in scenes["scene1"].calques[1]:
    objects[object].suivreScene = True

for object in scenes["scene1"].calques[3]:
    objects[object].suivreScene = True

objects["premierFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["premierFondbis"].sprites["anim1"][0], 1, 0)
objects["deuxiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["deuxiemeFondbis"].sprites["anim1"][0], 1, 0)
objects["troisiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["troisiemeFondbis"].sprites["anim1"][0], 1, 0)
objects["quatriemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["quatriemeFondbis"].sprites["anim1"][0], 1, 0)

objects["fondpause"].visible = False

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
                        (objects[objet].posx-(scenes[scenecourante].camera[0]*objects[objet].parallax[0]),objects[objet].posy-(scenes[scenecourante].camera[1]*objects[objet].parallax[1]))
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
    pygame.display.update()