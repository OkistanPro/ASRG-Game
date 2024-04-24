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
"fond_chargement" : Actif(
    {"anim1" : [PurePath("images/fonds/fond_chargement_niveau_Oriane.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"bandeauchar" : Actif(
    {"anim1" : [PurePath("images/interface/bandeauchargement.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"rondchargement" : Actif(
    {"anim1" : [PurePath("images/interface/iconechar.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"chargement" : Text(
    "Chargement...",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    50,
    (0, 0, 0)
),
"course1" : Actif(
    {"anim1" : [PurePath("images/interface/filcourse.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"course2" : Actif(
    {"anim1" : [PurePath("images/interface/filcourse.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"course3" : Actif(
    {"anim1" : [PurePath("images/interface/filcourse.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"bonhomme" : Actif(
    {"anim1" : [PurePath("images/interface/persochar.png")]},
    {"anim1" : [False, 5]},
    "anim1"
)
}

initcalques = {
        0:{
            "fond_chargement" : [0, 0]
        },
        1:{
            "bandeauchar" : [0, 460]
        },
        2:{
            "rondchargement" : [16, 468],
            "chargement" : [95, 485],
            "course1" : [575, 480],
            "course2" : [620, 500],
            "course3" : [545, 520],
            "bonhomme" : [705, 465]
        }
}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)
    objects["course2"].taillex = 0.75

def loopevent(event):
    if event.type == KEYDOWN and event.key == K_RETURN :
        game.scenecourante = "scene1"
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    pass