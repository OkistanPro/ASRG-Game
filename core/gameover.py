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
    game.objects["gameoverscreen"].visible = False
    game.objects["gameoverscreen"].suivreScene = True

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == game.objects["replay"].CLICKED and game.scenecourante == "gameover":
            game.scenecourante = "scene1"
            camera = [0, 0]
            pygame.mixer.music.play(start=0.0)
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    game.objects["replay"].activate(game.displaylist["replay"])