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

objects = {}

calques = {}

def init():
    global objects, calques, camera, fond
    if not objects:
        objects.update({"fond_touches" : Actif(
            {"anim1" : [PurePath("images/fonds/animation/ecran_touches/" + format(i, '05d') + ".jpg") for i in range(150)]},
            {"anim1" : [True, 1]},
            "anim1"
            ),
            "phase1" : Text(
                "Phase 1 :",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                35,
                (255,255,255)
            ),
            "bas" : Text(
                "Bas",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255,255,255)
            ),
            "touche_bas1" : Bouton(
                {"touche_bas1a" :
            [
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")]
            ],
                "touche_bas1b" :
            [
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")]
            ]
            },
            {"touche_bas1a" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ],
            "touche_bas1b" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "touche_bas1a"
            ),
            "touche_bas1txt" : Text(
                pygame.key.name(game.boutons["bas"][0]).upper(),
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                35,
                (0, 0, 0)
            ),
            "touche_bas2" : Bouton(
                {"touche_bas2a" :
            [
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")]
            ],
                "touche_bas2b" :
            [
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")]
            ]
            },
            {"touche_bas2a" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ],
            "touche_bas2b" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "touche_bas2a"
            ),
            "touche_bas2txt" : Text(
                pygame.key.name(game.boutons["bas"][1]).upper(),
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                35,
                (0, 0, 0)
            ),
            "touche_bas3" : Bouton(
                {"touche_bas3a" :
            [
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")]
            ],
                "touche_bas3b" :
            [
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")]
            ]
            },
            {"touche_bas3a" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ],
            "touche_bas3b" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "touche_bas3a"
            ),
            "touche_bas3txt" : Text(
                pygame.key.name(game.boutons["bas"][2]).upper(),
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                35,
                (0, 0, 0)
            ),
            "haut" : Text(
                "Haut",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255,255,255)
            ),
            "touche_haut1" : Bouton(
                {"touche_haut1a" :
            [
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")]
            ],
                "touche_haut1b" :
            [
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")]
            ]
            },
            {"touche_haut1a" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ],
            "touche_haut1b" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "touche_haut1a"
            ),
            "touche_haut1txt" : Text(
                pygame.key.name(game.boutons["haut"][0]).upper(),
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                35,
                (0, 0, 0)
            ),
            "touche_haut2" : Bouton(
                {"touche_haut2a" :
            [
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")]
            ],
                "touche_haut2b" :
            [
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")]
            ]
            },
            {"touche_haut2a" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ],
            "touche_haut2b" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "touche_haut2a"
            ),
            "touche_haut2txt" : Text(
                pygame.key.name(game.boutons["haut"][1]).upper(),
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                35,
                (0, 0, 0)
            ),
            "touche_haut3" : Bouton(
                {"touche_haut3a" :
            [
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")],
                [PurePath("images/interface/touche.png")]
            ],
                "touche_haut3b" :
            [
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")],
                [PurePath("images/interface/toucheGrise.png")]
            ]
            },
            {"touche_haut3a" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ],
            "touche_haut3b" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "touche_haut3a"
            ),
            "touche_haut3txt" : Text(
                pygame.key.name(game.boutons["haut"][2]).upper(),
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
                {"touche_phase3a" :
            [
                [PurePath("images/interface/touche_espace.png")],
                [PurePath("images/interface/touche_espace.png")],
                [PurePath("images/interface/touche_espace.png")],
                [PurePath("images/interface/touche_espace.png")],
                [PurePath("images/interface/touche_espace.png")]
            ],
                "touche_phase3b" :
            [
                [PurePath("images/interface/touche_espaceGrise.png")],
                [PurePath("images/interface/touche_espaceGrise.png")],
                [PurePath("images/interface/touche_espaceGrise.png")],
                [PurePath("images/interface/touche_espaceGrise.png")],
                [PurePath("images/interface/touche_espaceGrise.png")]
            ]
            },
            {"touche_phase3a" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ],
            "touche_phase3b" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "touche_phase3a"
            ),
            "touche_phase3txt" : Text(
                pygame.key.name(game.boutons["saut"]).upper(),
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                35,
                (0, 0, 0)
            ),
            "fondgris" : Actif(
                {"anim1" : [PurePath("images/fonds/fondpause.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "choix" : Actif(
                {"anim1" : [PurePath("images/interface/cadreChoixTouches.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "choixtxt" : Text(
                "Choississez une touche",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                20,
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
        })
    calques.update({
        0:{
            "fond_touches" : [0, 0]
        },
        1: {
            "phase1" : [50, 186],
            "bas" : [718, 146],
            "touche_bas1" : [645, 181],
            "touche_bas1txt" : [665-(objects["touche_bas1txt"].renderText().get_rect().width/2), 186],
            "touche_bas2" : [718, 181],
            "touche_bas2txt" : [738-(objects["touche_bas2txt"].renderText().get_rect().width/2), 186],
            "touche_bas3" : [791, 181],
            "touche_bas3txt" : [811-(objects["touche_bas3txt"].renderText().get_rect().width/2), 186],

            "haut" : [387, 146],
            "touche_haut1" : [395, 181],
            "touche_haut1txt" : [415-(objects["touche_haut1txt"].renderText().get_rect().width/2), 186],
            "touche_haut2" : [320, 181],
            "touche_haut2txt" : [340-(objects["touche_haut2txt"].renderText().get_rect().width/2), 186],
            "touche_haut3" : [470, 181],
            "touche_haut3txt" : [490-(objects["touche_haut3txt"].renderText().get_rect().width/2), 186],

            "phase3" : [50, 384],
            "touche_phase3" : [376, 379],
            "touche_phase3txt" : [576-(objects["touche_phase3txt"].renderText().get_rect().width/2), 384],

            "fondgris" : [0, 0],
            "choix" : [305, 270],
            "choixtxt" : [376, 295],

            "retour" : [0, 0]
    }})
    objects["touche_bas1txt"].color_shadow = (180, 180, 180)
    objects["touche_bas2txt"].color_shadow = (180, 180, 180)
    objects["touche_bas3txt"].color_shadow = (180, 180, 180)

    objects["touche_haut1txt"].color_shadow = (180, 180, 180)
    objects["touche_haut2txt"].color_shadow = (180, 180, 180)
    objects["touche_haut3txt"].color_shadow = (180, 180, 180)

    objects["touche_phase3txt"].color_shadow = (180, 180, 180)

    objects["choixtxt"].shadow = False

    objects["fondgris"].visible = False
    objects["choix"].visible = False
    objects["choixtxt"].visible = False

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["retour"].CLICKED:
        game.selectsound.play()
        objects["touche_bas1"].animCourante = "touche_bas1a"
        objects["touche_bas2"].animCourante = "touche_bas2a"
        objects["touche_bas3"].animCourante = "touche_bas3a"
        objects["touche_haut1"].animCourante = "touche_haut1a"
        objects["touche_haut2"].animCourante = "touche_haut2a"
        objects["touche_haut3"].animCourante = "touche_haut3a"
        objects["touche_phase3"].animCourante = "touche_phase3a"
        objects["fondgris"].visible = False
        objects["choix"].visible = False
        objects["choixtxt"].visible = False
        game.scenecourante = "parametres"

    if event.type == objects["touche_bas1"].CLICKED:
        game.selectsound.play()
        objects["touche_bas1"].animCourante = "touche_bas1b"
        objects["fondgris"].visible = True
        objects["choix"].visible = True
        objects["choixtxt"].visible = True

    if event.type == objects["touche_bas2"].CLICKED:
        game.selectsound.play()
        objects["touche_bas2"].animCourante = "touche_bas2b"
        objects["fondgris"].visible = True
        objects["choix"].visible = True
        objects["choixtxt"].visible = True

    if event.type == objects["touche_bas3"].CLICKED:
        game.selectsound.play()
        objects["touche_bas3"].animCourante = "touche_bas3b"
        objects["fondgris"].visible = True
        objects["choix"].visible = True
        objects["choixtxt"].visible = True

    if event.type == objects["touche_haut1"].CLICKED:
        game.selectsound.play()
        objects["touche_haut1"].animCourante = "touche_haut1b"
        objects["fondgris"].visible = True
        objects["choix"].visible = True
        objects["choixtxt"].visible = True
    
    if event.type == objects["touche_haut2"].CLICKED:
        game.selectsound.play()
        objects["touche_haut2"].animCourante = "touche_haut2b"
        objects["fondgris"].visible = True
        objects["choix"].visible = True
        objects["choixtxt"].visible = True

    if event.type == objects["touche_haut3"].CLICKED:
        game.selectsound.play()
        objects["touche_haut3"].animCourante = "touche_haut3b"
        objects["fondgris"].visible = True
        objects["choix"].visible = True
        objects["choixtxt"].visible = True

    if event.type == objects["touche_phase3"].CLICKED:
        game.selectsound.play()
        objects["touche_phase3"].animCourante = "touche_phase3b"
        objects["fondgris"].visible = True
        objects["choix"].visible = True
        objects["choixtxt"].visible = True

    if event.type == KEYDOWN and objects["touche_bas1"].animCourante == "touche_bas1b" and ((event.key in range(97,123)) or event.key==K_UP or event.key==K_DOWN\
        or event.key==K_LEFT or event.key==K_RIGHT) and not (event.key in game.boutons["bas"] or event.key in game.boutons["haut"]):
        game.boutons["bas"][0] = event.key
        objects["touche_bas1txt"].changeTexte(pygame.key.name(event.key).upper())
        calques[1]["touche_bas1txt"][0] = 665-(objects["touche_bas1txt"].renderText().get_rect().width/2)
        objects["touche_bas1"].animCourante = "touche_bas1a"
        objects["fondgris"].visible = False
        objects["choix"].visible = False
        objects["choixtxt"].visible = False
        print(game.boutons)

    if event.type == KEYDOWN and objects["touche_bas2"].animCourante == "touche_bas2b" and ((event.key in range(97,123)) or event.key==K_UP or event.key==K_DOWN\
        or event.key==K_LEFT or event.key==K_RIGHT) and not (event.key in game.boutons["bas"] or event.key in game.boutons["haut"]):
        game.boutons["bas"][1] = event.key
        objects["touche_bas2txt"].changeTexte(pygame.key.name(event.key).upper())
        calques[1]["touche_bas2txt"][0] = 738-(objects["touche_bas2txt"].renderText().get_rect().width/2)
        objects["touche_bas2"].animCourante = "touche_bas2a"
        objects["fondgris"].visible = False
        objects["choix"].visible = False
        objects["choixtxt"].visible = False
        print(game.boutons)

    if event.type == KEYDOWN and objects["touche_bas3"].animCourante == "touche_bas3b" and ((event.key in range(97,123)) or event.key==K_UP or event.key==K_DOWN\
        or event.key==K_LEFT or event.key==K_RIGHT) and not (event.key in game.boutons["bas"] or event.key in game.boutons["haut"]):
        game.boutons["bas"][2] = event.key
        objects["touche_bas3txt"].changeTexte(pygame.key.name(event.key).upper())
        calques[1]["touche_bas3txt"][0] = 811-(objects["touche_bas3txt"].renderText().get_rect().width/2)
        objects["touche_bas3"].animCourante = "touche_bas3a"
        objects["fondgris"].visible = False
        objects["choix"].visible = False
        objects["choixtxt"].visible = False
        print(game.boutons)
    
    if event.type == KEYDOWN and objects["touche_haut1"].animCourante == "touche_haut1b" and ((event.key in range(97,123)) or event.key==K_UP or event.key==K_DOWN\
        or event.key==K_LEFT or event.key==K_RIGHT) and not (event.key in game.boutons["bas"] or event.key in game.boutons["haut"]):
        game.boutons["haut"][0] = event.key
        objects["touche_haut1txt"].changeTexte(pygame.key.name(event.key).upper())
        calques[1]["touche_haut1txt"][0] = 415-(objects["touche_haut1txt"].renderText().get_rect().width/2)
        objects["touche_haut1"].animCourante = "touche_haut1a"
        objects["fondgris"].visible = False
        objects["choix"].visible = False
        objects["choixtxt"].visible = False
        print(game.boutons)

    if event.type == KEYDOWN and objects["touche_haut2"].animCourante == "touche_haut2b" and ((event.key in range(97,123)) or event.key==K_UP or event.key==K_DOWN\
        or event.key==K_LEFT or event.key==K_RIGHT) and not(event.key in game.boutons["bas"] or event.key in game.boutons["haut"]):
        game.boutons["haut"][1] = event.key
        objects["touche_haut2txt"].changeTexte(pygame.key.name(event.key).upper())
        calques[1]["touche_haut2txt"][0] = 340-(objects["touche_haut2txt"].renderText().get_rect().width/2)
        objects["touche_haut2"].animCourante = "touche_haut2a"
        objects["fondgris"].visible = False
        objects["choix"].visible = False
        objects["choixtxt"].visible = False
        print(game.boutons)

    if event.type == KEYDOWN and objects["touche_haut3"].animCourante == "touche_haut3b" and ((event.key in range(97,123)) or event.key==K_UP or event.key==K_DOWN\
        or event.key==K_LEFT or event.key==K_RIGHT) and not (event.key in game.boutons["bas"] or event.key in game.boutons["haut"]):
        game.boutons["haut"][2] = event.key
        objects["touche_haut3txt"].changeTexte(pygame.key.name(event.key).upper())
        calques[1]["touche_haut3txt"][0] = 490-(objects["touche_haut3txt"].renderText().get_rect().width/2)
        objects["touche_haut3"].animCourante = "touche_haut3a"
        objects["fondgris"].visible = False
        objects["choix"].visible = False
        objects["choixtxt"].visible = False
        print(game.boutons)

    if event.type == KEYDOWN and objects["touche_phase3"].animCourante == "touche_phase3b" and ((event.key in range(97,123)) or event.key==K_SPACE or event.key==K_UP or event.key==K_DOWN\
        or event.key==K_LEFT or event.key==K_RIGHT) and not (event.key in game.boutons["bas"] or event.key in game.boutons["haut"]):
        game.boutons["saut"] = event.key
        objects["touche_phase3txt"].changeTexte(pygame.key.name(event.key).upper())
        calques[1]["touche_phase3txt"][0] = 576-(objects["touche_phase3txt"].renderText().get_rect().width/2)
        objects["touche_phase3"].animCourante = "touche_phase3a"
        objects["fondgris"].visible = False
        objects["choix"].visible = False
        objects["choixtxt"].visible = False
        print(game.boutons)

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["retour"].activate(game.displaylist["retour"])
    if not(objects["fondgris"].visible):
        objects["touche_bas1"].activate(game.displaylist["touche_bas1"])
        objects["touche_bas2"].activate(game.displaylist["touche_bas2"])
        objects["touche_bas3"].activate(game.displaylist["touche_bas3"])
        objects["touche_haut1"].activate(game.displaylist["touche_haut1"])
        objects["touche_haut2"].activate(game.displaylist["touche_haut2"])
        objects["touche_haut3"].activate(game.displaylist["touche_haut3"])
        objects["touche_phase3"].activate(game.displaylist["touche_phase3"])