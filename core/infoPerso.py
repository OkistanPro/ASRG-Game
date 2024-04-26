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

objects = {"fond_infoPersoG" : Actif(
    {"anim1" : [PurePath("images/fonds/fond_info_perso_gauche.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"fond_infoPersoD" : Actif(
{"anim1" : [PurePath("images/fonds/fond_info_perso_droite.png")]},
{"anim1" : [False, 5]},
"anim1"
),
"flecheG" : Actif
    ({"anim1" : [PurePath("images/interface/fleche_gauche_ecran_IP.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"flecheD" : Actif
    ({"anim1" : [PurePath("images/interface/fleche_droite_ecran_IP.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"textnbNiveaux" : Text(
    "Nombre de niveaux débloqués :",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255, 255, 255)
),
"NbNiveaux" : Text(
    "1/4",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255, 255, 255)
),
"progression" : Text(
    "Progression du jeu",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255, 255, 255)
),
"progFacile" : Text(
    "25%",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255, 255, 255)
),
"progDiff" : Text(
    "0%",
    PurePath("fonts/LTSaeada-SemiBold.otf"),
    20,
    (255, 255, 255)
),

}