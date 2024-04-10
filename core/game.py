import pygame
from pygame.locals import *
from pathlib import Path, PurePath

from classes import *
import levelfiles.levelmaker as levelmaker


import copy


pygame.init()

# Définition globale
titreJeu = "Un jeu."
iconeJeu = ""
tailleEcran = largeurEcran, hauteurEcran = (960, 540)
ecran = pygame.display.set_mode(tailleEcran, DOUBLEBUF, vsync=1)

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
),
"fondgameover" : Actif(
    {"anim1" : [PurePath("images/fonds/fond_game_over.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"retour" : Bouton({"boutretour" :
[
    [PurePath("images/interface/blurgflecheretour.png")],
    [PurePath("images/interface/blurgflecheretour.png")],
    [PurePath("images/interface/blurgflecheretour.png")],
    [PurePath("images/interface/blurgflecheretour.png")],
    [PurePath("images/interface/blurgflecheretour.png")]
]},
{"boutretour" : [
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"boutretour"),
"replay" : Bouton( {"boutreplay" :
[
    [PurePath("images/interface/FlecheRecommencer.png")],
    [PurePath("images/interface/FlecheRecommencer.png")],
    [PurePath("images/interface/FlecheRecommencer.png")],
    [PurePath("images/interface/FlecheRecommencer.png")],
    [PurePath("images/interface/FlecheRecommencer.png")]
]},
{"boutreplay" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"boutreplay"),
"gameoverscreen" : Actif(
    {"anim1" : [PurePath("images/fonds/gameoverscreen.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"fondvicperso" : Actif(
    {"anim1" : [PurePath("images/interface/fond_perso_V.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"cadrescore" : Actif(
    {"anim1" : [PurePath("images/interface/cadre_score_V.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"scoregen" : Text(
    "Score Général :",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"nbscoregen" : Text(
    "34565",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"combogen" : Text(
    "Combo Général :",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"nbcombogen" : Text(
    "135",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"fondvic" : Actif(
    {"anim1" : [PurePath("images/interface/Fond_phases_EV.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"quitter" : Bouton( {"quitter" :
[
    [PurePath("images/interface/Bouton_quitter.png")],
    [PurePath("images/interface/Bouton_quitter.png")],
    [PurePath("images/interface/Bouton_quitter.png")],
    [PurePath("images/interface/Bouton_quitter.png")],
    [PurePath("images/interface/Bouton_quitter.png")]
]},
{"quitter" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"quitter"),
"rejouer" : Bouton( {"rejouer" :
[
    [PurePath("images/interface/Bouton_rejouer.png")],
    [PurePath("images/interface/Bouton_rejouer.png")],
    [PurePath("images/interface/Bouton_rejouer.png")],
    [PurePath("images/interface/Bouton_rejouer.png")],
    [PurePath("images/interface/Bouton_rejouer.png")]
]},
{"rejouer" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"rejouer"),
"phase1" : Actif(
    {"anim1" : [PurePath("images/interface/phase1.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"phase2" : Actif(
    {"anim1" : [PurePath("images/interface/phase2.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"phase3" : Actif(
    {"anim1" : [PurePath("images/interface/phase3.png")]},
    {"anim1" : [False, 5]},
    "anim1"
)
}

objects["premierFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["premierFondbis"].sprites["anim1"][0], 1, 0)
objects["deuxiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["deuxiemeFondbis"].sprites["anim1"][0], 1, 0)
objects["troisiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["troisiemeFondbis"].sprites["anim1"][0], 1, 0)
objects["quatriemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["quatriemeFondbis"].sprites["anim1"][0], 1, 0)


# Scène qui sera affiché
scenecourante = "scene1"

# Liste des objets qui seront affichés après le update
displaylist = {}

# Boucle de jeu
active = True

