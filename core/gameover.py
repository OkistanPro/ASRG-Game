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
"retour" : Bouton({"boutretour" :
[
    [PurePath("images/interface/flecheretour.png")],
    [PurePath("images/interface/flecheretour.png")],
    [PurePath("images/interface/flecheretour.png")],
    [PurePath("images/interface/flecheretour.png")],
    [PurePath("images/interface/flecheretour.png")]
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
    [PurePath("images/interface/Fleche_Recommencer.png")],
    [PurePath("images/interface/Fleche_Recommencer.png")],
    [PurePath("images/interface/Fleche_Recommencer.png")],
    [PurePath("images/interface/Fleche_Recommencer.png")],
    [PurePath("images/interface/Fleche_Recommencer.png")]
]},
{"boutreplay" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"boutreplay"),
"fondgameover" : Actif(
    {"anim1" : [PurePath("images/fonds/fond_game_over.png")]},
    {"anim1" : [False, 5]},
    "anim1"
)
}

# valeurs de scenes

initcalques = {
        0:{
            "fondgameover" : [0, 0]
        },
        1:{
            "retour" : [0, 0],
            "replay" : [890, 0]
        }}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    # Setup les objets (changement des propriétés de chaque objet)
    calques = copy.deepcopy(initcalques)

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["replay"].CLICKED and game.scenecourante == "gameover":
        game.scenecourante = "scene1"
        camera = [0, 0]
        pygame.mixer.music.play(start=0.0)
    if event.type == objects["retour"].CLICKED and game.scenecourante == "gameover":
        game.scenecourante = "selectionniveau"
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["retour"].activate(game.displaylist["retour"])
    objects["replay"].activate(game.displaylist["replay"])