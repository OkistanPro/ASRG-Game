import pygame
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
from classes import *

import game

import time

import copy

camera = [0, 0]

fond = (0, 0, 0)

objects = {
"fond_selection" : Actif(
    {"anim1" : [PurePath("images/fonds/animation/ecran_selecteur_niveau/ecran_selecteur_niveau_" + format(i, '05d') + ".png") for i in range(125)], 
    "anim2" : [PurePath("images/fonds/animation/ecran_selecteur_niveau2/ecran_selecteur_niveau2_" + format(i, '05d') + ".png") for i in range(125)]},
    {"anim1" : [True, 2],
    "anim2" : [True, 2]},
    "anim2"
),
"perso" : Bouton(
    {"logoperso" :
[
    [PurePath("images/interface/logoperso.png")],
    [PurePath("images/interface/logoperso.png")],
    [PurePath("images/interface/logoperso.png")],
    [PurePath("images/interface/logoperso.png")],
    [PurePath("images/interface/logoperso.png")]
]},
{"logoperso" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"logoperso"
),
"cadreniv" : Actif
    ({"anim1" : [PurePath("images/interface/cadreniv.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jaugevideniv" : Actif
    ({"anim1" : [PurePath("images/interface/jauge_selecteur_niveau.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jaugerempliniv" : Actif
    ({"anim1" : [PurePath("images/interface/bandeauniv.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"param" : Bouton(
    {"param" :
[
    [PurePath("images/interface/parametre.png")],
    [PurePath("images/interface/parametre.png")],
    [PurePath("images/interface/parametre.png")],
    [PurePath("images/interface/parametre.png")],
    [PurePath("images/interface/parametre.png")]
]},
{"param" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"param"
),
"niv1" : Actif
    ({"anim1" : [PurePath("images/fonds/fond_selection_niveau_Aurore.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"barreniv1" : Actif
    ({"anim1" : [PurePath("images/fonds/barre_fond_selecteur_niveau.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"fleche1" : Actif
    ({"anim1" : [PurePath("images/interface/fleche_gauche.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"niv2" : Actif
    ({"anim1" : [PurePath("images/fonds/fond_selection_niveau_Oriane.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"niv2" : Bouton(
    {"niveauOriane" :
[
    [PurePath("images/fonds/fond_selection_niveau_Oriane.png")],
    [PurePath("images/fonds/fond_selection_niveau_Oriane.png")],
    [PurePath("images/fonds/fond_selection_niveau_Oriane.png")],
    [PurePath("images/fonds/fond_selection_niveau_Oriane.png")],
    [PurePath("images/fonds/fond_selection_niveau_Oriane.png")]
]},
{"niveauOriane" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"niveauOriane"
),
"barreniv2" : Actif
    ({"anim1" : [PurePath("images/fonds/barre_fond_selecteur_niveau.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"fleche2" : Actif
    ({"anim1" : [PurePath("images/interface/fleche_droite.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"niv3" : Actif
    ({"anim1" : [PurePath("images/fonds/fond_selection_niveau_Jonathan.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"barreniv3" : Actif
    ({"anim1" : [PurePath("images/fonds/barre_fond_selecteur_niveau.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"cube1" : Actif
    ({"anim1" : [PurePath("images/interface/cubeblanc.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"cube2" : Actif
    ({"anim1" : [PurePath("images/interface/cubeblanc.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"nomniv" : Text(
    "Niveau Test",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (255, 255, 255)
),
"pourcentniv" : Text(
    "80%",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (255, 255, 255)
),
"difficulte" : Text(
    "1/3",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    30,
    (255, 255, 255)
),
"phase1" : Actif(
    {"anim1" : [PurePath("images/interface/icone_phase1.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"phase2" : Actif(
    {"anim1" : [PurePath("images/interface/icone_phase2.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"phase3" : Actif(
    {"anim1" : [PurePath("images/interface/icone_phase3.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"niveau" : Text(
    "Niv. 2",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255, 255, 255)
)
}


initcalques = {
        0:{
            "fond_selection" : [0, 0]
        },
        1:{
            "perso" : [0, 0],
            "cadreniv" : [335, 0],
            "jaugevideniv" : [345, 10],
            "jaugerempliniv" : [345, 10],
            "param" : [890, 0],
            "niv1" : [-296, 135],
            "barreniv1" : [-296, 278],
            "fleche1" : [123, 219],        #[480-(objects["niv2"].sprites["anim1"][0].get_rect().width/2)-10-(objects["fleche1"].sprites["anim1"][0].get_rect().width/2), 270-(objects["niv2"].sprites["anim1"][0].get_rect().height/2)],
            "niv2" : [257, 135],
            "barreniv2" : [257, 278],
            "niv3" : [811, 135],
            "barreniv3" : [811, 278],
            "fleche2" : [736, 221],  
            "cube1" : [0, 470],            #[0, 540-(objects["cube1"].sprites["anim1"][0].get_rect().height)],
            "cube2" : [890, 470]
        },
        2:{
            "nomniv" : [273, 292],
            "phase2" : [501, 282],       #[272+(objects["expliniv2"].sprites["anim1"][0].get_rect().width*3/4)-(objects["phase1"].sprites["anim1"][0].get_rect().width), 270+(objects["expliniv2"].sprites["anim1"][0].get_rect().height/4)-(objects["phase1"].sprites["anim1"][0].get_rect().height/4)],
            "phase1" : [563, 282],
            "phase3" : [625, 282],
            "pourcentniv" : [333, 357],
            "difficulte" : [569, 355],
            "niveau" : [460, 15]
        }
}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)
    objects["jaugerempliniv"].taillex = 0.45


def loopevent(event):
    if event.type == KEYDOWN and event.key == K_RETURN :
        game.scenecourante = "infoNiveau"
    if event.type == objects["param"].CLICKED:
        game.scenecourante = "parametres"
    if event.type == objects["perso"].CLICKED:
        game.scenecourante = "infoPerso"
    if event.type == objects["niv2"].CLICKED:
        game.scenecourante = "infoNiveau"
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["param"].activate(game.displaylist["param"])
    objects["perso"].activate(game.displaylist["perso"])
    objects["niv2"].activate(game.displaylist["niv2"])