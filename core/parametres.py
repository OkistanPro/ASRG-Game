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

objects = {"fond_param" : Actif(
    {"anim1" : [PurePath("images/fonds/fond_param.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"barreSon" : Actif(
    {"anim1" : [PurePath("images/interface/barreSon.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"rondBarreSon" : Actif(
    {"anim1" : [PurePath("images/interface/RainbowRond.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"Taille_ecran" : Text(
    "Taille de l'écran :",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (255,255,255)
),
"son" : Text(
    "Volume :",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (255,255,255)
),
"touches" : Bouton(
    {"touchesb" :
[
    [PurePath("images/interface/boutTouches.png")],
    [PurePath("images/interface/boutTouches.png")],
    [PurePath("images/interface/boutTouches.png")],
    [PurePath("images/interface/boutTouches.png")],
    [PurePath("images/interface/boutTouches.png")]
]},
{"touchesb" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"touchesb"
),
"tuto" : Bouton(
    {"tutob" :
[
    [PurePath("images/interface/boutRejTuto.png")],
    [PurePath("images/interface/boutRejTuto.png")],
    [PurePath("images/interface/boutRejTuto.png")],
    [PurePath("images/interface/boutRejTuto.png")],
    [PurePath("images/interface/boutRejTuto.png")]
]},
{"tutob" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"tutob"
),
"retour" : Bouton(
    {"flecheRetour" :
[
    [PurePath("images/interface/blurgflecheretour2.png")],
    [PurePath("images/interface/blurgflecheretour2.png")],
    [PurePath("images/interface/blurgflecheretour2.png")],
    [PurePath("images/interface/blurgflecheretour2.png")],
    [PurePath("images/interface/blurgflecheretour2.png")]
]},
{"flecheRetour" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"flecheRetour"
)
}

initcalques = {
        0:{
            "fond_param" : [0, 0]
        },
        1: {
            "retour" : [0, 0],
            "Taille_ecran" : [40, 100],
            "son" : [40, 170],
            "barreSon" : [220, 138],
            "rondBarreSon" : [245, 170],
            "touches" : [40, 250],
            "tuto" : [40, 390]
        }
}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)
    pass

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["tuto"].CLICKED:
        game.scenecourante = "scene1"
        camera = [0, 0]
    if event.type == objects["retour"].CLICKED:
        game.scenecourante = "selectionniveau"
    #if event.type == objects["touches"].CLICKED:
    #   game.scenecourante = "paramTouches"
        
    

def loopbeforeupdate():
    pass

def loopafterupdate():
     global pause, button, gameovertimer, camera
     objects["touches"].activate(game.displaylist["touches"])
     objects["retour"].activate(game.displaylist["retour"])
     objects["tuto"].activate(game.displaylist["tuto"])