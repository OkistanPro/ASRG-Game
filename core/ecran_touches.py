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

objects = {"fond_touches" : Actif(
    {"anim1" : [PurePath("images/fonds/fond_ecran_touches.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"phase1" : Text(
    "Phase 1 :",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (255,255,255)
),
"touche_bas1" : Bouton(
    {"touche_bas1b" :
[
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")]
]},
{"touche_bas1b" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"touche_bas1b"
),
"touche_bas1txt" : Text(
    "J",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (0, 0, 0)
),
"touche_bas2" : Bouton(
    {"touche_bas2b" :
[
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")]
]},
{"touche_bas2b" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"touche_bas2b"
),
"touche_bas2txt" : Text(
    "K",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (0, 0, 0)
),
"touche_bas3" : Bouton(
    {"touche_bas3b" :
[
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")]
]},
{"touche_bas3b" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"touche_bas3b"
),
"touche_bas3txt" : Text(
    "L",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (0, 0, 0)
),
"touche_haut1" : Bouton(
    {"touche_haut1b" :
[
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")]
]},
{"touche_haut1b" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"touche_haut1b"
),
"touche_haut1txt" : Text(
    "S",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (0, 0, 0)
),
"touche_haut2" : Bouton(
    {"touche_haut2b" :
[
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")]
]},
{"touche_haut2b" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"touche_haut2b"
),
"touche_haut2txt" : Text(
    "D",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (0, 0, 0)
),
"touche_haut3" : Bouton(
    {"touche_haut3b" :
[
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")],
    [PurePath("images/interface/touche.png")]
]},
{"touche_haut3b" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"touche_haut3b"
),
"touche_haut3txt" : Text(
    "F",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (0, 0, 0)
),
"phase3" : Text(
    "Phase 3 :",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (255,255,255)
),
"touche_phase3" : Bouton(
    {"touche_phase3b" :
[
    [PurePath("images/interface/touche_espace.png")],
    [PurePath("images/interface/touche_espace.png")],
    [PurePath("images/interface/touche_espace.png")],
    [PurePath("images/interface/touche_espace.png")],
    [PurePath("images/interface/touche_espace.png")]
]},
{"touche_phase3b" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"touche_phase3b"
),
"touche_phase3txt" : Text(
    "Espace",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    35,
    (0, 0, 0)
),
"retour" : Bouton(
    {"flecheRetour" :
[
    [PurePath("images/interface/flecheretour.png")],
    [PurePath("images/interface/flecheretour.png")],
    [PurePath("images/interface/flecheretour.png")],
    [PurePath("images/interface/flecheretour.png")],
    [PurePath("images/interface/flecheretour.png")]
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
            "fond_touches" : [0, 0]
        },
        1: {
            "retour" : [0, 0],

            "phase1" : [50, 186],
            "touche_bas1" : [645, 181],
            "touche_bas1txt" : [655, 186],
            "touche_bas2" : [718, 181],
            "touche_bas2txt" : [728, 186],
            "touche_bas3" : [791, 181],
            "touche_bas3txt" : [801, 186],

            "touche_haut1" : [395, 181],
            "touche_haut1txt" : [405, 186],
            "touche_haut2" : [320, 181],
            "touche_haut2txt" : [330, 186],
            "touche_haut3" : [470, 181],
            "touche_haut3txt" : [480, 186],

            "phase3" : [50, 384],
            "touche_phase3" : [376, 379],
            "touche_phase3txt" : [521, 384]
        }
}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)
    objects["touche_bas1txt"].color_shadow = (180, 180, 180)
    objects["touche_bas2txt"].color_shadow = (180, 180, 180)
    objects["touche_bas3txt"].color_shadow = (180, 180, 180)

    objects["touche_haut1txt"].color_shadow = (180, 180, 180)
    objects["touche_haut2txt"].color_shadow = (180, 180, 180)
    objects["touche_haut3txt"].color_shadow = (180, 180, 180)

    objects["touche_phase3txt"].color_shadow = (180, 180, 180)

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["retour"].CLICKED:
        game.scenecourante = "parametres"
        
    

def loopbeforeupdate():
    pass

def loopafterupdate():
     global pause, button, gameovertimer, camera
     objects["retour"].activate(game.displaylist["retour"])