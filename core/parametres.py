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

select = False


def init():
    global objects, calques, camera, fond
    if not objects:
        objects.update({"fond_param" : Actif(
                {"anim1" : [PurePath("images/fonds/animation/ecran_parametres/" + format(i, '05d') + ".jpg") for i in range(125)]},
                {"anim1" : [True, 2]},
                "anim1"
            ),
            "barreSon" : Actif(
                {"anim1" : [PurePath("images/interface/barreSon.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "rondBarreSon" : Actif(
                {"anim1" : [PurePath("images/interface/rondBarreSon.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "son" : Text(
                "Volume :",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                35,
                (255,255,255)
            ),
            "touches" : Bouton(
                {"touchesb" :
            [
                [PurePath("images/interface/boutTouches.png")],
                [PurePath("images/interface/boutTouches.png")],
                [PurePath("images/interface/boutTouches.png")],
                [PurePath("images/interface/boutTouches.png")],
                [PurePath("images/interface/boutTouches.png")]
            ]},
            {"touchesb" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "touchesb"
            ),
            "textTouches" : Text(
                "Touches",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                38,
                (255,255,255)
            ),
            "tuto" : Bouton(
                {"tutob" :
            [
                [PurePath("images/interface/boutRejTuto.png")],
                [PurePath("images/interface/boutRejTuto.png")],
                [PurePath("images/interface/boutRejTuto.png")],
                [PurePath("images/interface/boutRejTuto.png")],
                [PurePath("images/interface/boutRejTuto.png")]
            ]},
            {"tutob" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "tutob"
            ),
            "textTuto" : Text(
                "Rejouer le tutoriel",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                38,
                (255,255,255)
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
            )})
    calques.update({
        0:{
            "fond_param" : [0, 0]
        },
        1: {
            "retour" : [0, 0],
            "son" : [40, 120],
            "barreSon" : [220, 88],
            "rondBarreSon" : [220 + (305*game.volume), 120],
            "touches" : [40, 225],
            "tuto" : [40, 390]
        },
        2:{
            "textTouches" : [80, 260],
            "textTuto" : [80, 425]
        }
    })

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(PurePath("music/intheembraceofdarkness.mp3"))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(game.volume)

def loopevent(event):
    global pause, button, gameovertimer, camera, select
    if event.type == objects["retour"].CLICKED:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        game.selectsound.play()
        game.scenecourante = "selectionniveau"
    if event.type == MOUSEBUTTONDOWN and game.displaylist["barreSon"].collidepoint(pygame.mouse.get_pos()):
        select = True
    if event.type == MOUSEBUTTONUP:
        select = False
    if event.type == objects["touches"].CLICKED:
        game.selectsound.play()
        game.scenecourante = "ecran_touches"
    if event.type == objects["tuto"].CLICKED:
        game.selectsound.play()
        game.scenecourante = "scene1"
        camera = [0, 0]
        
    

def loopbeforeupdate():
    global select
    if select and 205 <= pygame.mouse.get_pos()[0] - 15 <= 525:
        calques[1]["rondBarreSon"][0] = pygame.mouse.get_pos()[0] - 15
        game.volume = (calques[1]["rondBarreSon"][0] - 205) / 305
        pygame.mixer.music.set_volume(game.volume)
        game.selectsound.set_volume(game.volume)


def loopafterupdate():
     global pause, button, gameovertimer, camera
     objects["touches"].activate(game.displaylist["touches"])
     objects["retour"].activate(game.displaylist["retour"])
     objects["tuto"].activate(game.displaylist["tuto"])