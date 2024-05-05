import pygame
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
import classes

import game

import time

import copy

# Position de la caméra au début de l'écran
camera = [0, 0]

# Couleur du fond de l'écran 
fond = (0, 0, 0)

#Création de tout les objets que l'on va utiliser dans l'écran
objects = {}

# Emplacement des objets au début dans l'écran
calques = {}

# Son de l'animation du logo
logosound = pygame.mixer.Sound(PurePath("music/logo.wav"))

def init():
    global objects, calques, camera, fond, logosound
    if not objects:
        objects.update({
            "fond_ecranTITRE" : classes.Actif(
                {"anim1" : [PurePath("images/fonds/animation/ecran_titre/" + format(i, '05d') + ".jpg") for i in range(125)]},
                {"anim1" : [True, 2]},
                "anim1"
            ),
            "ASRG" : classes.Actif({"anim1" : [PurePath("images/fonds/animation/animationlogo/" + format(i, '05d') + ".png") for i in range(87)]},
            {"anim1" : [False, 2]},
            "anim1"
            ),
            "Bienvenue" : classes.Text(
                "Appuyez sur 'Entrée' pour commencer",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                20,
                (255, 255, 255)
            )})
    calques.update({
        0:{
            "fond_ecranTITRE" : [0, 0] #[position x, position y]
        },
        1:{
            "ASRG" : [261, 0],
            "Bienvenue" : [311, 445]
        }
    })
    #objects["Bienvenue"].color_shadow = (135,206,250)
    objects["Bienvenue"].color_shadow = (0, 0, 0)

    pygame.mixer.music.load(PurePath("music/aloneintheforest.mp3"))
    pygame.mixer.music.play(loops=-1)
    logosound.play()
    pygame.mixer.music.set_volume(game.volume)

# Fonction qui liste les événements que l'on peut effectuer dans l'écran
def loopevent(event):
    # Si on appuie sur la touche entrée, on change d'écran
    if event.type == KEYDOWN and event.key == K_RETURN :
        classes.imageniveau = "nolevel"
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        game.selectsound.play()
        game.scenecourante = "selectionniveau"
    

def loopbeforeupdate():
    pass

# Fonction qui permet d'activer les boutons présent dans l'écran
def loopafterupdate():
    pass