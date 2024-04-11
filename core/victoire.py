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

objects = {"fondvicperso" : Actif(
    {"anim1" : [PurePath("images/interface/fond_perso_V.png")]},
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
    (0,0,0)
),
"nbscoregen" : Text(
    "3456500",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    19,
    (0,0,0)
),
"combogen" : Text(
    "Combo Général : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"nbcombogen" : Text(
    "135",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"nbpourcentgen" : Text(
    "80%",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"fondvic" : Actif(
    {"anim1" : [PurePath("images/interface/Fond_phases_EV.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"quitter" : Bouton( {"quitter" :
[
    [PurePath("images/interface/Bouton_quitter.png")],
    [PurePath("images/interface/Bouton_quitter.png")],
    [PurePath("images/interface/Bouton_quitter.png")],
    [PurePath("images/interface/Bouton_quitter.png")],
    [PurePath("images/interface/Bouton_quitter.png")]
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
    [PurePath("images/interface/Bouton_rejouer.png")],
    [PurePath("images/interface/Bouton_rejouer.png")],
    [PurePath("images/interface/Bouton_rejouer.png")],
    [PurePath("images/interface/Bouton_rejouer.png")],
    [PurePath("images/interface/Bouton_rejouer.png")]
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
    (0,0,0)
),
"Scorevic1" : Text(
    "Score : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    30,
    (0,0,0)
),
"numscore1" : Text(
    "1000000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
),
"miss1" : Text(
    "Miss : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"numiss1" : Text(
    "4",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255,0,0)
),
"great1" : Text(
    "Great : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"numgreat1" : Text(
    "38",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255,0,0)
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
    (0,0,0)
),
"Scorevic2" : Text(
    "Score : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    30,
    (0,0,0)
),
"numscore2" : Text(
    "1000000",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
),
"miss2" : Text(
    "Miss : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"numiss2" : Text(
    "15",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255,0,0)
),
"great2" : Text(
    "Great : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"numgreat2" : Text(
    "44",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255,0,0)
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
    (0,0,0)
),
"Scorevic3" : Text(
    "Score : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    30,
    (0,0,0)
),
"numscore3" : Text(
    "1456500",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    25,
    (255,0,0)
),
"miss3" : Text(
    "Miss : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"numiss3" : Text(
    "20",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255,0,0)
),
"pass" : Text(
    "Pass : ",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (0,0,0)
),
"numpass" : Text(
    "80",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255,0,0)
),
"pers1" : Actif(
    {"debout" : [PurePath("images/level/personnage.png")]},
    {"debout" : [True, 5]}, #Au hazard
    "debout"
)}

# valeurs de scenes

