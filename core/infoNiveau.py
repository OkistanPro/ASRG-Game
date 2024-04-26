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
    {"anim1" : [PurePath("images/fonds/fond_dessus_info_niveau.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"imageNiv" : Actif(
{"anim1" : [PurePath("images/fonds/fond_info_niveau_Oriane.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"iconeFacile" : Bouton(
    {"iconeF" :
[
    [PurePath("images/interface/difficult_easy.png")],
    [PurePath("images/interface/difficult_easy.png")],
    [PurePath("images/interface/difficult_easy.png")],
    [PurePath("images/interface/difficult_easy.png")],
    [PurePath("images/interface/difficult_easy.png")]
]},
{"iconeF" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"iconeF"
),
"iconeMoyen" : Bouton(
    {"iconeM" :
[
    [PurePath("images/interface/difficult_normal.png")],
    [PurePath("images/interface/difficult_normal.png")],
    [PurePath("images/interface/difficult_normal.png")],
    [PurePath("images/interface/difficult_normal.png")],
    [PurePath("images/interface/difficult_normal.png")]
]},
{"iconeM" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"iconeM"
),
"iconeDur" : Bouton(
    {"iconeDu" :
[
    [PurePath("images/interface/difficult_hard.png")],
    [PurePath("images/interface/difficult_hard.png")],
    [PurePath("images/interface/difficult_hard.png")],
    [PurePath("images/interface/difficult_hard.png")],
    [PurePath("images/interface/difficult_hard.png")]
]},
{"iconeDu" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"iconeDu"
),
"iconeDemon" : Bouton(
    {"iconeD" :
[
    [PurePath("images/interface/difficult_hell.png")],
    [PurePath("images/interface/difficult_hell.png")],
    [PurePath("images/interface/difficult_hell.png")],
    [PurePath("images/interface/difficult_hell.png")],
    [PurePath("images/interface/difficult_hell.png")]
]},
{"iconeD" :[
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5],
    [False, 0, 5]
]},
"iconeD"
),
"phase1" : Actif(
{"anim1" : [PurePath("images/interface/icone_phase1.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"phase2" : Actif(
    {"anim1" : [PurePath("images/interface/icone_phase2.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"phase3" : Actif(
    {"anim1" : [PurePath("images/interface/icone_phase3.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"jouer" : Bouton(
    {"BoutonJouer" :
[
    [PurePath("images/interface/BoutonJouer.png")],
    [PurePath("images/interface/BoutonJouer.png")],
    [PurePath("images/interface/BoutonJouer.png")],
    [PurePath("images/interface/BoutonJouer.png")],
    [PurePath("images/interface/BoutonJouer.png")]
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
"cube" : Actif
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
"NbScoremax1F" : Text(
    "125000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbScoremax1Dur" : Text(
    "10000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbScoremax1Demon" : Text(
    "0",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"Combomax1" : Text(
    "Combo max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbCombomax1F" : Text(
    "120",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbCombomax1Dur" : Text(
    "100",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbCombomax1Demon" : Text(
    "0",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"Scoremax2" : Text(
    "Score max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbScoremax2F" : Text(
    "125000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbScoremax2Dur" : Text(
    "10000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbScoremax2Demon" : Text(
    "0",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"Combomax2" : Text(
    "Combo max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbCombomax2F" : Text(
    "120",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbCombomax2Dur" : Text(
    "100",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbCombomax2Demon" : Text(
    "0",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"Scoremax3" : Text(
    "Score max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbScoremax3F" : Text(
    "125000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbScoremax3Dur" : Text(
    "10000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbScoremax3Demon" : Text(
    "0",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"Combomax3" : Text(
    "Combo max",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,255,255)
),
"NbCombomax3F" : Text(
    "120",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbCombomax3Dur" : Text(
    "100",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
"NbCombomax3Demon" : Text(
    "0",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (236,52,22)
),
#ronds de sélection
"selectionFacile" : Actif(
    {"anim1" : [PurePath("images/interface/rond_selection.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"selectionDur" : Actif(
    {"anim1" : [PurePath("images/interface/rond_selection.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"selectionDemon" : Actif(
    {"anim1" : [PurePath("images/interface/rond_selection.png")]},
    {"anim1" : [False, 5]},
    "anim1"
)
}

initcalques = {
        0:{
            "imageNiv" : [0, 0]
        },
        1:{
            "fondInfoNiv" : [0, 270],
            "selectionFacile" : [18, 288],
            "selectionDur" : [148, 288],
            "selectionDemon" : [288, 288],
            "iconeFacile" : [30, 300],
            "iconeDur" : [160, 300],
            "iconeDemon" : [300, 300],
            "phase1" : [530, 280],
            "phase2" : [530, 381],
            "phase3" : [530, 482]

        },
        2:{
            #bloc phase 1
            "Scoremax1" : [600, 275], #+10
            "NbScoremax1F" : [780, 275],
            "NbScoremax1Dur" : [780, 275],
            "NbScoremax1Demon" : [780, 275],
            "Combomax1" : [600, 315], #+5
            "NbCombomax1F" : [780, 315],
            "NbCombomax1Dur" : [780, 315],
            "NbCombomax1Demon" : [780, 315],
            #bloc phase 2
            "Scoremax2" : [600, 376], #+10
            "NbScoremax2F" : [780, 376],
            "NbScoremax2Dur" : [780, 376],
            "NbScoremax2Demon" : [780, 376],
            "Combomax2" : [600, 416],
            "NbCombomax2F" : [780, 416],
            "NbCombomax2Dur" : [780, 416],
            "NbCombomax2Demon" : [780, 416],
            #bloc phase 3
            "Scoremax3" : [600, 477],
            "NbScoremax3F" : [780, 477],
            "NbScoremax3Dur" : [780, 477],
            "NbScoremax3Demon" : [780, 477],
            "Combomax3" : [600, 517],
            "NbCombomax3F" : [780, 517],
            "NbCombomax3Dur" : [780, 517],
            "NbCombomax3Demon" : [780, 517],
            #nom niveau
            "NomNiveau" : [110, 220]
        },
        3:{
            "jouer" : [85, 420],
            "retour" : [0, 0],
            "cube" : [890, 0]
        }
}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    calques = copy.deepcopy(initcalques)
    objects["selectionDur"].visible = False
    objects["selectionDemon"].visible = False

    objects["NbScoremax1Dur"].visible = False
    objects["NbScoremax1Demon"].visible = False
    objects["NbCombomax1Dur"].visible = False
    objects["NbCombomax1Demon"].visible = False

    objects["NbScoremax2Dur"].visible = False
    objects["NbScoremax2Demon"].visible = False
    objects["NbCombomax2Dur"].visible = False
    objects["NbCombomax2Demon"].visible = False

    objects["NbScoremax3Dur"].visible = False
    objects["NbScoremax3Demon"].visible = False
    objects["NbCombomax3Dur"].visible = False
    objects["NbCombomax3Demon"].visible = False
    

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["iconeFacile"].CLICKED:
        objects["selectionFacile"].visible = True
        objects["selectionDur"].visible = False
        objects["selectionDemon"].visible = False

        objects["NbScoremax1Dur"].visible = False
        objects["NbScoremax1Demon"].visible = False
        objects["NbCombomax1Dur"].visible = False
        objects["NbCombomax1Demon"].visible = False

        objects["NbScoremax2Dur"].visible = False
        objects["NbScoremax2Demon"].visible = False
        objects["NbCombomax2Dur"].visible = False
        objects["NbCombomax2Demon"].visible = False

        objects["NbScoremax3Dur"].visible = False
        objects["NbScoremax3Demon"].visible = False
        objects["NbCombomax3Dur"].visible = False
        objects["NbCombomax3Demon"].visible = False

        objects["NbScoremax1F"].visible = True
        objects["NbCombomax1F"].visible = True
        objects["NbScoremax2F"].visible = True
        objects["NbCombomax2F"].visible = True
        objects["NbScoremax3F"].visible = True
        objects["NbCombomax3F"].visible = True


    if event.type == objects["iconeDur"].CLICKED:
        objects["selectionDur"].visible = True
        objects["selectionFacile"].visible = False
        objects["selectionDemon"].visible = False

        objects["NbScoremax1Demon"].visible = False
        objects["NbScoremax1F"].visible = False
        objects["NbCombomax1Demon"].visible = False
        objects["NbCombomax1F"].visible = False

        objects["NbScoremax2Demon"].visible = False
        objects["NbScoremax2F"].visible = False
        objects["NbCombomax2Demon"].visible = False
        objects["NbCombomax2F"].visible = False

        objects["NbScoremax3Demon"].visible = False
        objects["NbScoremax3F"].visible = False
        objects["NbCombomax3Demon"].visible = False
        objects["NbCombomax3F"].visible = False

        objects["NbScoremax1Dur"].visible = True
        objects["NbCombomax1Dur"].visible = True
        objects["NbScoremax2Dur"].visible = True
        objects["NbCombomax2Dur"].visible = True
        objects["NbScoremax3Dur"].visible = True
        objects["NbCombomax3Dur"].visible = True

    if event.type == objects["iconeDemon"].CLICKED:
        objects["selectionDemon"].visible = True
        objects["selectionFacile"].visible = False
        objects["selectionDur"].visible = False

        objects["NbScoremax1Dur"].visible = False
        objects["NbScoremax1F"].visible = False
        objects["NbCombomax1Dur"].visible = False
        objects["NbCombomax1F"].visible = False

        objects["NbScoremax2Dur"].visible = False
        objects["NbScoremax2F"].visible = False
        objects["NbCombomax2Dur"].visible = False
        objects["NbCombomax2F"].visible = False

        objects["NbScoremax3Dur"].visible = False
        objects["NbScoremax3F"].visible = False
        objects["NbCombomax3Dur"].visible = False
        objects["NbCombomax3F"].visible = False

        objects["NbScoremax1Demon"].visible = True
        objects["NbCombomax1Demon"].visible = True
        objects["NbScoremax2Demon"].visible = True
        objects["NbCombomax2Demon"].visible = True
        objects["NbScoremax3Demon"].visible = True
        objects["NbCombomax3Demon"].visible = True

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
     objects["iconeFacile"].activate(game.displaylist["iconeFacile"])
     objects["iconeDur"].activate(game.displaylist["iconeDur"])
     objects["iconeDemon"].activate(game.displaylist["iconeDemon"])