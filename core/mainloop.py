import pygame
import pygame.freetype
from pygame.locals import *

from classes import *
import game

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

        if event.type == KEYDOWN and event.key == K_h:
            game.scenecourante = 0

        game.button1.activate(event)
        game.button2.activate(event)

    game.text01.text = str(game.scenecourante)
    game.update()

    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)