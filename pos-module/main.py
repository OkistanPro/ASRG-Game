import pygame
from pygame.locals import *

from classes import *
import game

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilenames


while game.active:
    game.ecran.fill("black")

    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            game.active = False
            pygame.display.quit()
            pygame.quit()

        if event.type == MOUSEBUTTONDOWN:
            if game.buttonAjouter.rect.collidepoint(event.pos[0], event.pos[1]):
                Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
                filename = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
                    
    
    
    game.update()

    game.horloge.tick()