import pygame
from pygame.locals import *
from pathlib import Path, PurePath

from classes import *
import levelfiles.levelmaker as levelmaker


import copy


pygame.init()

# Définition globale
titreJeu = "Un jeu."
iconeJeu = ""
tailleEcran = largeurEcran, hauteurEcran = (960, 540)
ecran = pygame.display.set_mode(tailleEcran, DOUBLEBUF, vsync=1)

# Définition de l'horloge
horloge = pygame.time.Clock()
FPS = 60

# Scène qui sera affiché
scenecourante = "ecranTitre"

# Liste des objets qui seront affichés après le update
displaylist = {}

# Boucle de jeu
active = True

# Dictionnaire des boutons à utiliser dans les phase 1 et 3
boutons = {
    "haut" : [K_d, K_s, K_f], 
    "bas" : [K_j, K_k, K_l], 
    "saut" : K_SPACE
}

volume = 1
selectsound = pygame.mixer.Sound(PurePath("music/select.wav"))

scoreglobal = 0

with open("save.asrg") as filesave:
    for line in filesave:
        if "SCOREGLOBAL" in line:
            scoreglobal = int(line[:-1].split("\t")[1])

niveauglobal = scoreglobal // 1000000

niveaucourant = ""
niveaudifficulte = 0

stats_perso = {
    "score" : 0,
    "pv" : 200,
    "compteurcomboglobal" : 0,
    "comboglobal" : 0,

    "scorephase1": 0,
    "scorephase2": 0,
    "scorephase3": 0,

    "precisionphase1" : 0,
    "precisionphase2" : 0,
    "precisionphase3" : 0,

    "compteurcombophase1" : 0,
    "compteurcombophase2" : 0,
    "combophase1" : 0,
    "combophase2" : 0,

    "compteurtempsphase3" : 0,
    "tempsphase3" : 0,

    "notesphase1" : 0,
    "notesphase3" : 0,

    "missphase1" : 0,
    "missphase2" : 0,
    "missphase3" : 0,

    "greatphase1" : 0,
    "greatphase2" : 0,
    
    "perfectphase1" : 0,
    "perfectphase2" : 0,

    "passphase2" : 0,

    "inLongUp" : False,
    "inLongDown" : False,
    "tempsUp" : "",
    "tempsDown" : ""
}
