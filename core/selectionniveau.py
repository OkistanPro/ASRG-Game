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
    {"anim1" : [PurePath("images/fonds/fondselecteur.jpg")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"perso" : Actif
    ({"anim1" : [PurePath("images/interface/logopersodegrad.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"cadreniv" : Actif
    ({"anim1" : [PurePath("images/interface/cadrenivcursed.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jaugevideniv" : Actif
    ({"anim1" : [PurePath("images/interface/bandeaunivcursed.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jaugerempliniv" : Actif
    ({"anim1" : [PurePath("images/interface/bandeauniv2.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"soleilparam" : Actif
    ({"anim1" : [PurePath("images/interface/soleilparam.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"niv1" : Actif
    ({"anim1" : [PurePath("images/interface/choixniv.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"expliniv1" : Actif
    ({"anim1" : [PurePath("images/interface/inscriptionniv.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"fleche1" : Actif
    ({"anim1" : [PurePath("images/interface/flechechoix1cursed.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"niv2" : Actif
    ({"anim1" : [PurePath("images/interface/choixniv.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"expliniv2" : Actif
    ({"anim1" : [PurePath("images/interface/inscriptionniv.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"fleche2" : Actif
    ({"anim1" : [PurePath("images/interface/flechechoix2cursed.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"niv3" : Actif
    ({"anim1" : [PurePath("images/interface/choixniv.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"expliniv3" : Actif
    ({"anim1" : [PurePath("images/interface/inscriptionniv.png")]},
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
"Bienvenue" : Text(
    "Appuyez sur 'Entrée' pour commencer",
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
            "cadreniv" : [330, 0],         #[480-(objects["cadreniv"].sprites["anim1"][0].get_rect().width/2), 0],
            "jaugevideniv" : [333, 3],     #[480-(objects["jaugevideniv"].sprites["anim1"][0].get_rect().width/2), 0],
            "jaugerempliniv" : [333, 3],   #[480-(objects["jaugerempliniv"].sprites["anim1"][0].get_rect().width/2), 0],
            "soleilparam" : [410, 0],      #[960-(objects["soleilparam"].sprites["anim1"][0].get_rect().width), 0],
            "niv1" : [-265, 132],          #[0-(objects["niv1"].sprites["anim1"][0].get_rect().width*2/3), 132],
            "expliniv1" : [-265, 270],
            "fleche1" : [123, 218],        #[480-(objects["niv2"].sprites["anim1"][0].get_rect().width/2)-10-(objects["fleche1"].sprites["anim1"][0].get_rect().width/2), 270-(objects["niv2"].sprites["anim1"][0].get_rect().height/2)],
            "niv2" : [265, 132],           #[480-(objects["niv2"].sprites["anim1"][0].get_rect().width/2), 270-(objects["niv2"].sprites["anim1"][0].get_rect().height/2)],
            "expliniv2" : [265, 270],
            "fleche2" : [745, 218],        #[480-(objects["niv2"].sprites["anim1"][0].get_rect().width/2)+10+(objects["fleche2"].sprites["anim1"][0].get_rect().width/2), 270-(objects["niv2"].sprites["anim1"][0].get_rect().height/2)],
            "niv3" : [795, 132],           #[960-(objects["niv3"].sprites["anim1"][0].get_rect().width/3), 132],
            "expliniv3" : [795, 270],
            "cube1" : [0, 470],            #[0, 540-(objects["cube1"].sprites["anim1"][0].get_rect().height)],
            "cube2" : [890, 470]           #[960-(objects["cube2"].sprites["anim1"][0].get_rect().width), 540-(objects["cube2"].sprites["anim1"][0].get_rect().height)],
        }
}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)

def loopevent(event):
    if event.type == KEYDOWN and event.key == K_RETURN :
        game.scenecourante = "scene1"
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    pass