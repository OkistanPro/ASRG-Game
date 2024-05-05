import pygame
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
from classes import *

import game

import time

import copy

# Propriétés des scènes

camera = [0, 0]

fond = (0, 0, 0)

objects = {}

calques = {}

gameoversound = pygame.mixer.Sound(PurePath("music/defaite.wav"))

def init():
    global objects, calques, camera, fond, gameoversound
    # Définition des objets
    if not objects:
        objects.update({"retour" : Bouton({"boutretour" :
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
            )})
    # Placement des objets
    calques.update({
        0:{
            "fondgameover" : [0, 0]
        },
        1:{
            "retour" : [0, 0],
            "replay" : [890, 0]
        }})

    gameoversound.play(loops=-1)

def loopevent(event):
    # Evénements
    global pause, button, gameovertimer, camera, gameoversound
    if event.type == objects["replay"].CLICKED and game.scenecourante == "gameover":
        pygame.mixer.music.unload()
        gameoversound.stop()
        game.selectsound.play()
        game.scenecourante = "scene1"
        camera = [0, 0]
    if event.type == objects["retour"].CLICKED and game.scenecourante == "gameover":
        gameoversound.stop()
        game.selectsound.play()
        game.scenecourante = "selectionniveau"
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["retour"].activate(game.displaylist["retour"])
    objects["replay"].activate(game.displaylist["replay"])