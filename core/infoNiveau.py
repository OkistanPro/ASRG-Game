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
    {"anim1" : [PurePath("images/fonds/fond_dessus_info_niveau_Oriane.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"imageNiv" : Actif(
{"anim1" : [PurePath("images/fonds/fond_info_niveau_Oriane.png")]},
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
{"anim1" : [PurePath("images/interface/icone_phase1_Oriane.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"phase2" : Actif(
    {"anim1" : [PurePath("images/interface/icone_phase2_Oriane.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"phase3" : Actif(
    {"anim1" : [PurePath("images/interface/icone_phase3_Oriane.png")]},
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
"cube3" : Actif
    ({"anim1" : [PurePath("images/interface/cubeblanc.png")]},
    {"anim1" : [False, 5]},
    "anim1"
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
            "imageNiv" : [0, 0]
        },
        1:{
            "fondInfoNiv" : [0, 270],
            "iconeFacile" : [10, 300],
            "iconeDur" : [160, 300],
            "iconeDemon" : [320, 300],
            "phase1" : [530, 280],
            "phase2" : [530, 381],
            "phase3" : [530, 482]

        },
        2:{
            #bloc phase 1
            "Scoremax1" : [600, 275], #+10
            "NbScoremax1" : [780, 275],
            "Combomax1" : [600, 315], #+5
            "NbCombomax1" : [780, 315],
            #bloc phase 2
            "Scoremax2" : [600, 376], #+10
            "NbScoremax2" : [780, 376],
            "Combomax2" : [600, 416],
            "NbCombomax2" : [780, 416],
            #bloc phase 3
            "Scoremax3" : [600, 477],
            "NbScoremax3" : [780, 477],
            "Combomax3" : [600, 517],
            "NbCombomax3" : [780, 517],
            #nom niveau
            "NomNiveau" : [110, 220]
        },
        3:{
            "jouer" : [85, 420],
            "retour" : [0, 0],
            "cube1" : [890, 0],
            #"cube2" : [0, 470],            
            #"cube3" : [890, 470]
        }
}

objects["Scoremax1"].shadow = True
objects["NbScoremax1"].shadow = True
objects["Combomax1"].shadow = True
objects["NbCombomax1"].shadow = True

objects["Scoremax2"].shadow = True
objects["NbScoremax2"].shadow = True
objects["Combomax2"].shadow = True
objects["NbCombomax2"].shadow = True

objects["Scoremax3"].shadow = True
objects["NbScoremax3"].shadow = True
objects["Combomax3"].shadow = True
objects["NbCombomax3"].shadow = True

objects["NomNiveau"].shadow = True

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)
    pass

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["jouer"].CLICKED:
        game.scenecourante = "chargement"
        camera = [0, 0]
    if event.type == objects["retour"].CLICKED:
        game.scenecourante = "selectionniveau"
        
    

def loopbeforeupdate():
    pass

def loopafterupdate():
     global pause, button, gameovertimer, camera
     objects["jouer"].activate(game.displaylist["jouer"])
     objects["retour"].activate(game.displaylist["retour"])