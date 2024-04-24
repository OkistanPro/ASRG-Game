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
    {"anim1" : [PurePath("images/fonds/ecran_selecteur_niveau2.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"perso" : Actif
    ({"anim1" : [PurePath("images/interface/logoperso.png")]},
    {"anim1" : [False, 5]},
    "anim1"
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
    ({"anim1" : [PurePath("images/fonds/fond_selection_niveau_Oriane.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"expliniv1" : Actif
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
"expliniv2" : Actif
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
    ({"anim1" : [PurePath("images/fonds/fond_selection_niveau_Oriane.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"expliniv3" : Actif
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
    (0, 0, 0)
),
"pourcentniv" : Text(
    "80%",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (0, 0, 0)
),
"difficulte" : Text(
    "1/3",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    30,
    (0, 0, 0)
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
            "expliniv1" : [-296, 270],
            "fleche1" : [123, 219],        #[480-(objects["niv2"].sprites["anim1"][0].get_rect().width/2)-10-(objects["fleche1"].sprites["anim1"][0].get_rect().width/2), 270-(objects["niv2"].sprites["anim1"][0].get_rect().height/2)],
            "niv2" : [257, 135],
            "expliniv2" : [257, 270],
            "niv3" : [811, 135],
            "expliniv3" : [811, 270],
            "fleche2" : [736, 221],  
            "cube1" : [0, 470],            #[0, 540-(objects["cube1"].sprites["anim1"][0].get_rect().height)],
            "cube2" : [890, 470]
        },
        2:{
            "nomniv" : [273, 290],
            "phase2" : [501, 278],       #[272+(objects["expliniv2"].sprites["anim1"][0].get_rect().width*3/4)-(objects["phase1"].sprites["anim1"][0].get_rect().width), 270+(objects["expliniv2"].sprites["anim1"][0].get_rect().height/4)-(objects["phase1"].sprites["anim1"][0].get_rect().height/4)],
            "phase1" : [563, 278],
            "phase3" : [625, 278],
            "pourcentniv" : [333, 357],
            "difficulte" : [569, 355]
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
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["param"].activate(game.displaylist["param"])