initcalques = {
        0:{
            "fondvicperso" : [960 - (objects["fondvicperso"].sprites["anim1"][0].get_rect().width), 0],
            "fondvic" : [0, 0]
        },
        1:{
            "quitter" : [312.5 - (objects["quitter"].images["quitter"][0][0].get_rect().width), 5],
            "rejouer" : [322.5, 5],
            "cadrescore" : [635+(163 - (objects["cadrescore"].sprites["anim1"][0].get_rect().width/2)), 0],
            "phase1" : [10, 25+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)],
            "phase2" : [10, 25+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)],
            "phase3" : [10, 25+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)],
            "pers1" : [635+(163 - (objects["pers1"].sprites["debout"][0].get_rect().width/2)), 510-(objects["pers1"].sprites["debout"][0].get_rect().height)]
        },
        2:{
            "scoregen" : [643+(163 - (objects["cadrescore"].sprites["anim1"][0].get_rect().width/2)), 15],
            "nbscoregen" : [643+(163 - (objects["cadrescore"].sprites["anim1"][0].get_rect().width/2) + (objects["scoregen"].renderText().get_rect().width)), 15],
            "combogen" : [643+(163 - (objects["cadrescore"].sprites["anim1"][0].get_rect().width/2)), 55],
            "nbcombogen" : [643+(163 - (objects["cadrescore"].sprites["anim1"][0].get_rect().width/2) + (objects["combogen"].renderText().get_rect().width)), 55],
            "nbpourcentgen" : [635+(163 - (objects["nbpourcentgen"].renderText().get_rect().width/2)), 95]
        },
        3:{
            "Scorevic1" : [20+(objects["phase1"].sprites["anim1"][0].get_rect().width), 30+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)],
            "numscore1" : [20+(objects["phase1"].sprites["anim1"][0].get_rect().width)+(objects["Scorevic1"].renderText().get_rect().width), 34+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)],
            "nbpourcent1" : [595-(objects["nbpourcent1"].renderText().get_rect().width), 30+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)],
            "miss1" : [40+(objects["phase1"].sprites["anim1"][0].get_rect().width), 40+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic1"].renderText().get_rect().height)],
            "numiss1" : [40+(objects["phase1"].sprites["anim1"][0].get_rect().width) + (objects["miss1"].renderText().get_rect().width), 40+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic1"].renderText().get_rect().height)],
            "great1" : [318, 40+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic1"].renderText().get_rect().height)],
            "numgreat1" : [318+(objects["great1"].renderText().get_rect().width), 40+490/3-(objects["phase1"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic1"].renderText().get_rect().height)],
            "Scorevic2" : [20+(objects["phase2"].sprites["anim1"][0].get_rect().width), 30+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)],
            "numscore2" : [20+(objects["phase2"].sprites["anim1"][0].get_rect().width)+(objects["Scorevic2"].renderText().get_rect().width), 34+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)],
            "nbpourcent2" : [595-(objects["nbpourcent2"].renderText().get_rect().width), 30+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)],
            "miss2" : [40+(objects["phase2"].sprites["anim1"][0].get_rect().width), 40+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic2"].renderText().get_rect().height)],
            "numiss2" : [40+(objects["phase2"].sprites["anim1"][0].get_rect().width) + (objects["miss2"].renderText().get_rect().width), 40+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic2"].renderText().get_rect().height)],
            "great2" : [318, 40+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic2"].renderText().get_rect().height)],
            "numgreat2" : [318+(objects["great2"].renderText().get_rect().width), 40+490*2/3-(objects["phase2"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic2"].renderText().get_rect().height)],
            "Scorevic3" : [20+(objects["phase3"].sprites["anim1"][0].get_rect().width), 30+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)],
            "numscore3" : [20+(objects["phase2"].sprites["anim1"][0].get_rect().width)+(objects["Scorevic3"].renderText().get_rect().width), 34+490-(objects["phase2"].sprites["anim1"][0].get_rect().height)],
            "nbpourcent3" : [595-(objects["nbpourcent3"].renderText().get_rect().width), 30+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)],
            "miss3" : [(635-(objects["phase3"].sprites["anim1"][0].get_rect().width))/2-40-(objects["numiss3"].renderText().get_rect().width)-(objects["miss3"].renderText().get_rect().width), 40+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic3"].renderText().get_rect().height)],
            "numiss3" : [(635-(objects["phase3"].sprites["anim1"][0].get_rect().width))/2-40-(objects["numiss3"].renderText().get_rect().width), 40+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic3"].renderText().get_rect().height)],
            "pass" : [(635-(objects["phase3"].sprites["anim1"][0].get_rect().width))/2+40, 40+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic3"].renderText().get_rect().height)],
            "numpass" : [(635-(objects["phase3"].sprites["anim1"][0].get_rect().width))/2+40+(objects["pass"].renderText().get_rect().width), 40+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)+(objects["Scorevic3"].renderText().get_rect().height)]
        }}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    # Setup les objets (changement des propriétés de chaque objet)
    calques = copy.deepcopy(initcalques)
    objects["pers1"].taillex = 1
    objects["pers1"].tailley = 1

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["rejouer"].CLICKED:
        game.scenecourante = "scene1"
        camera = [0, 0]
        pygame.mixer.music.play(start=0.0)
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["rejouer"].activate(game.displaylist["rejouer"])