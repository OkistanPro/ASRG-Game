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

objects = {"fond_ecranTITRE" : Actif(
    {"anim1" : [PurePath("images/fonds/fond_ecranTITRE.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"A" : Actif({"anim1" : [PurePath("images/interface/A.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"S" : Actif({"anim1" : [PurePath("images/interface/S.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"R" : Actif({"anim1" : [PurePath("images/interface/R.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"G" : Actif({"anim1" : [PurePath("images/interface/G.png")]},
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
            "fond_ecranTITRE" : [0, 0]
        },
        1:{
            "A" : [380, 150],
            "S" : [491, 150],
            "R" : [380, 260],
            "G" : [491, 260],
            "Bienvenue" : [311, 445]
        }
}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)
    objects["Bienvenue"].shadow = True
    objects["Bienvenue"].color_shadow = (135,206,250)

def loopevent(event):
    if event.type == KEYDOWN and event.key == K_RETURN :
        game.scenecourante = "selectioniveau"
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    pass