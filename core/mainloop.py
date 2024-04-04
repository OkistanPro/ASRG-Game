import pygame
from pygame.locals import *

from classes import *
import game

import keyboard


while game.active:
    
    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            game.active = False

        
        if event.type == KEYDOWN and event.key == K_UP:
            game.objects["pers1"].posy = 100

        if event.type == KEYDOWN and event.key == K_DOWN:
            game.objects["pers1"].posy = 280

    game.scenes[game.scenecourante].camera[0] += 10
    
    game.update()
    
    # Activation des boutons

    # Boucle de fond
    if game.displaylist["premierFond"].right == 0:
        game.objects["premierFond"].posx += 1920
    if game.displaylist["premierFondbis"].right == 0:
        game.objects["premierFondbis"].posx += 1920
    if game.displaylist["deuxiemeFond"].right == 0:
        game.objects["deuxiemeFond"].posx += 1920
    if game.displaylist["deuxiemeFondbis"].right == 0:
        game.objects["deuxiemeFondbis"].posx += 1920
    if game.displaylist["troisiemeFond"].right == 0:
        game.objects["troisiemeFond"].posx += 1920
    if game.displaylist["troisiemeFondbis"].right == 0:
        game.objects["troisiemeFondbis"].posx += 1920
    if game.displaylist["quatriemeFond"].right == 0:
        game.objects["quatriemeFond"].posx += 1920
    if game.displaylist["quatriemeFondbis"].right == 0:
        game.objects["quatriemeFondbis"].posx += 1920
    if game.displaylist["solbis"].right == 0:
        game.objects["solbis"].posx += 1920
    if game.displaylist["sol"].right == 0:
        game.objects["sol"].posx += 1920

    
    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)

pygame.display.quit()
pygame.quit()