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

# valeurs de scenes

calques = {}

def init():
    global objects, calques, camera, fond
    objects.update({"fondvicperso" : Actif(
        {"anim1" : [PurePath("images/fonds/fond_perso_V.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "cadrescore" : Actif(
        {"anim1" : [PurePath("images/interface/cadre_score_V.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "scoregen" : Text(
        "Score Général : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (0, 0, 0)
    ),
    "nbscoregen" : Text(
        "3456500",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        19,
        (0, 0, 0)
    ),
    "combogen" : Text(
        "Combo Général : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (0, 0, 0)
    ),
    "nbcombogen" : Text(
        "135",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (0, 0, 0)
    ),
    "nbpourcentgen" : Text(
        "80%",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (0, 0, 0)
    ),
    "fondvic" : Actif(
        {"anim1" : [PurePath("images/fonds/Fond_phases_EV.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "quitter" : Bouton( {"quitter" :
    [
        [PurePath("images/interface/flecheretour.png")],
        [PurePath("images/interface/flecheretour.png")],
        [PurePath("images/interface/flecheretour.png")],
        [PurePath("images/interface/flecheretour.png")],
        [PurePath("images/interface/flecheretour.png")]
    ]},
    {"quitter" :[
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5]
    ]},
    "quitter"),
    "rejouer" : Bouton( {"rejouer" :
    [
        [PurePath("images/interface/Fleche_Recommencer.png")],
        [PurePath("images/interface/Fleche_Recommencer.png")],
        [PurePath("images/interface/Fleche_Recommencer.png")],
        [PurePath("images/interface/Fleche_Recommencer.png")],
        [PurePath("images/interface/Fleche_Recommencer.png")]
    ]},
    {"rejouer" :[
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5]
    ]},
    "rejouer"),
    "phase1" : Actif(
        {"anim1" : [PurePath("images/interface/phase1.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "nbpourcent1" : Text(
        "90%",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "Scorevic1" : Text(
        "Score : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "numscore1" : Text(
        "1000000",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        25,
        (254, 95, 83)
    ),
    "miss1" : Text(
        "Miss : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numiss1" : Text(
        "7",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (254, 95, 83)
    ),
    "great1" : Text(
        "Great : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numgreat1" : Text(
        "38",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (254, 95, 83)
    ),
    "perfect1" : Text(
        "Perfect : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numperfect1" : Text(
        "70",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (254, 95, 83)
    ),
    "combo1" : Text(
        "Combo Max : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numcombo1" : Text(
        "52",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (254, 95, 83)
    ),
    "phase2" : Actif(
        {"anim1" : [PurePath("images/interface/phase2.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "nbpourcent2" : Text(
        "70%",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "Scorevic2" : Text(
        "Score : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "numscore2" : Text(
        "1000000",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        25,
        (84, 185, 255)
    ),
    "miss2" : Text(
        "Miss : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numiss2" : Text(
        "15",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "great2" : Text(
        "Great : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numgreat2" : Text(
        "44",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "perfect2" : Text(
        "Perfect : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numperfect2" : Text(
        "27",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "pass2" : Text(
        "Pass : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numpass2" : Text(
        "20",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "combo2" : Text(
        "Combo Max : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numcombo2" : Text(
        "13",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "phase3" : Actif(
        {"anim1" : [PurePath("images/interface/phase3.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "nbpourcent3" : Text(
        "80%",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "Scorevic3" : Text(
        "Score : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "numscore3" : Text(
        "1456500",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        25,
        (246, 240, 119)
    ),
    "miss3" : Text(
        "Miss : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numiss3" : Text(
        "20",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (246, 240, 119)
    ),
    "pass3" : Text(
        "Pass : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numpass3" : Text(
        "80",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (246, 240, 119)
    ),
    "combo3" : Text(
        "Combo Max : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numcombo3" : Text(
        "25",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (246, 240, 119)
    ),
    "pers1" : Actif(
        {"debout" : [PurePath("images/level/personnage.png")]},
        {"debout" : [True, 5]}, #Au hazard
        "debout"
    )})
    # Setup les objets (changement des propriétés de chaque objet)
    calques.update({
        0:{
            "fondvicperso" : [635, 0],
            "fondvic" : [0, 0]
        },
        1:{
            "quitter" : [0, 0],
            "rejouer" : [565, 0],
            "cadrescore" : [677, 0],
            "phase1" : [10, 90],
            "phase2" : [10, 254],
            "phase3" : [10, 418],
            "pers1" : [752, 213]
        },
        2:{
            "scoregen" : [687, 15],
            "nbscoregen" : [834, 16],
            "combogen" : [687, 55],
            "nbcombogen" : [846, 56],
            "nbpourcentgen" : [778, 95]
        },
        3:{
            "Scorevic1" : [124, 96],
            "numscore1" : [224, 101],
            "nbpourcent1" : [533, 96],
            "miss1" : [144, 129],
            "numiss1" : [197, 130],
            "great1" : [313, 129],
            "numgreat1" : [382, 130],
            "perfect1" : [484, 129],
            "numperfect1" : [567, 130],
            "combo1" : [268, 154],
            "numcombo1" : [391, 155],

            "Scorevic2" : [124, 259],
            "numscore2" : [224, 264],
            "nbpourcent2" : [533, 259],
            "miss2" : [144, 293],
            "numiss2" : [197, 294],
            "great2" : [313, 293],
            "numgreat2" : [382, 294],
            "perfect2" : [484, 293],
            "numperfect2" : [567, 294],
            "pass2" : [232, 319],
            "numpass2" : [289, 319],
            "combo2" : [407, 319],
            "numcombo2" : [530, 320],

            "Scorevic3" : [124, 423],
            "numscore3" : [224, 428],
            "nbpourcent3" : [533, 423],#[595-(objects["nbpourcent3"].renderText().get_rect().width), 30+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)],
            "miss3" : [144, 456],
            "numiss3" : [197, 457],
            "pass3" : [144, 481],
            "numpass3" : [201, 482],
            "combo3" : [268, 481],
            "numcombo3" : [391, 482]
        }})
    objects["pers1"].taillex = 1
    objects["pers1"].tailley = 1
    objects["scoregen"].color_shadow = (180, 180, 180)
    objects["nbscoregen"].color_shadow = (180, 180, 180)
    objects["combogen"].color_shadow = (180, 180, 180)
    objects["nbcombogen"].color_shadow = (180, 180, 180)
    objects["nbpourcentgen"].color_shadow = (180, 180, 180)

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["rejouer"].CLICKED:
        game.scenecourante = "scene1"
        camera = [0, 0]
        pygame.mixer.music.play(start=0.0)
    if event.type == objects["quitter"].CLICKED:
        game.scenecourante = "selectionniveau"
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["rejouer"].activate(game.displaylist["rejouer"])
    objects["quitter"].activate(game.displaylist["quitter"])