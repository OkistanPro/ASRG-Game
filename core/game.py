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
boutons = {"haut" : [K_d, K_s, K_f], "bas" : [K_j, K_k, K_l], "saut" : K_SPACE}

niveaucourant = ""