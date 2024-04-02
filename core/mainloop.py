import pygame
from pygame.locals import *

from classes import *
import game

import keyboard

up = 0
down = 0

while game.active:
    
    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            game.active = False

        
        if event.type == KEYDOWN and event.key == K_UP:
            up = 1

        if event.type == KEYUP and event.key == K_UP:
            up = 0

        if event.type == KEYDOWN and event.key == K_DOWN:
            down = 1

        if event.type == KEYUP and event.key == K_DOWN:
            down = 0

    if up == 1:
        game.scenes[game.scenecourante].camera[0] += 5

    if down == 1:
        game.scenes[game.scenecourante].camera[0] -= 5
    
    game.update()
    # Activation des boutons
    
    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)

pygame.display.quit()
pygame.quit()