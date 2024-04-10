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
            "fondvicperso" : [960 - (game.objects["fondvicperso"].sprites["anim1"][0].get_rect().width), 0],
            "fondvic" : [0, 0]
        },
        1:{
            "quitter" : [312.5 - (game.objects["quitter"].images["quitter"][0][0].get_rect().width), 5],
            "rejouer" : [322.5, 5],
            "cadrescore" : [635+(163 - (game.objects["cadrescore"].sprites["anim1"][0].get_rect().width/2)), 0],
            "phase1" : [10, 25+490/3-(game.objects["phase1"].sprites["anim1"][0].get_rect().height)],
            "phase2" : [10, 25+490*2/3-(game.objects["phase2"].sprites["anim1"][0].get_rect().height)],
            "phase3" : [10, 25+490-(game.objects["phase3"].sprites["anim1"][0].get_rect().height)],
            "pers1" : [635+(163 - (game.objects["pers1"].sprites["debout"][0].get_rect().width/2)), 510-(game.objects["pers1"].sprites["debout"][0].get_rect().height)]
        },
        2:{
            "scoregen" : [643+(163 - (game.objects["cadrescore"].sprites["anim1"][0].get_rect().width/2)), 15],
            "nbscoregen" : [643+(163 - (game.objects["cadrescore"].sprites["anim1"][0].get_rect().width/2) + (game.objects["scoregen"].renderText().get_rect().width)), 15],
            "combogen" : [643+(163 - (game.objects["cadrescore"].sprites["anim1"][0].get_rect().width/2)), 55],
            "nbcombogen" : [643+(163 - (game.objects["cadrescore"].sprites["anim1"][0].get_rect().width/2) + (game.objects["combogen"].renderText().get_rect().width)), 55],
            "pourcentgen" : [643+(163 - (game.objects["cadrescore"].sprites["anim1"][0].get_rect().width/2)), 95],
            "nbpourcentgen" : [643+(163 - (game.objects["cadrescore"].sprites["anim1"][0].get_rect().width/2) + (game.objects["pourcentgen"].renderText().get_rect().width)), 95]
        }}

calques = copy.deepcopy(initcalques)

def init():
    global calques, initcalques, camera, fond
    # Setup les objets (changement des propriétés de chaque objet)
    calques = copy.deepcopy(initcalques)
    game.objects["pers1"].taillex = 1
    game.objects["pers1"].tailley = 1

def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == game.objects["rejouer"].CLICKED:
        game.scenecourante = "scene1"
        camera = [0, 0]
        pygame.mixer.music.play(start=0.0)
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    game.objects["rejouer"].activate(game.displaylist["rejouer"])