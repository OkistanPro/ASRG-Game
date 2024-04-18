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

objects = {"fondInfoNiv" : Actif(
    {"anim1" : [PurePath("images/interface/fond_Info_Niveau.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"imageNiv" : Actif(
{"anim1" : [PurePath("images/interface/ImageNiveau.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"iconeFacile" : Actif(
{"anim1" : [PurePath("images/interface/DifFacile.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"iconeMoyen" : Actif(
{"anim1" : [PurePath("images/interface/DifMoyen.png")]},
{"anim1" : [False, 5]},
"anim1"
),"iconeDur" : Actif(
{"anim1" : [PurePath("images/interface/DifDur.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"iconeDemon" : Actif(
{"anim1" : [PurePath("images/interface/DifDemon.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"phase1" : Actif(
{"anim1" : [PurePath("images/interface/phase1.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"phase2" : Actif(
    {"anim1" : [PurePath("images/interface/phase2.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"phase3" : Actif(
    {"anim1" : [PurePath("images/interface/phase3.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jouer" : Bouton(
    {"BoutonJouer" :
[
    [PurePath("images/interface/BoutonJouer1.png")],
    [PurePath("images/interface/BoutonJouer1.png")],
    [PurePath("images/interface/BoutonJouer1.png")],
    [PurePath("images/interface/BoutonJouer1.png")],
    [PurePath("images/interface/BoutonJouer1.png")]
]},
{"BoutonJouer" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"BoutonJouer"
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
),
"NomNiveau" : Text(
    "Niveau Test",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    40,
    (255,255,255)
),
"Scoremax1" : Text(
    "Score max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbScoremax1" : Text(
    "125000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
),
"Combomax1" : Text(
    "Combo max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbCombomax1" : Text(
    "120",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
),
"Scoremax2" : Text(
    "Score max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbScoremax2" : Text(
    "125000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
),
"Combomax2" : Text(
    "Combo max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbCombomax2" : Text(
    "120",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
),
"Scoremax3" : Text(
    "Score max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbScoremax3" : Text(
    "125000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
),
"Combomax3" : Text(
    "Combo max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbCombomax3" : Text(
    "120",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
)
}

initcalques = {
        0:{
            "fondInfoNiv" : [0, 0]
        },
        1:{
            "imageNiv" : [0, 0],
            "iconeFacile" : [10, 300],
            "iconeDur" : [160, 300],
            "iconeDemon" : [320, 300],
            "phase1" : [480, 145],
            "phase2" : [480, 246],
            "phase3" : [480, 347]

        },
        2:{
            #bloc phase 1
            "Scoremax1" : [600, 165],
            "NbScoremax1" : [780, 165],
            "Combomax1" : [600, 210],
            "NbCombomax1" : [780, 210],
            #bloc phase 2
            "Scoremax2" : [600, 266],
            "NbScoremax2" : [780, 266],
            "Combomax2" : [600, 311],
            "NbCombomax2" : [780, 311],
            #bloc phase 3
            "Scoremax3" : [600, 367],
            "NbScoremax3" : [780, 367],
            "Combomax3" : [600, 412],
            "NbCombomax3" : [780, 412],
            #nom niveau
            "NomNiveau" : [110, 220]
        },
        3:{
            "jouer" : [560, 460],
            "retour" : [160, 460]
        }
}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)
    pass

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["jouer"].CLICKED:
        game.scenecourante = "scene1"
        camera = [0, 0]
        pygame.mixer.music.play(start=0.0)
    if event.type == objects["retour"].CLICKED:
        game.scenecourante = "selectionniveau"
        
    

def loopbeforeupdate():
    pass

def loopafterupdate():
     global pause, button, gameovertimer, camera
     objects["jouer"].activate(game.displaylist["jouer"])
     objects["retour"].activate(game.displaylist["retour"])