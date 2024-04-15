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

objects = {"fond_ecranTITRE" : Actif(
    {"anim1" : [PurePath("images/fonds/fond_ecranTITRE.png")]},
    {"anim1" : [False, 5]},
    "anim1"
)}


initcalques = {
        0:{
            "fond_ecranTITRE" : [0, 0]
        }
}