import pygame
from pygame.locals import *

from classes import *
import game

import keyboard

while game.active:
    game.ecran.fill("black")

    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            game.active = False
        if event.type == game.objects["bouton2"].CLICKED:
            print("Ca marche !")
    
    if keyboard.is_pressed("left"):
        game.scenes[game.scenecourante].camera[0] -= 5
    if keyboard.is_pressed("right"):
        game.scenes[game.scenecourante].camera[0] += 5
        
        

    game.update()

    game.objects["bouton2"].activate(game.displaylist["bouton2"])
    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)

pygame.display.quit()
pygame.quit()