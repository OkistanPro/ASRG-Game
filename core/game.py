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
"cadrescore" : Actif(
    {"anim1" : [PurePath("images/interface/cadre_score_V.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
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
        0:{
            "quatriemeFond" : [0, 0], 
            "quatriemeFondbis" : [960, 0], 
            "troisiemeFond" : [0, 150], 
            "troisiemeFondbis" : [960, 150], 
            "deuxiemeFond" : [0, 181], 
            "deuxiemeFondbis" : [960, 181], 
            "premierFond" : [0, 181], 
            "premierFondbis" : [960, 181], 
            "sol" : [0, 410], 
            "solbis" : [960, 410] ,
            "gameoverscreen" : [0, 0]
        }, 
        1:{
            "pers1" : [50, 280]
        }, 
        2:{},
        3:{
            "fondpause" : [0, 0],
            "bandeau_haut" : [0, 0], 
            "bandeau_bas" : [0, 470], 
            "cadreProgression" : [480 - (objects["cadreProgression"].sprites["anim1"][0].get_rect().width / 2), 492],
            "cadrePV" : [480 - (objects["cadrePV"].sprites["anim1"][0].get_rect().width / 2), 7], 
            "jaugeProgression" : [480 - (objects["jaugeProgression"].sprites["anim1"][0].get_rect().width / 2), 497], 
            "jaugeRougePV" : [480 - (objects["jaugeRougePV"].sprites["anim1"][0].get_rect().width / 2), 11], 
            "jaugeVertPV" : [480 - (objects["jaugeVertPV"].sprites["anim1"][0].get_rect().width / 2), 11], 
            "PV" : [480 - (objects["PV"].renderText().get_rect().width / 2), 10], 
            "score" : [10, 40],
            "numscore" : [10, 10],
            "combo" : [480 - (objects["combo"].renderText().get_rect().width / 2), 40],
            "pause" : [890, 0]
        }}, 
        (0, 0, 0)),
    "gameover" : Scene({
        0:{
            "fondgameover" : [0, 0]
        },
        1:{
            "retour" : [0, 0],
            "replay" : [890, 0]
        }}, 
        (0, 0, 0)),
    "victoire" : Scene({
        0:{
            "fondvicperso" : [960 - (objects["fondvicperso"].sprites["anim1"][0].get_rect().width), 0],
            "fondvic" : [0, 0]
        },
        1:{
            "quitter" : [312.5 - (objects["quitter"].images["quitter"][0][0].get_rect().width), 5],
            "rejouer" : [322.5, 5],
            "cadrescore" : [940 - (objects["cadrescore"].sprites["anim1"][0].get_rect().width), 0],
            "phase1" : [10, 25+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)],
            "phase2" : [10, 25+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)],
            "phase3" : [10, 25+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)]
        }}, 
        (0, 0, 0))
}

