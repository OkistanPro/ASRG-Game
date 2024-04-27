import pygame
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
from classes import *

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

def init():
    global objects, calques, camera, fond
    if not objects:
        objects.update({
            "fond_ecranTITRE" : Actif(
                {"anim1" : [PurePath("images/fonds/ecran_titre.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "A" : Actif({"anim1" : [PurePath("images/fonds/A.png")]},
            {"anim1" : [False, 5]},
            "anim1"
            ),
            "S" : Actif({"anim1" : [PurePath("images/fonds/S.png")]},
            {"anim1" : [False, 5]},
            "anim1"
            ),
            "R" : Actif({"anim1" : [PurePath("images/fonds/R.png")]},
            {"anim1" : [False, 5]},
            "anim1"
            ),
            "G" : Actif({"anim1" : [PurePath("images/fonds/G.png")]},
            {"anim1" : [False, 5]},
            "anim1"
            ),
            "Bienvenue" : Text(
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
            "A" : [380, 140],
            "S" : [491, 140],
            "R" : [380, 250],
            "G" : [491, 250],
            "Bienvenue" : [311, 445]
        }
    })
    objects["Bienvenue"].color_shadow = (135,206,250)

# Fonction qui liste les événements que l'on peut effectuer dans l'écran
def loopevent(event):
    # Si on appuie sur la touche entrée, on change d'écran
    if event.type == KEYDOWN and event.key == K_RETURN :
        game.scenecourante = "selectionniveau"
    

def loopbeforeupdate():
    pass

# Fonction qui permet d'activer les boutons présent dans l'écran
def loopafterupdate():
    pass