objects["premierFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["premierFondbis"].sprites["anim1"][0], 1, 0)
objects["deuxiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["deuxiemeFondbis"].sprites["anim1"][0], 1, 0)
objects["troisiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["troisiemeFondbis"].sprites["anim1"][0], 1, 0)
objects["quatriemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["quatriemeFondbis"].sprites["anim1"][0], 1, 0)


def initscene1():
    # Setup les objets (changement des propriétés de chaque objet)
    scenes["scene1"].calques = copy.deepcopy(scenes["scene1"].init)
    # print(scenes["scene1"].init)
    #Tailles objets
    objects["pers1"].taillex = 0.5
    objects["pers1"].tailley = 0.5

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

    objects["fondpause"].visible = False
    objects["gameoverscreen"].visible = False
    objects["gameoverscreen"].suivreScene = True

    levelelements = levelmaker.getelements(PurePath("levelfiles/testniveau3.csv"))
    """
    for element in levelelements:
        match element:
            case "phase":

            case "items":

            case "small":

            case "large":

            case "long":

            case "boss":

            case "fantome":

            case "normal":

            case "liee":

            case "silence":

            case "cube":

            case "pique":

            case "orbe":
            
            case "dash":
    """

    for element in levelelements:
        match element:
            case "phase":
                for phase in levelelements[element]:
                    if phase=="phase1" and levelelements[element][phase] != []:
                        objects["iconphase1"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase1.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface"]
                        )
                    if phase=="phase2" and levelelements[element][phase] != []:
                        objects["iconphase2"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase2.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface"]
                        )
                    if phase=="phase3" and levelelements[element][phase] != []:
                        objects["iconphase3"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase3.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface"]
                        )

            case "items":
                if levelelements[element]["notes"] != {"up" : [], "down" : []}:
                    for up in levelelements[element]["notes"]['up']:
                        objects["note"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/note.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup"]
                    )
                        scenes["scene1"].calques[2]["note"+str(up)] = [(up * 600 / 1000) + 150, 160]
                    for down in levelelements[element]["notes"]['down']:
                        objects["note"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/note.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown"]
                    )
                        scenes["scene1"].calques[2]["note"+str(down)] = [(down * 600 / 1000) + 150, 340]

                if levelelements[element]["coeur"] != {"up" : [], "down" : []}:
                    for up in levelelements[element]["coeur"]['up']:
                        objects["coeur"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/coeur.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup"]
                    )
                        scenes["scene1"].calques[2]["coeur"+str(up)] = [(up * 600 / 1000) + 150, 160]
                    for down in levelelements[element]["coeur"]['down']:
                        objects["coeur"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/coeur.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown"]
                    )
                        scenes["scene1"].calques[2]["coeur"+str(down)] = [(down * 600 / 1000) + 150, 340]
            case "small":
                if levelelements[element]["up"] != [] or levelelements[element]["down"] != []:
                    for up in levelelements[element]['up']:
                        objects["small"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/small.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup"]
                    )
                        scenes["scene1"].calques[2]["small"+str(up)] = [(up * 600 / 1000) + 150, 160]
                    for down in levelelements[element]['down']:
                        objects["small"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/small.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown"]
                    )
                        scenes["scene1"].calques[2]["small"+str(down)] = [(down * 600 / 1000) + 150, 340]
            
            case "large":
                for up in levelelements[element]['up']:
                        objects["large"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/large.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup"]
                    )
                        scenes["scene1"].calques[2]["large"+str(up)] = [(up * 600 / 1000) + 150, 135]
                for down in levelelements[element]['down']:
                        objects["large"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/large.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown"]
                    )
                        scenes["scene1"].calques[2]["large"+str(down)] = [(down * 600 / 1000) + 150, 315]

            case "long":
                for up in levelelements[element]['up']:
                        objects["longstart"+str(up[0])] = Actif(
                        {"anim1" : [PurePath("images/level/debutlongredi.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "long", "start", "up"]
                    )
                        objects["longend"+str(up[1])] = Actif(
                        {"anim1" : [PurePath("images/level/finlongredi.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "long", "end", "down"]
                    )
                        scenes["scene1"].calques[2]["longstart"+str(up[0])] = [(up[0] * 600 / 1000) + 150, 150]
                        scenes["scene1"].calques[2]["longend"+str(up[1])] = [(up[1] * 600 / 1000) -131, 150]
                for down in levelelements[element]['down']:
                        objects["longstart"+str(down[0])] = Actif(
                        {"anim1" : [PurePath("images/level/debutlongredi.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "long", "start", "down"]
                    )
                        objects["longend"+str(down[1])] = Actif(
                        {"anim1" : [PurePath("images/level/finlongredi.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "long", "end", "down"]
                    )
                        scenes["scene1"].calques[2]["longstart"+str(down[0])] = [(down[0] * 600 / 1000) + 150, 360]
                        scenes["scene1"].calques[2]["longend"+str(down[1])] = [(down[1] * 600 / 1000) -131, 360]

            case "boss":
                for hit in levelelements[element]['hit']:
                        objects["boss"+str(hit)] = Actif(
                        {"anim1" : [PurePath("images/level/boss.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "boss", "hit"]
                    )
                        scenes["scene1"].calques[2]["boss"+str(hit)] = [(hit * 600 / 1000) + 420, 100]
                for long in levelelements[element]['long']:
                        objects["boss"+str(long[0])] = Actif(
                        {"anim1" : [PurePath("images/level/boss.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "boss", "long", str(long[1])]
                    )
                        scenes["scene1"].calques[2]["boss"+str(long[0])] = [(long[0] * 600 / 1000) + 420, 100]

            case "fantome":
                for up in levelelements[element]['up']:
                        objects["fantome"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/fantome.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup"]
                    )
                        scenes["scene1"].calques[2]["fantome"+str(up)] = [(up * 600 / 1000) + 150, 135]
                for down in levelelements[element]['down']:
                        objects["fantome"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/fantome.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown"]
                    )
                        scenes["scene1"].calques[2]["fantome"+str(down)] = [(down * 600 / 1000) + 150, 315]

            # case "normal":

            # case "liee":

            # case "silence":

            # case "cube":

            # case "pique":

            # case "orbe":
            
            # case "dash":

def initgameover():
    objects["gameoverscreen"].visible = False
    objects["gameoverscreen"].suivreScene = True


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
                        (scenes[scenecourante].calques[calque][objet][0]-(scenes[scenecourante].camera[0]*objects[objet].parallax[0]),scenes[scenecourante].calques[calque][objet][1]-(scenes[scenecourante].camera[1]*objects[objet].parallax[1]))
                    )
                else:
                    displaylist[objet] = ecran.blit(
                        pygame.transform.scale_by(objects[objet].renderActif(),
                        (objects[objet].taillex, objects[objet].tailley)),
                        (scenes[scenecourante].calques[calque][objet][0],scenes[scenecourante].calques[calque][objet][1])
                    )
            # Si l'objet est un Text
            if isinstance(objects[objet], Text) and objects[objet].visible:

                if not objects[objet].suivreScene:
                    if objects[objet].shadow:
                        displaylist[objet+ "_SHADOW"] = ecran.blit(objects[objet].renderShadow(), (scenes[scenecourante].calques[calque][objet][0]+objects[objet].sx-scenes[scenecourante].camera[0], scenes[scenecourante].calques[calque][objet][1]+objects[objet].sy-scenes[scenecourante].camera[1]))
                    displaylist[objet] = ecran.blit(objects[objet].renderText(), (scenes[scenecourante].calques[calque][objet][0]-scenes[scenecourante].camera[0], scenes[scenecourante].calques[calque][objet][1]-scenes[scenecourante].camera[1]))
                else:
                    if objects[objet].shadow:
                        displaylist[objet+ "_SHADOW"] = ecran.blit(objects[objet].renderShadow(), (scenes[scenecourante].calques[calque][objet][0]+objects[objet].sx, scenes[scenecourante].calques[calque][objet][1]+objects[objet].sy))
                    displaylist[objet] = ecran.blit(objects[objet].renderText(), (scenes[scenecourante].calques[calque][objet][0], scenes[scenecourante].calques[calque][objet][1]))


            # Si l'objet est un Bouton
            if isinstance(objects[objet], Bouton) and objects[objet].visible:
                # On augmente son compteur d'animation
                objects[objet].cptframe += 1

                if not objects[objet].suivreScene:
                    displaylist[objet] = ecran.blit(
                        pygame.transform.scale_by(objects[objet].renderButton(),
                        (objects[objet].taillex, objects[objet].tailley)),
                        (scenes[scenecourante].calques[calque][objet][0]-scenes[scenecourante].camera[0],scenes[scenecourante].calques[calque][objet][1]-scenes[scenecourante].camera[1])
                    )
                else:
                    displaylist[objet] = ecran.blit(
                        pygame.transform.scale_by(objects[objet].renderButton(),
                        (objects[objet].taillex, objects[objet].tailley)),
                        (scenes[scenecourante].calques[calque][objet][0],scenes[scenecourante].calques[calque][objet][1])
                    )
    # On réactualise l'écran
    pygame.display.update()